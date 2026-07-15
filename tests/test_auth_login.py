from app.models import User
from app.security import hash_password


def create_test_user(db_session):
    user = User(
        first_name="Mathilde",
        last_name="Paisley",
        email="client@example.com",
        hashed_password=hash_password("Motdepasse123"),
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def test_login_success(client, db_session):
    create_test_user(db_session)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "client@example.com",
            "password": "Motdepasse123",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Connexion réussie."
    assert data["email"] == "client@example.com"
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_wrong_password_refused(client, db_session):
    create_test_user(db_session)

    response = client.post(
        "/api/auth/login",
        json={
            "email": "client@example.com",
            "password": "MauvaisMotdepasse123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides."


def test_login_unknown_account_refused(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "inconnu@example.com",
            "password": "Motdepasse123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides."
