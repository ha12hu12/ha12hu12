
from app.schemas import user_create_out_schema
from app.config import settings
from jose import jwt
import pytest



def test_create_user(client):
    response = client.post("/users/create_user", json={"email": "11very_not_normal_guy@gmail.com",
                                                     "password": "VERYsecretADMingACCOUNT"
                                                     })
    assert response.status_code == 201
    new_user = user_create_out_schema(**response.json())
    assert new_user.email == "11very_not_normal_guy@gmail.com"



def test_login_user(client, create_test_user):
    response = client.post("/users/user_login",json={"email": create_test_user["email"], 
                                                     "password": create_test_user["password"]})
    decoded_token = jwt.decode(token=response.json().get("access_token"), key=settings.secret_key, algorithms=[settings.algorithm])
    the_id  = decoded_token.get("id")
    assert the_id == create_test_user['id']
    assert response.json().get("token_type") == "bearer"
    assert response.status_code == 200



@pytest.mark.parametrize("email, password, status_code, detail", [
        ("11very_not_normal_guy@gmail.com", "WRONG password", 403, "WRONG PASSWORD, please try again"),
        ("WRONG_email@gmail.com", "VERYsecretADMingACCOUNT", 403, "there is no user with the email: WRONG_email@gmail.com"),
        (None, "VERYsecretADMingACCOUNT", 422,[{'input': None, 'loc': ['body', 'email'], 'msg': 'Input should be a valid string', 'type': 'string_type'}]) ,
        ("11very_not_normal_guy@gmail.com", None, 422, [{'input': None, 'loc': ['body', 'password'], 'msg': 'Input should be a valid string', 'type': 'string_type'}])
])      
def test_incorrect_login(client, email, password, status_code, detail, create_test_user):
    response = client.post("/users/user_login",
                           json={"email": email, 
                            "password": password})
    assert response.status_code == status_code
    assert response.json().get("detail") == detail