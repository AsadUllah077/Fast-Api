from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated
import json
class User(BaseModel):
    id: int 
    email: str
    age: int
    name: Annotated[str, Field(..., description="The name of the user", json_schema_extra={"example": "John Doe"})]
    weight: float
    height: float
    allergies: Annotated[List[str], Field(default=None, description="List of allergies", json_schema_extra={"example": ["peanuts", "shellfish"]})]
    contacts_details: Annotated[Dict[str, str], Field(default={'email': 'example@example.com', 'phone': '123456'})]

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_emails = ["gmail.com", "yahoo.com", "outlook.com"]
        domain = value.split("@")[-1]
        if domain not in valid_emails:
            raise ValueError(f"Invalid email domain. Must be one of {valid_emails}.")
        return value
    
    @field_validator("name")
    @classmethod
    def name_validator(cls, value):
        return value.upper()

    @model_validator(mode="after")
    def emergency_contact(self):
        if self.age > 18 and "phone" not in self.contacts_details:
            raise ValueError("Emergency contact phone number is required for users over 18.")
        return self

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)


def add_user(user: User):
   print(f"User added: {user}")

user_data = {
    "id": 1,
    "email": "john.doe@gmail.com",
    "age": 25,
    "name": "John Doe",
    "weight": 70.5,
    "height": 1.75,
    "allergies": ["peanuts", "shellfish"],
    "contacts_details": {
        "email": "john.doe@example.com",
        "phone": "123-456-7890"
    }
}
user1 = User(**user_data)
add_user(user1)
