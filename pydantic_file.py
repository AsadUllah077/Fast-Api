from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Annotated
import json
class User(BaseModel):
    id: int 
    name: Annotated[str, Field(..., description="The name of the user", json_schema_extra={"example": "John Doe"})]
    weight: float
    allergies: Annotated[List[str], Field(default=None, description="List of allergies", json_schema_extra={"example": ["peanuts", "shellfish"]})]
    contacts_details: Annotated[Dict[str, str], Field(default={'email': 'example@example.com', 'phone': '123456'})]

def add_user(user: User):
   print(f"User added: {user}")

user_data = {
    "id": 1,
    "name": "John Doe",
    "weight": 70.5,
    "allergies": ["peanuts", "shellfish"],
    "contacts_details": {
        "email": "john.doe@example.com",
        "phone": "123-456-7890"
    }
}
user1 = User(**user_data)
add_user(user1)
