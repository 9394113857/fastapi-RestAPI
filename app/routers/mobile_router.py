from fastapi import APIRouter
from app.services.mobile_service import get_all_mobiles, add_mobile

router = APIRouter()

@router.get("/mobiles")
def get_mobiles():
    return get_all_mobiles()

@router.post("/mobiles")
def create_mobile(data: dict):
    add_mobile(data)
    return {"message": "created"}