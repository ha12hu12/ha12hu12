#test the: create/delete votes
    #normal  test
def test_create_vote(authorized_client, create_test_posts):
    the_post = create_test_posts[0]
    data={
        "post_id": the_post.id,
        "dir": True
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 200
    assert response.json() == f"vote added to: {the_post}"
    # unauthorized_create_test

def test_create_vote_twice(authorized_client, create_test_posts, create_test_votes):
    the_post = create_test_posts[0]
    data={
        "post_id": the_post.id,
        "dir": True
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 409
    assert response.json() == {"detail": f"user with the email: 11very_not_normal_guy@gmail.com already liked post with the id: {the_post.id}"}
    # unauthorized_create_test

def test_unauthorized_user_create_vote(client, create_test_posts):
    response = client.post("/votes")
    assert response.status_code == 401

    # test to create a vote to a none exist post
def test_create_vote_not_found(authorized_client, create_test_posts):
    data={
        "post_id": 32,
        "dir": True
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "there is no post with the id: 32"}


def test_delete_vote(authorized_client, create_test_posts, create_test_votes):
    the_post = create_test_posts[0]
    data={
        "post_id": the_post.id,
        "dir": False
    }
    response = authorized_client.post("/votes", json=data)
    assert response.status_code == 200
    assert response.json() == 'seccuffly deleted inshallah'