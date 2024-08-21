import logging
import os
import uuid

import pandas as pd

from models import FileStorage

logger = logging.getLogger(__name__)


class FileManager:
    def __init__(self, storage_dir="data_dump"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_file(self, session, **kwargs):
        logger.info("Storing File path")

        file_id = kwargs.get("file_id") if kwargs.get("file_id") else str(uuid.uuid4())
        file_path = os.path.join(self.storage_dir, f"{file_id}.csv")

        file_storage = FileStorage(
            file_id=file_id,
        )
        if kwargs.get("file"):
            file = kwargs.get("file")
            with open(file_path, "wb") as f:
                f.write(file.read())
        elif "df" in kwargs:
            kwargs.get("df").to_csv(file_path, index=False)

        session.add(file_storage)
        session.commit()
        return file_id

    def load_file(self, file_id):
        file_path = os.path.join(self.storage_dir, f"{file_id}.csv")
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            raise FileNotFoundError("File not found")
