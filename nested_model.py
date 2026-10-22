from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    zip_code: str
class Patient(BaseModel):
    id: int
    name: str
    age: int
    address: Address

patient_address = {
    "city": "New York", 
    "state": "NY",
    "zip_code": "10001"
}

patient_data = {
    "id": 1,
    "name": "John Doe",
    "age": 25,
    "address": Address(**patient_address)
}

patient = Patient(**patient_data)
print(patient)