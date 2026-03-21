from decimal import Decimal

from app.models import User, Wallet


def test_add_expense_success(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name = "card", balance = 200, user_id = user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    #Act
    responce = client.post(
        "/api/v1/operations/expense", 
        json={
            "wallet_name": "card", 
            "amount": 50.0, 
            "description": "food"
        }, 
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )
     
    #Assert
    assert responce.status_code == 200
    assert responce.json()["message"] == "Expense added"
    assert responce.json()["wallet"] == wallet.name
    assert Decimal(str(responce.json()["amount"])) == Decimal(50)
    assert Decimal(str(responce.json()["new_balance"])) == Decimal(150)
    assert responce.json()["description"] == "food"
   

def test_add_expense_negative_amount(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name = "card", balance = 200, user_id = user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    #Act
    responce = client.post(
        "/api/v1/operations/expense", 
        json={
            "wallet_name": "card", 
            "amount": -100.0, 
            "description": "food"
        }, 
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert responce.status_code == 422

def test_add_expense_empty_name(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name = "card", balance = 200, user_id = user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    #Act
    responce = client.post(
        "/api/v1/operations/expense", 
        json={
            "wallet_name": "  ", 
            "amount": 50.0, 
            "description": "food"
        }, 
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert responce.status_code == 422


def test_add_expense_wallet_not_exists(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    #Act
    responce = client.post(
        "/api/v1/operations/expense", 
        json={
            "wallet_name": "card", 
            "amount": 50.0, 
            "description": "food"
        }, 
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert responce.status_code == 404

def test_add_expense_unauthorized(db_session, client):
    #Arrange

    #Act
    responce = client.post(
        "/api/v1/operations/expense", 
        json={
            "wallet_name": "card", 
            "amount": 50.0, 
            "description": "food"
        }, 
        headers={
            "Authorization": f"Bearer notexists"
        }
    )

    #Assert
    assert responce.status_code == 401

def test_add_expense_not_enough_balance(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name = "card", balance = 200, user_id = user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    #Act
    responce = client.post(
        "/api/v1/operations/expense", 
        json={
            "wallet_name": "card", 
            "amount": 250.0, 
            "description": "food"
        }, 
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )
     
    #Assert
    assert responce.status_code == 400


def test_add_income_success(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name = "card", balance = 100, user_id = user.id)
    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    #Act
    responce = client.post(
        "/api/v1/operations/income", 
        json={
            "wallet_name": "card", 
            "amount": 50.0, 
            "description": "salary"
        }, 
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )
     
    #Assert
    assert responce.status_code == 200
    assert responce.json()["message"] == "income added"
    assert responce.json()["wallet"] == wallet.name
    assert Decimal(str(responce.json()["amount"])) == Decimal(50)
    assert Decimal(str(responce.json()["new_balance"])) == Decimal(150)
    assert responce.json()["description"] == "salary"


def test_add_income_negative_amount(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.flush()
    wallet = Wallet(name = "card", balance = 100, user_id = user.id)
    db_session.add(wallet)
    db_session.commit()

    #Act
    responce = client.post(
        "/api/v1/operations/income", 
        json={
            "wallet_name": "card", 
            "amount": -50.0, 
            "description": "salary"
        }, 
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert responce.status_code == 422


def test_add_income_wallet_not_exists(db_session, client):
    #Arrange
    user = User(login="test")
    db_session.add(user)
    db_session.commit()

    #Act
    responce = client.post(
        "/api/v1/operations/income", 
        json={
            "wallet_name": "card", 
            "amount": 50.0, 
            "description": "salary"
        }, 
        headers={
            "Authorization": f"Bearer {user.login}"
        }
    )

    #Assert
    assert responce.status_code == 404


def test_add_income_unauthorized(db_session, client):
    #Arrange

    #Act
    responce = client.post(
        "/api/v1/operations/income", 
        json={
            "wallet_name": "card", 
            "amount": 50.0, 
            "description": "salary"
        }, 
        headers={
            "Authorization": f"Bearer notexists"
        }
    )

    #Assert
    assert responce.status_code == 401