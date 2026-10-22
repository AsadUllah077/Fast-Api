from pydantic import BaseModel, Field
from typing import List, Dict, Optional
class User(BaseModel):
    id: int 
    name: str
    weight: float
    allergies: Optional[List[str]] = None
    contacts_details: Dict[str, str] = {'email': 'example@example.com', 'phone': '123456'}

def add_user(user: User):
    print(f"Adding user: {user} ")

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
