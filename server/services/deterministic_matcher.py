from typing import Any, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database import ElectionResult, OfficialSource
from server.models.enums import AlignmentStatus


class MatchResult:
    def __init__(
        self,
        alignment: AlignmentStatus,
        official_result: Optional[Any] = None,
        source: Optional[Any] = None,
        confidence: float = 0.0,
        conflicts: Optional[list] = None,
    ):
        self.alignment = alignment
        self.official_result = official_result
        self.source = source
        self.confidence = confidence
        self.conflicts = conflicts or []


class DeterministicMatcher:
    """Compare extracted entities against official EC data."""

    async def match(self, extracted: dict, db: AsyncSession) -> MatchResult:
        # Build query filters based on what was extracted
        filters = []

        if extracted.get("candidate_name"):
            # Use ILIKE for fuzzy matching
            name = extracted["candidate_name"]
            # Try matching against any part of the candidate name
            filters.append(
                ElectionResult.candidate_name.ilike(f"%{name.split()[-1]}%")
            )

        if extracted.get("district"):
            filters.append(
                ElectionResult.district.ilike(f"%{extracted['district']}%")
            )

        if extracted.get("position"):
            pos = extracted["position"]
            # Normalize MP variants
            if pos in ("MP", "Member of Parliament"):
                filters.append(
                    ElectionResult.position.ilike("%Member of Parliament%")
                    | ElectionResult.position.ilike("%MP%")
                )
            else:
                filters.append(ElectionResult.position.ilike(f"%{pos}%"))

        if extracted.get("party"):
            filters.append(ElectionResult.party.ilike(f"%{extracted['party']}%"))

        # If we have no meaningful filters, we cannot verify
        if not filters:
            return MatchResult(
                alignment=AlignmentStatus.CANNOT_VERIFY,
                confidence=0.0,
            )

        # Try with all filters first
        result = await self._query_with_filters(filters, db)

        if not result:
            # Progressive relaxation: try with fewer filters
            # Try candidate + district only
            relaxed = [f for f in filters[:2]]
            if len(relaxed) >= 1:
                result = await self._query_with_filters(relaxed, db)

            # Try candidate only
            if not result and filters:
                result = await self._query_with_filters([filters[0]], db)

        if not result:
            return MatchResult(
                alignment=AlignmentStatus.NO_OFFICIAL_DATA,
                confidence=0.3,
            )

        # Get the source for this result
        source = await self._get_source(result.source_id, db)

        # Compare fields
        conflicts = self._compare_fields(extracted, result)
        confidence = self._calculate_confidence(extracted, result, conflicts)

        if conflicts:
            alignment = AlignmentStatus.CONFLICTS
        else:
            alignment = AlignmentStatus.MATCHES

        return MatchResult(
            alignment=alignment,
            official_result=result,
            source=source,
            confidence=confidence,
            conflicts=conflicts,
        )

    async def _query_with_filters(
        self, filters: list, db: AsyncSession
    ) -> Optional[ElectionResult]:
        query = select(ElectionResult).where(and_(*filters)).limit(5)
        rows = await db.execute(query)
        results = rows.scalars().all()
        return results[0] if results else None

    async def _get_source(
        self, source_id: int, db: AsyncSession
    ) -> Optional[OfficialSource]:
        query = select(OfficialSource).where(OfficialSource.id == source_id)
        row = await db.execute(query)
        return row.scalar_one_or_none()

    def _compare_fields(self, extracted: dict, official: ElectionResult) -> list:
        conflicts = []

        # Vote count comparison
        if extracted.get("vote_count") is not None and official.vote_count:
            claimed = extracted["vote_count"]
            actual = official.vote_count
            # Allow 1% tolerance for rounding
            if abs(claimed - actual) / max(claimed, actual) > 0.01:
                conflicts.append(
                    {
                        "field": "vote_count",
                        "claimed": claimed,
                        "official": actual,
                    }
                )

        # Percentage comparison
        if extracted.get("percentage") is not None and official.percentage:
            claimed = extracted["percentage"]
            actual = official.percentage
            if abs(claimed - actual) > 0.5:
                conflicts.append(
                    {
                        "field": "percentage",
                        "claimed": claimed,
                        "official": actual,
                    }
                )

        # Result claim: "won" vs is_winner
        if extracted.get("result_claim") in ("won", "wins", "winning", "elected"):
            if not official.is_winner:
                conflicts.append(
                    {
                        "field": "result_claim",
                        "claimed": "won",
                        "official": "did not win according to official results",
                    }
                )
        elif extracted.get("result_claim") in ("lost", "loses", "losing", "defeated"):
            if official.is_winner:
                conflicts.append(
                    {
                        "field": "result_claim",
                        "claimed": "lost",
                        "official": "won according to official results",
                    }
                )

        return conflicts

    def _calculate_confidence(
        self, extracted: dict, official: ElectionResult, conflicts: list
    ) -> float:
        """
        Confidence reflects how many fields we could meaningfully compare.
        Higher confidence = more data points matched.
        """
        matched_fields = 0
        total_fields = 0

        # Candidate name match
        if extracted.get("candidate_name"):
            total_fields += 1
            if official.candidate_name and extracted["candidate_name"].split()[-1].lower() in official.candidate_name.lower():
                matched_fields += 1

        # District match
        if extracted.get("district"):
            total_fields += 1
            if official.district and extracted["district"].lower() in official.district.lower():
                matched_fields += 1

        # Party match
        if extracted.get("party"):
            total_fields += 1
            if official.party and extracted["party"].lower() in official.party.lower():
                matched_fields += 1

        # Numeric fields contribute to confidence even when conflicting
        if extracted.get("vote_count") is not None:
            total_fields += 1
            if not any(c["field"] == "vote_count" for c in conflicts):
                matched_fields += 1

        if extracted.get("percentage") is not None:
            total_fields += 1
            if not any(c["field"] == "percentage" for c in conflicts):
                matched_fields += 1

        if total_fields == 0:
            return 0.3

        return round(matched_fields / total_fields, 2)
