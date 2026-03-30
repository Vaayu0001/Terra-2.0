"""
Terra 2.0 Database Setup
SQLAlchemy 2.0 style with declarative_base, all 8 models.
"""

from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text,
    ForeignKey, create_engine, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship, Session

from config import DB_URL

Base = declarative_base()


def _utcnow():
    """Return naive UTC datetime for SQLite compatibility."""
    return datetime.utcnow()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    college = Column(String(200), nullable=False)
    role = Column(String(50), default="student")
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak = Column(Integer, default=0)
    last_login = Column(DateTime, nullable=True)
    avatar_seed = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    footprint_logs = relationship("FootprintLog", back_populates="user", lazy="dynamic")
    swipe_scores = relationship("SwipeScore", back_populates="user", lazy="dynamic")
    achievements = relationship("Achievement", back_populates="user", lazy="dynamic")
    meme_logs = relationship("MemeLog", back_populates="user", lazy="dynamic")
    eco_searches = relationship("EcoSearch", back_populates="user", lazy="dynamic")
    waste_logs = relationship("WasteLog", back_populates="user", lazy="dynamic")


class FootprintLog(Base):
    __tablename__ = "footprint_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(DateTime, default=_utcnow)
    transport_kg = Column(Float, default=0.0)
    food_kg = Column(Float, default=0.0)
    energy_kg = Column(Float, default=0.0)
    shopping_kg = Column(Float, default=0.0)
    total_kg = Column(Float, default=0.0)
    created_at = Column(DateTime, default=_utcnow)

    user = relationship("User", back_populates="footprint_logs")


class SwipeScore(Base):
    __tablename__ = "swipe_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    score = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    total_rounds = Column(Integer, default=10)
    xp_earned = Column(Integer, default=0)
    played_at = Column(DateTime, default=_utcnow)

    user = relationship("User", back_populates="swipe_scores")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    badge_name = Column(String(100), nullable=False)
    badge_icon = Column(String(10), default="🏅")
    earned_at = Column(DateTime, default=_utcnow)

    user = relationship("User", back_populates="achievements")


class MemeLog(Base):
    __tablename__ = "meme_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    template_name = Column(String(100), nullable=False)
    top_text = Column(Text, default="")
    bottom_text = Column(Text, default="")
    created_at = Column(DateTime, default=_utcnow)

    user = relationship("User", back_populates="meme_logs")


class EcoSearch(Base):
    __tablename__ = "eco_searches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_name = Column(String(200), nullable=False)
    eco_score = Column(Integer, default=0)
    searched_at = Column(DateTime, default=_utcnow)

    user = relationship("User", back_populates="eco_searches")


class WasteLog(Base):
    __tablename__ = "waste_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    item_name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    logged_at = Column(DateTime, default=_utcnow)

    user = relationship("User", back_populates="waste_logs")


class CollegeLeaderboard(Base):
    __tablename__ = "college_leaderboard"

    id = Column(Integer, primary_key=True, autoincrement=True)
    college_name = Column(String(200), unique=True, nullable=False, index=True)
    total_xp = Column(Integer, default=0)
    avg_footprint = Column(Float, default=0.0)
    member_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=_utcnow)


# ---------------------------------------------------------------------------
# Engine and session helpers
# ---------------------------------------------------------------------------

_engine = None


def get_engine():
    """Get or create the SQLAlchemy engine (singleton)."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            DB_URL,
            connect_args={"check_same_thread": False},
            echo=False,
        )
    return _engine


def init_db(engine=None):
    """Create all tables if they don't exist."""
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(bind=engine)


def get_session(engine=None):
    """Return a new Session bound to the engine."""
    if engine is None:
        engine = get_engine()
    return Session(engine)
