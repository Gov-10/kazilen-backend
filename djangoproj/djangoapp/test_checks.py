import pytest
from django.test import Client
import json

@pytest.mark.django_db
def test_db():
    client = Client()
    resp = client.get("/api/db_health/")
    assert resp.status_code==200
    assert resp.json() == {"status": "DB is up"}
