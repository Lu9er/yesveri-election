from datetime import datetime

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database import ClaimVerification


class CleanupService:
    """Delete expired claim verification records."""

    async def delete_expired(self, db: AsyncSession) -> int:
        now = datetime.utcnow()
        result = await db.execute(
            delete(ClaimVerification).where(ClaimVerification.expires_at < now)
        )
        await db.commit()
        return result.rowcount or 0
