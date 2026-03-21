from app.models import User


def test_create_user_success(db_session, client):
    #Arrange & Act
    response = client.post(
        "/api/v1/users",
        json={
            "login": "newuser"
        }
    )

    #Assert
    assert response.status_code == 200
    assert response.json()["login"] == "newuser"
    assert response.json()["id"] is not None


def test_create_user_already_exists(db_session, client):
    #Arrange
    user = User(login="existing")
    db_session.add(user)
    db_session.commit()

    #Act
    response = client.post(
        "/api/v1/users",
        json={
            "login": "existing"
        }
    )

    #Assert
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_user_empty_login(db_session, client):
    #Act
    response = client.post(
        "/api/v1/users",
        json={
            "login": ""
        }
    )

    #Assert
    assert response.status_code == 422


def test_get_current_user_success(db_session, client):
    #Arrange
    user = User(login="testuser")
    db_session.add(user)
    db_session.commit()

    #Act
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 200
    assert response.json()["login"] == "testuser"
    assert response.json()["id"] is not None


def test_get_current_user_unauthorized(db_session, client):
    #Act
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer notexists"
        }
    )

    #Assert
    assert response.status_code == 401
