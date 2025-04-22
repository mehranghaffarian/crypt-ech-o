import json
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Transformer(ABC):
    def __init__(self, raw_path: str):
        """
        raw_path: full path to your JSON file,
          e.g. 'data/raw/news/crypto/news__2025-04-11_to_2025-04-21.json'
        """
        self.raw_path = Path(raw_path)

    @abstractmethod
    def transform(self) -> pd.DataFrame:
        pass