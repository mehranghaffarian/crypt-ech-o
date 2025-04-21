# File: etl/load/base_loader.py
import logging
from abc import ABC, abstractmethod
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from utils.config import DB_URL

logger = logging.getLogger(__name__)

class Loader(ABC):
    def __init__(self, db_url: str = None):
        self.db_url = db_url or DB_URL
        self.engine = create_engine(self.db_url)
        self.meta = MetaData(bind=self.engine)
        logger.info(f"DB engine initialized at {self.db_url}")

    @abstractmethod
    def load(self, df):
        pass

    def _upsert(self, table_name: str, df, constraint_cols, update_cols=None):
        """
        Generic upsert helper.
        - table_name: target table
        - df: DataFrame
        - constraint_cols: list of columns that form the unique constraint
        - update_cols: if provided, columns to update on conflict (else DO NOTHING)
        """
        table = Table(table_name, self.meta, autoload_with=self.engine)
        records = df.to_dict(orient='records')
        stmt = pg_insert(table).values(records)

        if update_cols:
            # e.g. UPDATE price_usd = EXCLUDED.price_usd, ...
            update_dict = {col: stmt.excluded[col] for col in update_cols}
            stmt = stmt.on_conflict_do_update(
                index_elements=constraint_cols,
                set_=update_dict
            )
        else:
            stmt = stmt.on_conflict_do_nothing(
                index_elements=constraint_cols
            )

        with self.engine.begin() as conn:
            result = conn.execute(stmt)
            inserted = result.rowcount  # note: for DO NOTHING, this is number of rows actually inserted
            logger.info(f"{inserted} rows upserted into '{table_name}' (conflict cols={constraint_cols})")
        return inserted
