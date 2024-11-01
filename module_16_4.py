from fastapi import FastAPI, status, Body, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int):
    if users:
        last_user_id = users[-1].id
        user_id = last_user_id + 1
    else:
        user_id = 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int):
    try:
        edit_user = users[user_id-1]
        edit_user.username = username
        edit_user.age = age
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{id}')
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(i)  # Удаляем и сохраняем удаленного пользователя
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")


# Python -m uvicorn module_16_4:app