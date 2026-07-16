def test_create_entry_can_be_retrieved(client):
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


def test_empty_database(client):
    response = client.get("/api/entries")
    
    assert response.status_code == 200
    assert response.json()== []


def test_get_entries_returns_multiple_entries_in_descending_date_order(client):
    payload1 = {
        "date": "2026-07-20",
        "mood": 5,
        "energy": 6
    }
    response_post1 = client.post(
        "/api/entries/",
        json=payload1
    )
    
    assert response_post1.status_code == 201

    payload2 = {
        "date": "2026-07-21",
        "mood": 7,
        "energy": 8
    }
    response_post2 = client.post(
        "/api/entries/",
        json=payload2
    )
    
    assert response_post2.status_code == 201

    response_get = client.get("/api/entries")

    assert response_get.status_code == 200
    data = response_get.json()
    
    assert len(data) == 2
    
    newest_entry = data[0]
    oldest_entry = data[1]
    
    
    assert oldest_entry["date"] == "2026-07-20"
    assert oldest_entry["mood"] == 5
    assert oldest_entry["energy"] == 6
    
    assert newest_entry["date"] == "2026-07-21"
    assert newest_entry["mood"] == 7
    assert newest_entry["energy"] == 8

    analytics_response = client.get("/api/analytics")
    assert analytics_response.status_code == 200
    data = analytics_response.json()
    assert data["average_mood"] == 6
    assert data["average_energy"] == 7
    assert data["tracked_days"] == 2