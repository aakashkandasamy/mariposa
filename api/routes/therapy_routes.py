from fastapi import APIRouter, HTTPException
from core.models.schemas import PatientInput, TherapyPlan
from core.services.plan_service import generate_therapy_plan

router = APIRouter()

@router.post("/plans/generate", response_model=TherapyPlan)
async def generate_plan(patient_input: PatientInput):
    try:
        therapy_plan = generate_therapy_plan(patient_input)
        return therapy_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 