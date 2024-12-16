import random
import string
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import select

from app.api.deps import DBSessionDep, RedisSessionDep
from app.core.config import settings
from app.models import URL, HitStats, ShortURL, URLResponse

router = APIRouter()


def generate_short_id(length: int = 6) -> str:
    """Generate a random string of letters and digits"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@router.get("/shorten", response_model=ShortURL)
def shorten_url(url: str, session: DBSessionDep, redis_client: RedisSessionDep) -> Any:
    """Shorten a URL"""
    short_id = generate_short_id()

    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = f"{settings.DEFAULT_URL_SCHEMA}://{url}"
    url = URL(original_url=url, short_id=short_id)
    session.add(url)
    session.commit()
    session.refresh(url)

    # Store the result in Redis
    redis_client.set(short_id, url.original_url, ex=2592000)  # Set expiration to 1 month (30 days)

    return ShortURL(
        original_url=url.original_url,
        expires_at=url.expires_at,
        short_url=f"{settings.FRONTEND_HOST}/{url.short_id}",
    )


@router.get("/redirect", response_model=URLResponse)
def redirect_to_url(short_id: str, session: DBSessionDep, redis_client: RedisSessionDep):
    """Redirect to the original URL"""
    # First, check Redis cache
    if original_url := redis_client.get(short_id):
        return RedirectResponse(original_url)

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

    # Return a redirect response
    return RedirectResponse(result.original_url)
