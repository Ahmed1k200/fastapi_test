from decimal import Decimal

from app.models import User, Wallet


def test_get_all_wallets_success(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet1 = Wallet(name="card", balance=100, user_id=user.id)
    wallet2 = Wallet(name="cash", balance=50, user_id=user.id)
    db_session.add(wallet1)
    db_session.add(wallet2)
    db_session.commit()

    #Act
    response = client.get(
        "/api/v1/balance",
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 200
    assert Decimal(str(response.json()["total_balance"])) == Decimal(150)


def test_get_specific_wallet_success(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=200, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()

    #Act
    response = client.get(
        "/api/v1/balance",
        params={"wallet_name": "card"},
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 200
    assert response.json()["wallet_name"] == "card"
    assert Decimal(str(response.json()["balance"])) == Decimal(200)


def test_get_wallet_not_found(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    #Act
    response = client.get(
        "/api/v1/balance",
        params={"wallet_name": "nonexistent"},
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_get_wallet_unauthorized(db_session, client):
    #Act
    response = client.get(
        "/api/v1/balance",
        params={"wallet_name": "card"},
        headers={
            "Authorization": f"Bearer notexists"
        }
    )

    #Assert
    assert response.status_code == 401


def test_get_all_wallets_with_no_wallets(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    #Act
    response = client.get(
        "/api/v1/balance",
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 200
    assert Decimal(str(response.json()["total_balance"])) == Decimal(0)


def test_create_wallet_success(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    #Act
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "savings",
            "initial_balance": 500.0
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 200
    assert response.json()["message"] == "wallet savings created"
    assert response.json()["wallet"] == "savings"
    assert Decimal(str(response.json()["balance"])) == Decimal(500)


def test_create_wallet_already_exists(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name="card", balance=100, user_id=user.id)
    db_session.add(wallet)
    db_session.commit()

    #Act
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "card",
            "initial_balance": 200.0
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_create_wallet_empty_name(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    #Act
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "   ",
            "initial_balance": 200.0
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 422


def test_create_wallet_negative_balance(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    #Act
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "card",
            "initial_balance": -100.0
        },
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert response.status_code == 422


def test_create_wallet_unauthorized(db_session, client):
    #Act
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "card",
            "initial_balance": 200.0
        },
        headers={
            "Authorization": f"Bearer notexists"
        }
    )

    #Assert
    assert response.status_code == 401
