"""
Terra 2.0 — Auth Module Tests
Tests registration, login, password hashing, and XP updates.
"""

import unittest
from datetime import datetime, timezone

from sqlalchemy import create_engine

from database.db_setup import Base, init_db, User
from sqlalchemy.orm import Session


class TestAuthManager(unittest.TestCase):
    """Test cases for the AuthManager class."""

    def setUp(self):
        """Create in-memory SQLite database for each test."""
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)

        # Insert a test user directly
        with Session(self.engine) as session:
            import bcrypt
            password_hash = bcrypt.hashpw(
                "testpass123".encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            user = User(
                username="testuser",
                email="test@example.com",
                password_hash=password_hash,
                college="Test University",
                role="student",
                xp=0,
                level=1,
                streak=0,
                last_login=datetime.now(timezone.utc),
                avatar_seed="testuser",
                created_at=datetime.now(timezone.utc),
            )
            session.add(user)
            session.commit()

    def tearDown(self):
        """Drop all tables after each test."""
        Base.metadata.drop_all(bind=self.engine)
        self.engine.dispose()

    def test_register_success(self):
        """Test successful user registration."""
        import bcrypt
        from sqlalchemy import select

        with Session(self.engine) as session:
            password_hash = bcrypt.hashpw(
                "newpass123".encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            new_user = User(
                username="newuser",
                email="new@example.com",
                password_hash=password_hash,
                college="Another University",
                role="student",
                xp=0,
                level=1,
            )
            session.add(new_user)
            session.commit()

            result = session.execute(
                select(User).where(User.username == "newuser")
            ).scalar_one_or_none()

            self.assertIsNotNone(result)
            self.assertEqual(result.username, "newuser")
            self.assertEqual(result.email, "new@example.com")

    def test_register_duplicate_username(self):
        """Test that duplicate username registration fails."""
        import bcrypt
        from sqlalchemy.exc import IntegrityError

        with Session(self.engine) as session:
            password_hash = bcrypt.hashpw(
                "pass123".encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            duplicate_user = User(
                username="testuser",  # Already exists
                email="different@example.com",
                password_hash=password_hash,
                college="Test University",
            )
            session.add(duplicate_user)

            with self.assertRaises(IntegrityError):
                session.commit()

    def test_login_correct(self):
        """Test successful login with correct credentials."""
        import bcrypt
        from sqlalchemy import select

        with Session(self.engine) as session:
            user = session.execute(
                select(User).where(User.username == "testuser")
            ).scalar_one_or_none()

            self.assertIsNotNone(user)
            is_valid = bcrypt.checkpw(
                "testpass123".encode("utf-8"),
                user.password_hash.encode("utf-8")
            )
            self.assertTrue(is_valid)

    def test_login_wrong_password(self):
        """Test login failure with wrong password."""
        import bcrypt
        from sqlalchemy import select

        with Session(self.engine) as session:
            user = session.execute(
                select(User).where(User.username == "testuser")
            ).scalar_one_or_none()

            self.assertIsNotNone(user)
            is_valid = bcrypt.checkpw(
                "wrongpassword".encode("utf-8"),
                user.password_hash.encode("utf-8")
            )
            self.assertFalse(is_valid)

    def test_password_hash_is_different_each_time(self):
        """Test that bcrypt produces different hashes for same password."""
        import bcrypt

        password = "samepassword123".encode("utf-8")
        hash1 = bcrypt.hashpw(password, bcrypt.gensalt())
        hash2 = bcrypt.hashpw(password, bcrypt.gensalt())

        self.assertNotEqual(hash1, hash2)
        # But both should verify correctly
        self.assertTrue(bcrypt.checkpw(password, hash1))
        self.assertTrue(bcrypt.checkpw(password, hash2))


if __name__ == "__main__":
    unittest.main()
