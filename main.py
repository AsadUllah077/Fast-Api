from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic_f.pydantic_file import Patient, UpdatePatient
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
    
@app.post("/patients")
def add_patient(patient: Patient):
    patients = data_load()
    if patient.name in [p["name"] for p in patients]:
        raise HTTPException(status_code=400, detail="Patient with this name already exists.")
    patients.append(patient.dict())
    with open("patient.json", "w") as file:
        json.dump(patients, file, indent=4)
    return JSONResponse(status_code=201, content={"message": "Patient added successfully."})


@app.put("/patients/{patient_name}")
def update_patient(patient_name: str, updated_patient: UpdatePatient):
    patients =data_load()
    # return patients
    for i, patient in enumerate(patients):
        if patient["name"].lower() == patient_name.lower():
            updated_data = updated_patient.dict(exclude_unset=True)
            patients[i].update(updated_data)
            height = patients[i].get("height")
            weight = patients[i].get("weight")
            if height is not None and weight is not None:
                bmi_value = weight / (height ** 2)
                patients[i]["bmi"] = bmi_value
                if bmi_value < 18.5:
                    patients[i]["verdict"] = "Underweight"
                elif 18.5 <= bmi_value < 24.9:
                    patients[i]["verdict"] = "Normal weight"
                elif 25 <= bmi_value < 29.9:
                    patients[i]["verdict"] = "Overweight"
                else:
                    patients[i]["verdict"] = "Obesity"
            else:
                raise HTTPException(status_code=400, detail="Height and weight must be provided to calculate BMI and verdict.")
            with open("patient.json", "w") as file:
                json.dump(patients, file, indent=4)
            return JSONResponse(status_code=200, content={"message": "Patient updated successfully."})
        
    raise HTTPException(status_code=404, detail="Patient not found")

@app.delete("/patients/{patient_name}")
def delete_patient(patient_name: str):
    patients = data_load()
    for i, patient in enumerate(patients):
        if patient["name"].lower() == patient_name.lower():
            del patients[i]
            with open("patient.json", "w") as file:
                json.dump(patients, file, indent=4)
            return JSONResponse(status_code=200, content={"message": "Patient deleted successfully."})
    raise HTTPException(status_code=404, detail="Patient not found")