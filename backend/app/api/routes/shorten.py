import random
import string
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.core.config import settings
from app.models import URL, HitStats, ShortURL, URLResponse

router = APIRouter()


def generate_short_id(length: int = 6) -> str:
    """Generate a random string of letters and digits"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@router.post("/", response_model=ShortURL)
def shorten_url(original_url: str, session: SessionDep) -> Any:
    """Shorten a URL"""
    short_id = generate_short_id()
    url = URL(original_url=original_url, short_id=short_id)
    session.add(url)
    session.commit()
    session.refresh(url)

    return ShortURL(
        original_url=url.original_url,
        expires_at=url.expires_at,
        short_url=f"{settings.HOST_NAME}/{url.short_id}",
    )


@router.get("/{short_id}", response_model=URLResponse)
def redirect_to_url(short_id: str, session: SessionDep):
    """Redirect to the original URL"""
    statement = select(URL).where(URL.short_id == short_id)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="URL not found")

    # Update hit stats
    statement = select(HitStats).where(HitStats.url_id == result.id)
    hit_stats = session.exec(statement).first()
    if hit_stats:
        hit_stats.increment_hits()
    else:
        hit_stats = HitStats(url_id=result.id, hits=1, last_hit=datetime.now(timezone.utc))
        session.add(hit_stats)

    session.commit()

    # Return the original URL
    return URLResponse(original_url=result.original_url, hits=hit_stats.hits)
