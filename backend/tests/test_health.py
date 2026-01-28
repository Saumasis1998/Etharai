def test_health_ok(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    j = r.json()
    assert j["status"] == "ok"
    assert j["db"] in ("ok", "unavailable")
