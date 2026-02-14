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
    "UPDF": "Uganda Peoples' Defence Forces",
    "RPP": "Revolutionary People's Party",
    "NPP": "National Peasants Party",
    "CMP": "Common Man's Party",
    "CP": "Conservative Party",
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
    "National", "UPDF", "Nakawa", "Obongi", "Kampala Central",
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
    "UPDF Male Representative to Parliament",
    "UPDF Female Representative to Parliament",
    "UPDF Representative",
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
    "mugisha muntu": "Gregory Mugisha Muntu Oyera",
    "muntu": "Gregory Mugisha Muntu Oyera",
    "nandala mafabi": "James Nathan Nandala Mafabi",
    "mafabi": "James Nathan Nandala Mafabi",
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
    "ssenyonyi": "Joel Ssenyonyi",
    "joel ssenyonyi": "Joel Ssenyonyi",
    "okidling sam": "Okidling SAM",
    "okidling": "Okidling SAM",
    "mugira james": "Mugira James",
    "mugira": "Mugira James",
    "kavuma samuel": "Kavuma Samuel",
    "meeme sylivia": "Meeme Sylivia",
    "meeme": "Meeme Sylivia",
    "ikiriza knight": "Ikiriza Knight",
    "minsa kabanda": "Hajjat Minsa Kabanda",
    "rubongoya": "David Lewis Rubongoya",
}

RESULT_KEYWORDS = {
    "won", "wins", "winning", "lost", "loses", "losing", "leading",
    "leads", "elected", "defeated", "beat", "beats", "beating",
    "declared", "announced", "garnered", "received", "got", "polled",
}

# ── Fallback regex patterns for when NER fails ──────────────────────
# These catch the most common claim structures directly
FALLBACK_NAME_PATTERNS = [
    # "Name received/got/polled/garnered N votes"
    r"([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)+)\s+(?:received|got|polled|garnered|won\s+with)\s+\d+",
    # "Name won the X seat/election"
    r"([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)+)\s+(?:won|wins|lost|elected)",
    # "Name (PARTY) received"
    r"([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)+)\s*\([A-Z]+\)",
]

FALLBACK_VOTE_PATTERNS = [
    # "received/got/polled/garnered 340 votes" or just "received 340"
    r"(?:received|got|polled|garnered)\s+(\d+)\s*(?:votes?)?",
    # "340 votes" (any number)
    r"(\d+)\s+votes?\b",
    # "won with 340 votes"
    r"won\s+with\s+(\d+)\s*(?:votes?)?",
]

ELECTION_CONTEXT_PATTERNS = [
    (r"\bupdf\b", "UPDF"),
    (r"\bpresidential\b", "presidential"),
    (r"\bparliamentary\b", "parliamentary"),
    (r"\bwoman\s+mp\b", "woman_mp"),
    (r"\bwoman\s+member\b", "woman_mp"),
]


class EntityExtractor:
    """Extract election-related entities from claim text."""

    def __init__(self, nlp: Any):
        self.nlp = nlp
        # Sort longest-first so "Kampala Central" matches before "Kampala"
        sorted_districts = sorted(KNOWN_DISTRICTS, key=len, reverse=True)
        self._district_lower = {d.lower(): d for d in sorted_districts}

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
        # 1. Known candidate aliases (highest priority)
        for alias, full_name in KNOWN_CANDIDATES.items():
            if alias in text_lower:
                fields["candidate_name"] = full_name
                break

        # 2. spaCy PERSON entities
        if not fields["candidate_name"]:
            persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            if persons:
                fields["candidate_name"] = persons[0]

        # 3. Fallback: regex patterns for names before action verbs
        if not fields["candidate_name"]:
            for pattern in FALLBACK_NAME_PATTERNS:
                match = re.search(pattern, text)
                if match:
                    fields["candidate_name"] = match.group(1).strip()
                    break

        # ── Vote count ───────────────────────────────────────────────
        # Try structured patterns first, then fallback
        vote_patterns = [
            r"(\d{1,3}(?:,\d{3})+)\s*votes?",
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
                if "million" in text_lower[match.start():match.end() + 10] or (
                    raw.replace(".", "").isdigit() and float(raw) < 100
                    and re.search(r"(?:million|m)\s*votes?", text_lower[match.start():])
                ):
                    fields["vote_count"] = int(float(raw) * 1_000_000)
                else:
                    fields["vote_count"] = int(float(raw))
                break

        # Fallback: simpler patterns that catch any digit count
        if fields["vote_count"] is None:
            for pattern in FALLBACK_VOTE_PATTERNS:
                match = re.search(pattern, text_lower)
                if match:
                    raw = match.group(1).replace(",", "")
                    try:
                        fields["vote_count"] = int(raw)
                        break
                    except ValueError:
                        pass

        # ── Percentage ───────────────────────────────────────────────
        pct_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent)", text_lower)
        if pct_match:
            fields["percentage"] = float(pct_match.group(1))

        # ── Party ────────────────────────────────────────────────────
        text_upper = text.upper()
        for abbr in KNOWN_PARTIES:
            if re.search(rf"\b{abbr}\b", text_upper):
                fields["party"] = abbr
                break

        # ── District / location ──────────────────────────────────────
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

        # ── Election context → district/position mapping ─────────────
        for pattern, context in ELECTION_CONTEXT_PATTERNS:
            if re.search(pattern, text_lower):
                if context == "UPDF":
                    if not fields["district"]:
                        fields["district"] = "UPDF"
                    if not fields["position"]:
                        fields["position"] = "UPDF Male Representative to Parliament"
                        # Refine if "female" or "woman" mentioned
                        if re.search(r"\b(?:female|woman|women)\b", text_lower):
                            fields["position"] = "UPDF Female Representative to Parliament"
                elif context == "presidential":
                    if not fields["position"]:
                        fields["position"] = "President"
                elif context == "parliamentary":
                    if not fields["position"]:
                        fields["position"] = "Member of Parliament"
                elif context == "woman_mp":
                    if not fields["position"]:
                        fields["position"] = "Woman Member of Parliament"
                break

        # ── Position ─────────────────────────────────────────────────
        if not fields["position"]:
            for pos in KNOWN_POSITIONS:
                if pos.lower() in text_lower:
                    fields["position"] = pos
                    break

        # Default to presidential if known presidential candidate
        if not fields["position"] and fields["candidate_name"]:
            name_lower = fields["candidate_name"].lower()
            presidential_candidates = {
                "yoweri kaguta museveni", "robert kyagulanyi ssentamu",
                "kizza besigye", "gregory mugisha muntu oyera",
                "james nathan nandala mafabi",
                "patrick oboi amuriat", "nancy kalembe",
                "henry tumukunde", "katumba wamala", "norbert mao",
            }
            if name_lower in presidential_candidates:
                fields["position"] = "President"

        # Presidential → district defaults to "National"
        if fields["position"] == "President" and not fields["district"]:
            fields["district"] = "National"

        # ── Result claim keyword ─────────────────────────────────────
        for keyword in RESULT_KEYWORDS:
            if re.search(rf"\b{keyword}\b", text_lower):
                fields["result_claim"] = keyword
                break

        return fields
