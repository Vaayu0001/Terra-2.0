"""
Terra 2.0 — College Leaderboard Module
Tracks and ranks colleges by total XP and average footprint.
"""

from datetime import datetime

import pandas as pd
from sqlalchemy import select, func

from database.db_setup import (
    get_engine, get_session,
    CollegeLeaderboard as CollegeLeaderboardModel, User, FootprintLog
)


class CollegeLeaderboard:
    """Manages inter-college XP rankings."""

    @staticmethod
    def update_college(college: str, xp: int, footprint: float) -> None:
        """
        Upsert college stats — recalculate totals from user data.
        """
        engine = get_engine()
        with get_session(engine) as session:
            # Get aggregate stats from users
            user_stats = session.execute(
                select(
                    func.sum(User.xp).label("total_xp"),
                    func.count(User.id).label("member_count")
                ).where(User.college == college)
            ).first()

            total_xp = user_stats.total_xp or 0
            member_count = user_stats.member_count or 0

            # Get average footprint for college
            avg_fp = session.execute(
                select(func.avg(FootprintLog.total_kg)).where(
                    FootprintLog.user_id.in_(
                        select(User.id).where(User.college == college)
                    )
                )
            ).scalar() or 0.0

            # Upsert
            existing = session.execute(
                select(CollegeLeaderboardModel).where(
                    CollegeLeaderboardModel.college_name == college
                )
            ).scalar_one_or_none()

            if existing:
                existing.total_xp = total_xp
                existing.avg_footprint = round(avg_fp, 2)
                existing.member_count = member_count
                existing.updated_at = datetime.utcnow()
            else:
                new_entry = CollegeLeaderboardModel(
                    college_name=college,
                    total_xp=total_xp,
                    avg_footprint=round(avg_fp, 2),
                    member_count=member_count,
                    updated_at=datetime.utcnow(),
                )
                session.add(new_entry)

            session.commit()

    @staticmethod
    def get_rankings() -> pd.DataFrame:
        """
        Get all college rankings sorted by total XP desc.
        Returns DataFrame: rank, college_name, total_xp,
                           avg_footprint, member_count
        """
        engine = get_engine()
        with get_session(engine) as session:
            entries = session.execute(
                select(CollegeLeaderboardModel)
                .order_by(CollegeLeaderboardModel.total_xp.desc())
            ).scalars().all()

            if not entries:
                return pd.DataFrame(columns=[
                    "rank", "college_name", "total_xp",
                    "avg_footprint", "member_count"
                ])

            data = []
            for i, entry in enumerate(entries, 1):
                data.append({
                    "rank": i,
                    "college_name": entry.college_name,
                    "total_xp": entry.total_xp,
                    "avg_footprint": entry.avg_footprint,
                    "member_count": entry.member_count,
                })

            return pd.DataFrame(data)

    @staticmethod
    def get_user_college_rank(college: str) -> int:
        """Get rank position for a specific college (1-indexed)."""
        engine = get_engine()
        with get_session(engine) as session:
            entries = session.execute(
                select(CollegeLeaderboardModel)
                .order_by(CollegeLeaderboardModel.total_xp.desc())
            ).scalars().all()

            for i, entry in enumerate(entries, 1):
                if entry.college_name == college:
                    return i

            return 0  # Not ranked yet
