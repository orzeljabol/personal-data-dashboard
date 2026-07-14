def test_create_entry_can_be_retrived(client):
    payload = {
        "date": "2026-07-20",
        "mood": 5,
        "energy": 6
    }

    post_response = client.post(
        "/api/entries/",
        json=payload
    )

    assert post_response.status_code == 201

    data = post_response.json()
    assert data["date"] == "2026-07-20"
    assert data["mood"] == 5
    assert data["energy"] == 6
    
    get_response = client.get("/api/entries")
    
    assert get_response.status_code == 200
    assert len(get_response.json()) == 1 
    
    data = get_response.json()
    data = data[0]
    
    assert data["date"] == "2026-07-20"
    assert data["mood"] == 5
    assert data["energy"] == 6
    
    

def test_create_entry_duplicate_date(client):
    payload = {
        "date": "2026-07-20",
        "mood": 5,
        "energy": 6
    }

    first_response = client.post("/api/entries/", json=payload)
    second_response = client.post("/api/entries/", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400


def test_create_entry_invalid_data(client):
    
    payload = {
        "date": "2026-07-20",
        "mood": 11,
        "energy": 6
    }
    response = client.post(
        "/api/entries/",
        json=payload
    )
    
    assert response.status_code == 422
    
    response = client.get("/api/entries")
    
    assert response.status_code == 200
    assert response.json() == []
