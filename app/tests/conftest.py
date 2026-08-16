#sqlalchemy
from sqlalchemy  import create_engine
from  sqlalchemy.orm  import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#app.
from app.config import settings
from app.database import Base
from app.main import app
from app.database import get_db
from app.oauth2 import create_access_token
from app import models
#other
from fastapi.testclient import TestClient
import pytest
sql_database_url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(sql_database_url)

TestSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush= False)


#database fixtures
@pytest.fixture
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

#authorization fixtures
@pytest.fixture
def token(create_test_user):
    return create_access_token(data={"id": create_test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

#others
@pytest.fixture
def create_test_user(client):
    #note: 
    # create_test_user ALREADY calls client, 
    # so if you call this fixture you dont need to call client.

    #make sure if you change the user email, to change it in test_vote -> test_create_vote_twice AND test_users --> test inccorrect login
    response = client.post("/users/create_user", json={"email": "11very_not_normal_guy@gmail.com",
                                                     "password": "VERYsecretADMingACCOUNT"
                                                     }  )
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = "VERYsecretADMingACCOUNT"
    return new_user

@pytest.fixture
def create_test_user2(client):
    #note: 
    # create_test_user ALREADY calls client, 
    # so if you call this fixture you dont need to call client
    response = client.post("/users/create_user", json={"email": "very_normal_guy@gmail.com",
                                                     "password": "111VERYsecretADMingACCOUNT"
                                                     }  )
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = "VERYsecretADMingACCOUNT"
    return new_user

@pytest.fixture
def create_test_posts(session, create_test_user, create_test_user2):


    session.add_all([models.Post(title = "Getting Started with FastAPI", content="FastAPI makes it easy to build modern, high-performance APIs with Python.", owner_id=create_test_user['id']),
                     models.Post(title = "Understanding SQLAlchemy", content="SQLAlchemy provides powerful tools for working with databases using Python.", owner_id=create_test_user2['id']),
                     models.Post(title = "Why Use Docker?", content="Docker helps developers package applications and their dependencies into consistent environments.", owner_id=create_test_user['id'])])
    session.commit()
    return session.query(models.Post).all()
@pytest.fixture   
def create_test_votes(session, create_test_posts, create_test_user):
    session.add_all([models.Votes(Post_id = create_test_posts[0].id, User_id = create_test_user["id"]),
                     models.Votes(Post_id = create_test_posts[1].id, User_id = create_test_user["id"]),
                     models.Votes(Post_id = create_test_posts[2].id, User_id = create_test_user["id"])])
    session.commit()
    return session.query(models.Votes).all()