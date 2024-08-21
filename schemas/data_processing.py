from typing import Dict, List

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class TransformationRequest(BaseModel):
    normalize: List[str] = []
    fill_missing: Dict[str, float] = {}


class FileUploadResponse(BaseModel):
    message: str
    file_id: str

class SummaryResponse(BaseModel):
    summary: Dict[str, Dict[str, Any]]

class TransformResponse(BaseModel):
    message: str
    file_id: str
