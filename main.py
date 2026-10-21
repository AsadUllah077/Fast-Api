from fastapi import FastAPI, Path
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
    return {"message": "Patient not found."}