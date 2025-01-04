from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.core.services.plan_service import TherapyPlanGenerator
from app.core.models.schemas import PatientInput, TherapyPlan
from app.core.utils.exceptions import NoMatchingConditionsError

app = FastAPI(
    title="Mariposa",
    description="AI-powered therapy plan optimization system",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Mariposa API"}

@app.post("/api/v1/plans/generate", response_model=TherapyPlan)
async def generate_plan(patient_input: PatientInput):
    try:
        planner = TherapyPlanGenerator()
        therapy_plan = planner.generate_therapy_plan(patient_input)
        return therapy_plan
    except NoMatchingConditionsError as e:
        raise HTTPException(status_code=400, detail={
            "message": str(e),
            "suggestions": e.suggestions
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 