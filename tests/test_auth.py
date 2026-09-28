async def test_register_login_and_read_profile(client):
    registration = await client.post(
        "/api/v1/auth/register",
        json={"email": "dev@example.com", "full_name": "Demo Developer", "password": "secure-pass"},
    )
    assert registration.status_code == 201
    assert registration.json()["email"] == "dev@example.com"
    assert "password" not in registration.json()

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "dev@example.com", "password": "secure-pass"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    profile = await client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert profile.status_code == 200
    assert profile.json()["full_name"] == "Demo Developer"


async def test_duplicate_email_returns_conflict(client):
    payload = {"email": "dev@example.com", "full_name": "Demo Developer", "password": "secure-pass"}
    assert (await client.post("/api/v1/auth/register", json=payload)).status_code == 201
    assert (await client.post("/api/v1/auth/register", json=payload)).status_code == 409


async def test_profile_requires_valid_token(client):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401

