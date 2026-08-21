"""Pydantic schemas for request validation and response serialization."""

from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    """Request body for POST /shorten."""
    url: HttpUrl


class URLResponse(BaseModel):
    """Response body returned after shortening a URL."""
    short_code: str
    short_url: str

    model_config = {"from_attributes": True}
