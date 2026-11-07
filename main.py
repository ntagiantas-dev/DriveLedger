"""
does4u-fleet — FastAPI backend για το fleet tracker.
"""
import logging
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import DriverReport, get_db, init_db

logger = logging.getLogger("does4u-fleet")
logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="Does4U Fleet Tracker",
    description="Backend API για αναφορές οδηγών",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    logger.info("Database initialized (fleet.db)")


# ============================================
# SCHEMAS
# ============================================
class DriverReportIn(BaseModel):
    route_id: str = Field(..., min_length=1, max_length=20)
    date: str = Field(..., description="YYYY-MM-DD")
    shift_start: Optional[str] = None
    shift_finish: Optional[str] = None
    km_start: Optional[float] = None
    km_finish: Optional[float] = None
    pickup_count: Optional[int] = None
    delivery_count: Optional[int] = None


class DriverReportOut(BaseModel):
    id: int
    route_id: str
    date: str
    shift_start: Optional[str] = None
    shift_finish: Optional[str] = None
    km_start: Optional[float] = None
    km_finish: Optional[float] = None
    pickup_count: Optional[int] = None
    delivery_count: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# ============================================
# STATIC FILES / PAGES
# ============================================
@app.get("/", include_in_schema=False)
async def serve_index():
    """Σερβίρει το HTML του οδηγού (tracker)."""
    return FileResponse("static/does4u-daily-tracker.html")


@app.get("/director", include_in_schema=False)
async def serve_director():
    """Σερβίρει το Dashboard του Διευθυντή (desktop)."""
    return FileResponse("static/director.html")


@app.get("/manifest.json", include_in_schema=False)
async def serve_manifest():
    return FileResponse(
        "static/manifest.json",
        media_type="application/manifest+json",
    )


@app.get("/sw.js", include_in_schema=False)
async def serve_sw():
    return FileResponse(
        "static/sw.js",
        media_type="application/javascript",
    )


# ============================================
# API ENDPOINTS
# ============================================
@app.post("/api/sync")
async def sync_report(
    payload: DriverReportIn,
    db: Session = Depends(get_db),
):
    """Upsert αναφοράς — αν υπάρχει (route_id, date) → update, αλλιώς insert."""
    existing = (
        db.query(DriverReport)
        .filter(
            DriverReport.route_id == payload.route_id,
            DriverReport.date == payload.date,
        )
        .first()
    )

    if existing:
        existing.shift_start = payload.shift_start
        existing.shift_finish = payload.shift_finish
        existing.km_start = payload.km_start
        existing.km_finish = payload.km_finish
        existing.pickup_count = payload.pickup_count
        existing.delivery_count = payload.delivery_count
        action = "updated"
    else:
        new_report = DriverReport(
            route_id=payload.route_id,
            date=payload.date,
            shift_start=payload.shift_start,
            shift_finish=payload.shift_finish,
            km_start=payload.km_start,
            km_finish=payload.km_finish,
            pickup_count=payload.pickup_count,
            delivery_count=payload.delivery_count,
        )
        db.add(new_report)
        action = "created"

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.exception("DB commit failed: %s", exc)
        raise HTTPException(status_code=500, detail="Database error") from exc

    logger.info(
        "Report %s: route=%s date=%s",
        action,
        payload.route_id,
        payload.date,
    )

    return {"status": "success", "action": action}


@app.get("/api/reports")
async def list_reports(db: Session = Depends(get_db)):
    """Επιστρέφει όλες τις αναφορές (για το director dashboard)."""
    rows = (
        db.query(DriverReport)
        .order_by(DriverReport.date.desc(), DriverReport.route_id.asc())
        .all()
    )
    result = []
    for r in rows:
        result.append({
            "id": r.id,
            "route_id": r.route_id,
            "date": r.date,
            "shift_start": r.shift_start,
            "shift_finish": r.shift_finish,
            "km_start": r.km_start,
            "km_finish": r.km_finish,
            "pickup_count": r.pickup_count,
            "delivery_count": r.delivery_count,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        })
    return result


# ============================================
# STATIC ASSETS (πρέπει να είναι ΤΕΛΕΥΤΑΙΟ)
# ============================================
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)