def test_register_creates_read_only_employee(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"username": "newuser", "email": "new@example.com", "password": "supersecret"},
    )
    assert res.status_code == 201
    assert res.json()["role"] == "employee"
    assert "password" not in res.json() and "hashed_password" not in res.json()


def test_register_ignores_requested_role(client):
    res = client.post(
        "/api/v1/auth/register",
        json={"username": "sneaky", "email": "s@example.com", "password": "supersecret", "role": "admin"},
    )
    assert res.status_code == 201
    assert res.json()["role"] == "employee"


def test_register_rejects_duplicates(client):
    payload = {"username": "dupe", "email": "dupe@example.com", "password": "supersecret"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409


def test_login_and_me(client):
    client.post(
        "/api/v1/auth/register",
        json={"username": "alice", "email": "alice@example.com", "password": "supersecret"},
    )
    res = client.post("/api/v1/auth/login", data={"username": "alice", "password": "supersecret"})
    assert res.status_code == 200
    token = res.json()["access_token"]

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "alice"


def test_login_with_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"username": "bob", "email": "bob@example.com", "password": "supersecret"},
    )
    res = client.post("/api/v1/auth/login", data={"username": "bob", "password": "wrong"})
    assert res.status_code == 401


def test_protected_routes_require_token(client):
    assert client.get("/api/v1/employees/").status_code == 401
    assert client.get("/api/v1/employees/", headers={"Authorization": "Bearer garbage"}).status_code == 401
