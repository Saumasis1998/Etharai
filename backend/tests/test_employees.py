def test_create_and_get_employee(client):
    payload = {
        "employee_id": "E001",
        "full_name": "Alice",
        "email": "alice@example.com",
        "department": "HR",
    }

    # create
    r = client.post("/api/v1/employees", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["employee_id"] == payload["employee_id"]
    assert data["email"] == payload["email"]
    emp_id = data["id"]

    # get by id
    r2 = client.get(f"/api/v1/employees/{emp_id}")
    assert r2.status_code == 200
    assert r2.json()["id"] == emp_id


def test_list_employees(client):
    r = client.get("/api/v1/employees")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
