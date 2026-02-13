from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class OfficialSource(Base):
    __tablename__ = "official_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    url = Column(String(512), nullable=True)
    description = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=True)
    last_scraped = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    results = relationship("ElectionResult", back_populates="source")


class ElectionResult(Base):
    __tablename__ = "election_results"
    __table_args__ = (
        Index("ix_election_results_candidate_district", "candidate_name", "district"),
        Index("ix_election_results_district", "district"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer, ForeignKey("official_sources.id"), nullable=False)
    election_level = Column(String(50), nullable=False)
    election_year = Column(Integer, nullable=False)
    district = Column(String(255), nullable=False)
    constituency = Column(String(255), nullable=True)
    polling_station = Column(String(255), nullable=True)
    position = Column(String(255), nullable=False)
    candidate_name = Column(String(255), nullable=False)
    party = Column(String(255), nullable=True)
    vote_count = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=True)
    total_valid_votes = Column(Integer, nullable=True)
    is_winner = Column(Integer, default=0)
    last_updated = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())

    source = relationship("OfficialSource", back_populates="results")


class ClaimVerification(Base):
    __tablename__ = "claim_verifications"
    __table_args__ = (Index("ix_claim_verifications_expires_at", "expires_at"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_text = Column(Text, nullable=False)
    claim_type = Column(String(50), nullable=False)
    extracted_text = Column(Text, nullable=True)
    extracted_fields = Column(JSONB, nullable=True)
    matched_result_id = Column(
        Integer, ForeignKey("election_results.id"), nullable=True
    )
    alignment_status = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    explanation = Column(Text, nullable=True)
    ip_hash = Column(String(64), nullable=True)
    verified_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
