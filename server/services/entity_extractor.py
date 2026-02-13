import re
from typing import Any


# Known Uganda election entities for supplementary matching
KNOWN_PARTIES = {
    "NRM": "National Resistance Movement",
    "NUP": "National Unity Platform",
    "FDC": "Forum for Democratic Change",
    "DP": "Democratic Party",
    "UPC": "Uganda Peoples Congress",
    "ANT": "Alliance for National Transformation",
    "JEEMA": "Justice Forum",
    "PPP": "People's Progressive Party",
}

KNOWN_DISTRICTS = [
    "Kampala", "Wakiso", "Mukono", "Jinja", "Gulu", "Lira", "Mbale",
    "Soroti", "Arua", "Mbarara", "Kabale", "Fort Portal", "Kabarole",
    "Masaka", "Entebbe", "Hoima", "Kasese", "Tororo", "Iganga", "Bushenyi",
    "Ntungamo", "Luweero", "Mityana", "Mpigi", "Kayunga", "Buikwe",
    "Busia", "Pallisa", "Kumi", "Katakwi", "Moroto", "Kotido",
    "Adjumani", "Moyo", "Nebbi", "Masindi", "Kibaale", "Bundibugyo",
    "Kisoro", "Kanungu", "Rukungiri", "Isingiro", "Kiruhura", "Lyantonde",
    "Rakai", "Kalangala", "Sembabule", "Gomba", "Butambala", "Kiboga",
    "Nakaseke", "Nakasongola", "Kamuli", "Buyende", "Luuka", "Namutumba",
    "Bugiri", "Namayingo", "Mayuge", "Kaliro", "Budaka", "Kibuku",
    "Butaleja", "Sironko", "Bulambuli", "Kapchorwa", "Bukwo", "Kween",
    "Amuria", "Ngora", "Serere", "Kaberamaido", "Amolatar", "Dokolo",
    "Alebtong", "Otuke", "Kole", "Oyam", "Apac", "Kwania", "Pader",
    "Agago", "Kitgum", "Lamwo", "Amuru", "Nwoya", "Omoro", "Zombo",
    "Pakwach", "Buliisa", "Kagadi", "Kakumiro", "Kiryandongo", "Kyankwanzi",
    "National",
]

KNOWN_POSITIONS = [
    "President",
    "Member of Parliament",
    "MP",
    "LC5 Chairman",
    "LC5 Chairperson",
    "Woman Member of Parliament",
    "Woman MP",
    "District Chairman",
    "Mayor",
]

KNOWN_CANDIDATES = {
    "museveni": "Yoweri Kaguta Museveni",
    "yoweri museveni": "Yoweri Kaguta Museveni",
    "kaguta": "Yoweri Kaguta Museveni",
    "m7": "Yoweri Kaguta Museveni",
    "bobi wine": "Robert Kyagulanyi Ssentamu",
    "kyagulanyi": "Robert Kyagulanyi Ssentamu",
    "robert kyagulanyi": "Robert Kyagulanyi Ssentamu",
    "besigye": "Kizza Besigye",
    "kizza besigye": "Kizza Besigye",
    "mugisha muntu": "Mugisha Muntu",
    "muntu": "Mugisha Muntu",
    "patrick amuriat": "Patrick Oboi Amuriat",
    "amuriat": "Patrick Oboi Amuriat",
    "norbert mao": "Norbert Mao",
    "mao": "Norbert Mao",
    "nsereko": "Muhammad Nsereko",
    "muhammad nsereko": "Muhammad Nsereko",
    "nancy kalembe": "Nancy Kalembe",
    "kalembe": "Nancy Kalembe",
    "tumukunde": "Henry Tumukunde",
    "henry tumukunde": "Henry Tumukunde",
    "katumba wamala": "Katumba Wamala",
    "wamala": "Katumba Wamala",
}

RESULT_KEYWORDS = {
    "won", "wins", "winning", "lost", "loses", "losing", "leading",
    "leads", "elected", "defeated", "beat", "beats", "beating",
    "declared", "announced", "garnered", "received", "got", "polled",
}


