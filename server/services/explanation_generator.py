from typing import Any, Optional

from server.models.enums import AlignmentStatus


class ExplanationGenerator:
    """Generate human-readable explanations from match results."""

    def generate(
        self,
        alignment: AlignmentStatus,
        extracted: dict,
        official_result: Optional[Any],
        conflicts: list,
    ) -> str:
        if alignment == AlignmentStatus.MATCHES:
            return self._matches(extracted, official_result)
        elif alignment == AlignmentStatus.CONFLICTS:
            return self._conflicts(extracted, official_result, conflicts)
        elif alignment == AlignmentStatus.NO_OFFICIAL_DATA:
            return self._no_data(extracted)
        elif alignment == AlignmentStatus.CANNOT_VERIFY:
            return self._cannot_verify(extracted)
        else:
            return "Official Electoral Commission data has been updated since this claim was last checked."

    def _matches(self, extracted: dict, official: Any) -> str:
        candidate = extracted.get("candidate_name") or "the mentioned candidate"
        district = extracted.get("district") or "the specified area"

        parts = [
            f"The claim about {candidate} in {district} aligns with official Electoral Commission data."
        ]

        if extracted.get("vote_count") and official and official.vote_count:
            parts.append(
                f"The stated vote count of {extracted['vote_count']:,} matches "
                f"the official count of {official.vote_count:,}."
            )

        if extracted.get("percentage") and official and official.percentage:
            parts.append(
                f"The stated percentage of {extracted['percentage']}% matches "
                f"the official figure of {official.percentage}%."
            )

        return " ".join(parts)

    def _conflicts(self, extracted: dict, official: Any, conflicts: list) -> str:
        candidate = extracted.get("candidate_name") or "the mentioned candidate"
        district = extracted.get("district") or "the specified area"

        parts = [
            f"The claim about {candidate} in {district} has been checked "
            f"against official Electoral Commission data and contains discrepancies."
        ]

        for conflict in conflicts:
            if conflict["field"] == "vote_count":
                parts.append(
                    f"The claimed vote count of {conflict['claimed']:,} does not match "
                    f"the official count of {conflict['official']:,}."
                )
            elif conflict["field"] == "percentage":
                parts.append(
                    f"The claimed percentage of {conflict['claimed']}% does not match "
                    f"the official figure of {conflict['official']}%."
                )
            elif conflict["field"] == "result_claim":
                parts.append(
                    f"The claim states the candidate \"{conflict['claimed']}\" but "
                    f"official records indicate: {conflict['official']}."
                )

        return " ".join(parts)

    def _no_data(self, extracted: dict) -> str:
        candidate = extracted.get("candidate_name") or "the mentioned candidate"
        district = extracted.get("district") or "the specified area"

        return (
            f"No official Electoral Commission data was found matching a claim "
            f"about {candidate} in {district}. This may mean results have not "
            f"been announced yet, or the claim references data we haven't collected."
        )

    def _cannot_verify(self, extracted: dict) -> str:
        detected = [k for k, v in extracted.items() if v is not None]
        if not detected:
            return (
                "We could not extract any verifiable election claim from the "
                "submitted text. Please include specific details like candidate "
                "names, vote counts, or constituencies."
            )

        return (
            f"We extracted limited information ({', '.join(detected)}) but not "
            f"enough to make a meaningful comparison against official records. "
            f"Try including more specifics like candidate names, vote counts, "
            f"or district names."
        )
