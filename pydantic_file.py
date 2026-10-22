from pydantic import BaseModel, Field

class User(BaseModel):
    id: int 
    name: str

def add_user(user: User):
    print(f"Adding user: {user.name} with ID: {user.id}")

user_data = {
    "id": 1,
    "name": "John Doe"
}
user1 = User(**user_data)
add_user(user1)
