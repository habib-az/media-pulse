from pydantic import BaseModel
from typing import Optional


class Podcast(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    url: str
    language: Optional[str]


class Publication(BaseModel):
    id: Optional[int]
    title: str
    abstract: Optional[str]
    url: str
    publication_date: Optional[str]
    language: Optional[str]


class ContentSummary(BaseModel):
    id: Optional[int]
    podcast_id: Optional[int]
    publication_id: Optional[int]
    summary: str


class GeneratedContent(BaseModel):
    id: Optional[int]
    content_type: str
    content: str
    summary_id: Optional[int]


class User(BaseModel):
    id: Optional[int]
    user_id: str
    name: str
    email: str
    password: str
    preferences: Optional[dict]
