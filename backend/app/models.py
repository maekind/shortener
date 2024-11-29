import uuid
from datetime import datetime, timedelta, timezone

from sqlmodel import Field, SQLModel


class URL(SQLModel, table=True):
    """Represents a URL entry in the database."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    original_url: str
    short_id: str = Field(index=True, unique=True)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=30)
    )


class ShortURL(SQLModel):
    """This is the model of the response for creating a short URL."""

    original_url: str
    expires_at: datetime
    short_url: str  # Dynamically added field for the shortened URL


class URLResponse(SQLModel):
    """This is the model of the response for getting the original URL by ID."""

    original_url: str
    hits: int


class HitStats(SQLModel, table=True):
    """Tracks statistics of URL hits."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hits: int = Field(default=0)
    url_id: uuid.UUID = Field(foreign_key="url.id", nullable=False)
    last_hit: datetime = Field(default_factory=datetime.now)

    def increment_hits(self):
        self.hits += 1
        self.last_hit = datetime.now()
