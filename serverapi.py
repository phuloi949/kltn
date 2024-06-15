from typing import Union
from fastapi import FastAPI, Request, Header, Body, HTTPException
from pydantic import BaseModel, validator
from starlette.responses import FileResponse
import pymongo
import uvicorn
import string 
import random
import bcrypt



app = FastAPI()

client = pymongo.MongoClient("mongodb://192.168.120.37:27017")
db = client.mydb
collection = db["clients"]
collection1 = db["users"]

class Client(BaseModel):
    _id: object
    Client_Name: str
    Client_IP: str
    Status: str
    Model: str
    Token: str
    
class User (BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@validator('username')
def username_must_be_alphanumeric(cls, value):
        if not value.isalnum() or not value.islower():
            raise ValueError("Username must contain only lowercase alphanumeric characters")
        return value
@validator('password')
def password_length(cls, value):
        if len(value) < 8 or len(value) > 16:
            raise ValueError('Password length must be between 8 and 16 characters')
        return value

@app.post("/users/")
async def create_user(user: User, collection=collection1):
    existing_user = await collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_dict = user.dict()
    await collection.insert_one(user_dict)
    return {"message": "User created successfully"}


@app.get("/items/{item_id}")
async def get_item(item_id: int, request: Request):
    client_ip = request.headers.get("Client-IP")
    client_name = request.headers.get("Client-Name")
    print(f"Client IP: {client_ip}")
    print(f"Client name: {client_name}")
    return {"item_id": item_id, "name": "Item name"}
if __name__ == "__serverapi__":
    uvicorn.run("serverapi:app", host="0.0.0.0", port=8000)

# #post token, client_ip, client_name to mongoDB 
@app.post("/addclient/")    
async def receive_data(Client_ID: str, Client_IP: str):
    token1 = 30 
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = token1))    
    print("The token to connect to server is: " + str(ran))  
    print(f"Received data: {Client_ID}, {Client_IP}")
    info = {"Client_ID": Client_ID, "Client_IP": Client_IP, "Client_Status": "Enable", "Model": "None", "Token": ran}
    collection.insert_one(info)
    return {"Client Create successfully!"}

token1 = 30
@app.get("/get_ip")
async def get_ip(request: Request, token1: str):
    client_ip = request.client.host
  #verify token
    token = collection.find_one({"Token": token1})
    if token is None:
        return {"Token is invalid"}
    else: 
        if client_ip == token["Client_IP"]:
            #return FileResponse(filename="test.txt",media_type="text/plain", headers={"Content-Disposition": "attachment"},path="test.txt")
            return FileResponse(filename="flower-homomorphic_encryption.zip", media_type="application/zip", headers={"Content-Disposition": "attachment"}, path="flower-homomorphic_encryption.zip")
        else:
            return {"Client IP": "Client IP is invalid"}
        

@app.delete("/deleteclient/")
async def delete_client(Client_ID: str):
    collection.delete_one({"Client_ID": Client_ID})
    return {"Client deleted successfully!"}


@app.post("/register")   
async def register(request: LoginRequest):
    hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    collection1.insert_one({"username": request.username, "password": hashed_password})
    return {"message": "User registered successfully"}

@app.post("/login/")
async def login(user : User):
    print(f"Received data: {user.username}, {user.password}")
    found_user = collection1.find_one({"username": user.username, "password": user.password})
    if  found_user and bcrypt.checkpw(Request.password.encode('utf-8'), user['password']):
            return {"message": "Login successful"}
    else:
         raise HTTPException(status_code=401, detail="Invalid username or password")
     
if __name__ == "__serverapi__":
     uvicorn.run("serverapi:app", host="0.0.0.0", port=8000)
     



