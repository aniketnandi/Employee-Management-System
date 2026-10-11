def test_create_and_list_departments(client, admin_headers):
    assert client.post("/api/v1/departments/", json={"name": "Finance"}, headers=admin_headers).status_code == 201
    assert client.post("/api/v1/departments/", json={"name": "Engineering"}, headers=admin_headers).status_code == 201

    names = [d["name"] for d in client.get("/api/v1/departments/", headers=admin_headers).json()]
    assert names == ["Engineering", "Finance"]


def test_duplicate_department_rejected(client, admin_headers):
    client.post("/api/v1/departments/", json={"name": "Finance"}, headers=admin_headers)
    assert client.post("/api/v1/departments/", json={"name": "Finance"}, headers=admin_headers).status_code == 409


def test_deleting_department_unassigns_employees(client, admin_headers):
    dept = client.post("/api/v1/departments/", json={"name": "Ops"}, headers=admin_headers).json()
    emp = client.post(
        "/api/v1/employees/",
        json={"name": "Kai", "email": "kai@example.com", "department_id": dept["id"]},
        headers=admin_headers,
    ).json()

    assert client.delete(f"/api/v1/departments/{dept['id']}", headers=admin_headers).status_code == 204
    assert client.get(f"/api/v1/employees/{emp['id']}", headers=admin_headers).json()["department_id"] is None


def test_employee_role_cannot_create_department(client, employee_headers):
    assert client.post("/api/v1/departments/", json={"name": "HR"}, headers=employee_headers).status_code == 403
