from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Trip, User
from ..schemas import TripRequest, TripResponse
from ..dependencies import get_current_user
from ..services.ai_services import generate_trip_plan

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)


@router.post("/plan", response_model=TripResponse)
def create_trip(request: TripRequest,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    try:
      generated_plan = generate_trip_plan(
        request.destination,
        request.days,
        request.interests
        )
    except RuntimeError as error:
        raise HTTPException(status_code=503,detail=str(error))
  
    new_trip = Trip(
        destination=request.destination,
        days=request.days,
        interests=request.interests,
        generated_plan=generated_plan,
        user_id=current_user.id 
        )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return new_trip


@router.get("/", response_model=list[TripResponse])
def get_my_trips(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(Trip).filter(Trip.user_id == current_user.id).all()


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.id == trip_id,Trip.user_id == current_user.id).first()

    if not trip:
        raise HTTPException(status_code=404,detail="Trip not found")

    return trip


@router.delete("/{trip_id}")
def delete_trip(trip_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    trip = db.query(Trip).filter(Trip.id == trip_id,Trip.user_id == current_user.id).first()

    if not trip:
        raise HTTPException(status_code=404,detail="Trip not found")

    db.delete(trip)
    db.commit()

    return {"message": "Trip deleted successfully"}