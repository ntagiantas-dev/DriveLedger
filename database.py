"""
Database setup για το does4u-fleet.

Χρήση SQLAlchemy 2.x + SQLite.
Το αρχείο της βάσης (fleet.db) δημιουργείται αυτόματα στο ίδιο folder.
"""
from datetime import datetime, timezone
from typing import Generator

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# ============================================
# ΡΥΘΜΙΣΕΙΣ
# ============================================
# SQLite file: ./fleet.db (δημιουργείται αυτόματα)
DATABASE_URL = "sqlite:///./fleet.db"

# check_same_thread=False απαραίτητο για SQLite + FastAPI (πολλαπλά threads)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============================================
# BASE
# ============================================
class Base(DeclarativeBase):
    """Base class για όλα τα models."""
    pass


# ============================================
# MODEL: DriverReport
# ============================================
class DriverReport(Base):
    """Αναφορά ημέρας από οδηγό.

    Ένα record ανά (route_id, date). Αν ο ίδιος οδηγός στείλει ξανά για
    την ίδια ημέρα, το POST /api/sync κάνει update αντί insert.
    """

    __tablename__ = "driver_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Ταυτοποίηση
    route_id = Column(String, nullable=False, index=True)   # π.χ. "071"
    date = Column(String, nullable=False, index=True)       # "YYYY-MM-DD"

    # Ώρες
    shift_start = Column(String, nullable=True)             # "08:30"
    shift_finish = Column(String, nullable=True)            # "17:45"

    # Χιλιόμετρα
    km_start = Column(Float, nullable=True)
    km_finish = Column(Float, nullable=True)

    # Δέματα
    pickup_count = Column(Integer, nullable=True)
    delivery_count = Column(Integer, nullable=True)

    # Timestamps — server-side defaults
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# ============================================
# HELPERS
# ============================================
def init_db() -> None:
    """Δημιουργία όλων των tables (αν δεν υπάρχουν)."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — δίνει Session και το κλείνει στο τέλος."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()