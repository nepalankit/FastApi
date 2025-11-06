# test/test_users.py
import pytest
from app import schemas
from .conftest import client as test_client,session
from jose import jwt
import os
from dotenv import load_dotenv

@pytest.fixture
def test_user(test_client):
    user_data={"email": "a@gmail.com", "password": "password123"}
    
    res=test_client.post("/users",json=user_data)
    assert res.status_code==201
    print(res.json())
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user
    


# def test_root(test_client):
#     res = test_client.get('/')
#     assert res.status_code == 200
#     assert res.json().get('message') == 'hello world'

def test_create_user(test_client):
    payload = {"email": "a@gmail.com", "password": "password123"}
    res = test_client.post('/users/', json=payload)

    # Validate response
    assert res.status_code == 201
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == payload["email"]


def test_login_user(test_client,test_user):
    res=test_client.post(
        "/login",data={"username":test_user["email"] , "password": test_user["password"]}
    )
    login_res=schemas.Token(**res.json())
    payload=jwt.decode(login_res.access_token,os.getenv('DATABASE_SECRET_KEY'),algorithms=os.getenv('DATABASE_ALGORITHM'))
    print(res.json())
    id=payload.get("user_id")
    assert id==test_user['id']
    assert login_res.token_type=="bearer"
     # Validate response
    assert res.status_code==200
       
def test_incorrect_login(test_user,test_client):
    res=test_client.post(
        '/login',data={"username":test_user['email'],"password":"wrongpassword"})
    assert res.status_code==403
    assert res.json().get('detail')=="Invalid Credentials"
    