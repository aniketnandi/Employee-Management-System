EMPLOYEE = {"name": "Jane Doe", "email": "jane@example.com", "role": "Engineer", "salary": 100000}


def test_crud_lifecycle(client, admin_headers):
    created = client.post("/api/v1/employees/", json=EMPLOYEE, headers=admin_headers)
    assert created.status_code == 201
    emp_id = created.json()["id"]

    assert client.get(f"/api/v1/employees/{emp_id}", headers=admin_headers).json()["name"] == "Jane Doe"

    updated = client.put(f"/api/v1/employees/{emp_id}", json={"role": "Senior Engineer"}, headers=admin_headers)
    assert updated.status_code == 200
    assert updated.json()["role"] == "Senior Engineer"
    assert updated.json()["email"] == "jane@example.com"

    assert client.delete(f"/api/v1/employees/{emp_id}", headers=admin_headers).status_code == 204
    assert client.get(f"/api/v1/employees/{emp_id}", headers=admin_headers).status_code == 404


def test_duplicate_email_rejected(client, admin_headers):
    client.post("/api/v1/employees/", json=EMPLOYEE, headers=admin_headers)
    res = client.post("/api/v1/employees/", json={**EMPLOYEE, "name": "Other"}, headers=admin_headers)
    assert res.status_code == 409


def test_update_to_existing_email_rejected(client, admin_headers):
    client.post("/api/v1/employees/", json=EMPLOYEE, headers=admin_headers)
    other = client.post(
        "/api/v1/employees/", json={"name": "John", "email": "john@example.com"}, headers=admin_headers
    ).json()
    res = client.put(f"/api/v1/employees/{other['id']}", json={"email": "jane@example.com"}, headers=admin_headers)
    assert res.status_code == 409


def test_validation_errors(client, admin_headers):
    assert client.post("/api/v1/employees/", json={"name": "X", "email": "nope"}, headers=admin_headers).status_code == 422
    assert client.post("/api/v1/employees/", json={**EMPLOYEE, "salary": -1}, headers=admin_headers).status_code == 422
    res = client.post("/api/v1/employees/", json={**EMPLOYEE, "department_id": 999}, headers=admin_headers)
    assert res.status_code == 422


def test_search_and_filter(client, admin_headers):
    eng = client.post("/api/v1/departments/", json={"name": "Engineering"}, headers=admin_headers).json()
    client.post("/api/v1/employees/", json={**EMPLOYEE, "department_id": eng["id"]}, headers=admin_headers)
    client.post(
        "/api/v1/employees/",
        json={"name": "Sam Lee", "email": "sam@example.com", "role": "Accountant"},
        headers=admin_headers,
    )

    by_name = client.get("/api/v1/employees/", params={"q": "jane"}, headers=admin_headers).json()
    assert [e["name"] for e in by_name] == ["Jane Doe"]

    by_role = client.get("/api/v1/employees/", params={"q": "account"}, headers=admin_headers).json()
    assert [e["name"] for e in by_role] == ["Sam Lee"]

    by_dept = client.get("/api/v1/employees/", params={"department_id": eng["id"]}, headers=admin_headers).json()
    assert [e["name"] for e in by_dept] == ["Jane Doe"]


def test_employee_role_is_read_only(client, admin_headers, employee_headers):
    emp_id = client.post("/api/v1/employees/", json=EMPLOYEE, headers=admin_headers).json()["id"]

    assert client.get("/api/v1/employees/", headers=employee_headers).status_code == 200
    assert client.post("/api/v1/employees/", json=EMPLOYEE, headers=employee_headers).status_code == 403
    assert client.put(f"/api/v1/employees/{emp_id}", json={"role": "x"}, headers=employee_headers).status_code == 403
    assert client.delete(f"/api/v1/employees/{emp_id}", headers=employee_headers).status_code == 403
