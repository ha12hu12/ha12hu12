from app import schemas
import pytest
#test the: get_posts functions
    #test normal
def test_get_all_posts(authorized_client, create_test_posts):
    response = authorized_client.get("/posts/")

    assert response.status_code == 200
    #test if post doesn't exist
def test_get_all_posts_notEXIST(authorized_client):
    response = authorized_client.get("/posts/")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "there is no posts in the database"}

    #test get all posts with unauthorized user
def test_unauthorized_user_get_all_posts(client, create_test_posts):
    response = client.get("/posts/")

    assert response.status_code == 401



#test the: get one post functions
    #normal test
def test_authorized_get_one_post(authorized_client,  create_test_posts):
    the_post = create_test_posts[0]
    response = authorized_client.get(f"/posts/get_post/{the_post.id}")
    schemas.post_get_schema(**response.json())
    assert response.status_code == 200

    #test if it doesn't exist
def test_get_one_post_notEXIST(authorized_client):
    response = authorized_client.get("/posts/get_post/91823")
    assert response.status_code == 404
    assert response.json() == {"detail": "there is no post with id: 91823"}


    #test get_one_post with authorized user
def test_unauthorized_get_one_post(client, create_test_posts):
    response = client.get(f"/posts/get_post/{create_test_posts[0].id}")
    assert response.status_code == 401 



#test the: create post function
@pytest.mark.parametrize("title, content", [("TEST1", "WE ARE TESTING 1"), ("TEST2", "WE ARE TESTING 2")])
def test_create_post(authorized_client, title, content):
    data={
        "title": title, 
        "content": content
    }
    response = authorized_client.post("/posts/create_post", json=data)

    created_post = schemas.post_create_out_schema(**response.json())
    assert response.status_code == 201
    assert response.json().get("title") == title
    assert response.json().get("id") == created_post.id
    assert response.json().get("content") == content
    assert response.json().get("owner_id") == created_post.owner_id

#test create with unauthorized user
def test_unauthorized_user_create_post(client):
    data={
        "title": "title", 
        "content": "content"
    }
    response = client.post("/posts/create_post", json=data)
    assert response.status_code == 401



#test the: delete post function
    #normal test
def test_delete_post(authorized_client, create_test_posts):
    response = authorized_client.delete(f"/posts/delete_post/{create_test_posts[0].id}")

    assert response.status_code == 204

    #test if the user didn't own the post
def test_delete_post_without_beingOwner(authorized_client, create_test_posts):
    #im using here the post number2 bc it was created buy another user (that user was created with: create_test_user2 function)
    response = authorized_client.delete(f"/posts/delete_post/{create_test_posts[1].id}")
    assert response.status_code == 403
    assert response.json() == {"detail": "you with the id: 1 can not delete this post with owner id: 2"}

    #test if it doesn't exist
def test_delete_noneEXISTNE_post(authorized_client):
    response = authorized_client.delete("/posts/delete_post/99")
    assert response.status_code == 404
    assert response.json() == {"detail":"there is no post with the id 99"}

    #test delete post with unauthorized user
def test_unauthorized_user_delete_post(client):
    #no need to look for a real post  bc we are unauthorized it wont let us search
    response = client.delete("/posts/delete_post/1")
    assert response.status_code == 401



#test the: update post functions
    #normal test
def test_update_post(authorized_client, create_test_posts):
    data = {
        "title": "titling",
        "content": "contining"
    }
    response = authorized_client.put(f"/posts/update_post/{create_test_posts[0].id}", 
                                     json=data)
    updated_post = schemas.post_update_data_schema(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]