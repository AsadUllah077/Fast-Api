
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional

class Patient(BaseModel):
    name: Annotated[str, Field(..., description="The Name of the patient", example="Asad Khan")]
    age: Annotated[int, Field(..., description="The Age of the patient", example=30)]
    city: Annotated[str, Field(..., description="The City of the patient", example="New York")]
    gender: Annotated[str, Field(..., description="The Gender of the patient", example="Male")]
    height: Annotated[float, Field(..., description="The Height of the patient in meters", example=1.75)]
    weight: Annotated[float, Field(..., description="The Weight of the patient in kilograms", example=70.5)]

class UpdatePatient(BaseModel):
    name: Optional[Annotated[str, Field(None, description="The Name of the patient", example="Asad Khan")]]
    age: Optional[Annotated[int, Field(None, description="The Age of the patient", example=30)]]
    city: Optional[Annotated[str, Field(None, description="The City of the patient", example="New York")]]
    gender: Optional[Annotated[str, Field(None, description="The Gender of the patient", example="Male")]]
    height: Optional[Annotated[float, Field(None, description="The Height of the patient in meters", example=1.75)]]
    weight: Optional[Annotated[float, Field(None, description="The Weight of the patient in kilograms", example=70.5)]]
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