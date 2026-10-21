from fastapi import FastAPI, Path, HTTPException, Query
import json
app = FastAPI()

def data_load():
    with open("patient.json", "r") as file:
        return json.load(file)

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
    