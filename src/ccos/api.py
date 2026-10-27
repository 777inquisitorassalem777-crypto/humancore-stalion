from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .kernel import CCOSKernel

app = FastAPI(title="CCOS-Ω Research Core", version="0.1.0",
              description="Persistent narrative agent research prototype; no consciousness claim.")
kernel = CCOSKernel()

class ProcessInput(BaseModel):
    text: str = Field(min_length=1, max_length=20000)

class RememberInput(BaseModel):
    text: str = Field(min_length=1, max_length=20000)
    importance: float = Field(default=0.5, ge=0, le=1)
    emotion: float = Field(default=0.0, ge=-1, le=1)
    participants: list[str] = []
    impact_on_values: dict[str, float] = {}
    interpretation: str = ""

class PlanInput(BaseModel):
    goal: str = Field(min_length=1, max_length=4000)

class ReflectInput(BaseModel):
    question: str = Field(min_length=1, max_length=4000)

@app.get("/")
def root():
    return {"name": "CCOS-Ω", "version": "0.1.0", "status": "prototype"}

@app.post("/process")
def process(payload: ProcessInput):
    return kernel.process(payload.text)

@app.post("/remember")
def remember(payload: RememberInput):
    return kernel.remember(payload.text, payload.importance, payload.emotion,
                           payload.participants, payload.impact_on_values, payload.interpretation)

@app.get("/status")
def status():
    return kernel.status()

@app.get("/identity")
def identity():
    return kernel.identity.snapshot()

@app.get("/biography")
def biography():
    return kernel.biography()

@app.post("/plan")
def plan(payload: PlanInput):
    return kernel.plan_for(payload.goal)

@app.post("/reflect")
def reflect(payload: ReflectInput):
    return kernel.reflect(payload.question)
