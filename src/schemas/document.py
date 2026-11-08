from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DocumentOut(BaseModel):
    id: int
    filename: str
    file_type: str
    size_bytes: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DocumentDetail(DocumentOut):
    text_length: int
    preview: str


class QuestionIn(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