class EntityExtractor:
    """Extract election-related entities from claim text."""

    def __init__(self, nlp: Any):
        self.nlp = nlp
        self._district_lower = {d.lower(): d for d in KNOWN_DISTRICTS}

    def extract(self, text: str) -> dict:
        doc = self.nlp(text)
        text_lower = text.lower()

        fields: dict = {
            "candidate_name": None,
            "party": None,
            "position": None,
            "district": None,
            "vote_count": None,
            "percentage": None,
            "result_claim": None,
        }

        # ── Candidate name ───────────────────────────────────────────
        # First try known candidate aliases (highest priority)
        for alias, full_name in KNOWN_CANDIDATES.items():
            if alias in text_lower:
                fields["candidate_name"] = full_name
                break

        # Fall back to spaCy PERSON entities
        if not fields["candidate_name"]:
            persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            if persons:
                fields["candidate_name"] = persons[0]

        # ── District / location ──────────────────────────────────────
        # First check known districts
        for d_lower, d_proper in self._district_lower.items():
            if d_lower in text_lower:
                fields["district"] = d_proper
                break

        # Fall back to spaCy GPE entities
        if not fields["district"]:
            gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
            for gpe in gpes:
                if gpe.lower() in self._district_lower:
                    fields["district"] = self._district_lower[gpe.lower()]
                    break

        # Check for "national" / "nationally"
        if not fields["district"] and re.search(
            r"\bnational(?:ly)?\b", text_lower
        ):
            fields["district"] = "National"

        # ── Vote count ───────────────────────────────────────────────
        # Pattern: numbers followed by "votes" or standalone large numbers
        vote_patterns = [
            r"(\d{1,3}(?:,\d{3})+)\s*votes?",
            r"(\d{4,})\s*votes?",
            r"(\d+(?:\.\d+)?)\s*(?:million|m)\s*votes?",
            r"got\s+(\d{1,3}(?:,\d{3})+)",
            r"received\s+(\d{1,3}(?:,\d{3})+)",
            r"polled\s+(\d{1,3}(?:,\d{3})+)",
            r"garnered\s+(\d{1,3}(?:,\d{3})+)",
        ]
        for pattern in vote_patterns:
            match = re.search(pattern, text_lower)
            if match:
                raw = match.group(1).replace(",", "")
                # Handle "million" / "m" suffix
                if "million" in text_lower[match.start() : match.end() + 10] or (
                    raw.replace(".", "").isdigit() and float(raw) < 100
                    and re.search(r"(?:million|m)\s*votes?", text_lower[match.start():])
                ):
                    fields["vote_count"] = int(float(raw) * 1_000_000)
                else:
                    fields["vote_count"] = int(float(raw))
                break

        # ── Percentage ───────────────────────────────────────────────
        pct_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent)", text_lower)
        if pct_match:
            fields["percentage"] = float(pct_match.group(1))

        # ── Party ────────────────────────────────────────────────────
        text_upper = text.upper()
        for abbr in KNOWN_PARTIES:
            # Match as whole word to avoid false positives
            if re.search(rf"\b{abbr}\b", text_upper):
                fields["party"] = abbr
                break

        # ── Position ─────────────────────────────────────────────────
        for pos in KNOWN_POSITIONS:
            if pos.lower() in text_lower:
                fields["position"] = pos
                break

        # Default to presidential if no position detected but a known
        # presidential candidate is mentioned
        if not fields["position"] and fields["candidate_name"]:
            name_lower = fields["candidate_name"].lower()
            presidential_candidates = {
                "yoweri kaguta museveni", "robert kyagulanyi ssentamu",
                "kizza besigye", "mugisha muntu", "patrick oboi amuriat",
                "nancy kalembe", "henry tumukunde", "katumba wamala",
                "norbert mao",
            }
            if name_lower in presidential_candidates:
                fields["position"] = "President"

        # ── Result claim keyword ─────────────────────────────────────
        for keyword in RESULT_KEYWORDS:
            if re.search(rf"\b{keyword}\b", text_lower):
                fields["result_claim"] = keyword
                break

        return fields
