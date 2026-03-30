"""
Terra 2.0 — Authentication Module
Uses bcrypt for secure password hashing with SQLAlchemy 2.0 patterns.
"""

from datetime import datetime

import bcrypt
from sqlalchemy import select

from config import XP_PER_LEVEL, LEVEL_NAMES
from database.db_setup import get_engine, get_session, User


class AuthManager:
    """Handles user registration, login, and XP updates."""

    @staticmethod
    def register(username: str, email: str, password: str,
                 college: str, role: str = "student") -> dict:
        """
        Register a new user.
        Returns {"success": True, "user_id": int} or
                {"success": False, "error": str}.
        """
        engine = get_engine()
        with get_session(engine) as session:
            # Check unique username
            existing_user = session.execute(
                select(User).where(User.username == username.strip())
            ).scalar_one_or_none()
            if existing_user is not None:
                return {"success": False, "error": "Username already taken."}

            # Check unique email
            existing_email = session.execute(
                select(User).where(User.email == email.strip().lower())
            ).scalar_one_or_none()
            if existing_email is not None:
                return {"success": False, "error": "Email already registered."}

            # Hash password with bcrypt
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(
                password.encode("utf-8"), salt
            ).decode("utf-8")

            new_user = User(
                username=username.strip(),
                email=email.strip().lower(),
                password_hash=password_hash,
                college=college.strip(),
                role=role,
                xp=0,
                level=1,
                streak=0,
                last_login=datetime.utcnow(),
                avatar_seed=username.strip(),
                created_at=datetime.utcnow(),
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return {"success": True, "user_id": new_user.id}

    @staticmethod
    def login(username: str, password: str) -> dict | None:
        """
        Authenticate user. Returns user dict on success, None on failure.
        """
        engine = get_engine()
        with get_session(engine) as session:
            user = session.execute(
                select(User).where(User.username == username.strip())
            ).scalar_one_or_none()

            if user is None:
                return None

            # Verify password
            if not bcrypt.checkpw(
                password.encode("utf-8"),
                user.password_hash.encode("utf-8")
            ):
                return None

            # Update last login and streak
            now = datetime.utcnow()
            if user.last_login is not None:
                days_diff = (now - user.last_login).days
                if days_diff == 1:
                    user.streak += 1
                elif days_diff > 1:
                    user.streak = 1
                # If same day, streak stays the same
            else:
                user.streak = 1

            user.last_login = now
            session.commit()

            return {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "college": user.college,
                "role": user.role,
                "xp": user.xp,
                "level": user.level,
                "streak": user.streak,
                "avatar_seed": user.avatar_seed,
                "created_at": user.created_at.isoformat() if user.created_at else "",
            }

    @staticmethod
    def get_user(user_id: int) -> dict | None:
        """Fetch user by ID. Returns user dict or None."""
        engine = get_engine()
        with get_session(engine) as session:
            user = session.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()

            if user is None:
                return None

            return {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "college": user.college,
                "role": user.role,
                "xp": user.xp,
                "level": user.level,
                "streak": user.streak,
                "avatar_seed": user.avatar_seed or user.username,
                "last_login": user.last_login.isoformat() if user.last_login else "",
                "created_at": user.created_at.isoformat() if user.created_at else "",
            }

    @staticmethod
    def update_xp(user_id: int, xp_to_add: int) -> dict:
        """
        Add XP to user and recalculate level.
        Returns {"new_xp": int, "new_level": int,
                 "leveled_up": bool, "level_name": str}.
        """
        engine = get_engine()
        with get_session(engine) as session:
            user = session.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()

            if user is None:
                return {
                    "new_xp": 0,
                    "new_level": 1,
                    "leveled_up": False,
                    "level_name": LEVEL_NAMES[0],
                }

            old_level = user.level
            user.xp += xp_to_add
            new_level = min(user.xp // XP_PER_LEVEL + 1, 30)
            user.level = new_level
            session.commit()

            leveled_up = new_level > old_level
            level_name = LEVEL_NAMES[new_level - 1] if new_level <= 30 else LEVEL_NAMES[29]

            return {
                "new_xp": user.xp,
                "new_level": new_level,
                "leveled_up": leveled_up,
                "level_name": level_name,
            }
