from app.models import User


def test_create_user_success(client):
    response = client.post(
        "/api/auth/register",
        json={
            "first_name": "Mathilde",
            "last_name": "Paisley",
            "email": "mathilde.paisley@example.com",
            "password": "Motdepasse123",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["first_name"] == "Mathilde"
    assert data["last_name"] == "Paisley"
    assert data["email"] == "mathilde.paisley@example.com"
    assert data["is_active"] is True
    assert "hashed_password" not in data
    assert "password" not in data


def test_create_user_duplicate_email_refused(client):
    payload = {
        "first_name": "Mathilde",
        "last_name": "Paisley",
        "email": "doublon@example.com",
        "password": "Motdepasse123",
    }

    first_response = client.post("/api/auth/register", json=payload)
    second_response = client.post("/api/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Cette adresse e-mail est déjà utilisée."


def test_create_user_password_too_short_refused(client):
    response = client.post(
        "/api/auth/register",
        json={
            "first_name": "Mathilde",
            "last_name": "Paisley",
            "email": "court@example.com",
            "password": "court",
        },
    )

    assert response.status_code == 422


def test_password_is_not_stored_in_clear_text(client, db_session):
    response = client.post(
        "/api/auth/register",
        json={
            "first_name": "Mathilde",
            "last_name": "Paisley",
            "email": "secure@example.com",
            "password": "Motdepasse123",
        },
    )

    assert response.status_code == 201

    user = db_session.query(User).filter(User.email == "secure@example.com").first()

    assert user is not None
    assert user.hashed_password != "Motdepasse123"
    assert user.hashed_password.startswith("$2b$")
