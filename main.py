from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
import json
app = FastAPI()

class Patient(BaseModel):
    name: Annotated[str, Field(..., description="The Name of the patient", example="Asad Khan")]
    age: Annotated[int, Field(..., description="The Age of the patient", example=30)]
    city: Annotated[str, Field(..., description="The City of the patient", example="New York")]
    gender: Annotated[str, Field(..., description="The Gender of the patient", example="Male")]
    height: Annotated[float, Field(..., description="The Height of the patient in meters", example=1.75)]
    weight: Annotated[float, Field(..., description="The Weight of the patient in kilograms", example=70.5)]

def data_load():
    with open("patient.json", "r") as file:
        return json.load(file)
@computed_field
@property
def bmi(self) -> float:
    return self.weight / (self.height ** 2)

@computed_field
@property
def verdict(self) -> str:
    bmi_value = self.bmi
    if bmi_value < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_value < 24.9:
        return "Normal weight"
    elif 25 <= bmi_value < 29.9:
        return "Overweight"
    else:
        return "Obesity"

@app.get("/")
def hello():
    return {"message": "Patient Management System API is running."}
@app.get("/about")
def about():
    return {"message": "This API is designed to manage patient records, appointments, and other related healthcare information."}

@app.get("/patients")
def get_patients():
    return data_load()

@app.get("/patients/{patient_name}")
def get_patient(patient_name: str = Path(..., description="The Name of the patient to retrieve", example="Asad Khan")):
    patients = data_load()
    for patient in patients:
        if patient["name"] == patient_name:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort by value should be height, weight, or age", example="age"), order : str = Query(..., description="asc or desc")):
    patients = data_load()
    if sort_by not in ["height", "weight", "age"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by value. Must be 'height', 'weight', or 'age'.")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'.")
    order = True if order == "desc" else False
    sorted_patients = sorted(patients, key=lambda x: x[sort_by], reverse=order)
    return sorted_patients
    
@app.post("/patients")
def add_patient(patient: Patient):
    patients = data_load()
    if patient.name in [p["name"] for p in patients]:
        raise HTTPException(status_code=400, detail="Patient with this name already exists.")
    patients.append(patient.dict())
    with open("patient.json", "w") as file:
        json.dump(patients, file, indent=4)
    return JSONResponse(status_code=201, content={"message": "Patient added successfully."})