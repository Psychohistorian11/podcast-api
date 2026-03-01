class TestParticipant:
    def test_create_participant(self, client):
        response = client.post(
            "/participants/",
            json={
                "name": "Juan Pérez",
                "email": "juan@test.com",
                "role": "host",
                "bio": "Host principal del podcast",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Juan Pérez"
        assert data["email"] == "juan@test.com"
        assert data["role"] == "host"
        assert "id" in data

    def test_get_participants(self, client):
        client.post(
            "/participants/",
            json={"name": "Ana López", "email": "ana@test.com", "role": "guest"},
        )
        response = client.get("/participants/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_participant_by_id(self, client):
        create_resp = client.post(
            "/participants/",
            json={"name": "Carlos", "email": "carlos@test.com", "role": "producer"},
        )
        participant_id = create_resp.json()["id"]

        response = client.get(f"/participants/{participant_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Carlos"

    def test_get_participant_not_found(self, client):
        response = client.get("/participants/9999")
        assert response.status_code == 404

    def test_update_participant(self, client):
        create_resp = client.post(
            "/participants/",
            json={"name": "María", "email": "maria@test.com", "role": "host"},
        )
        participant_id = create_resp.json()["id"]

        response = client.put(
            f"/participants/{participant_id}",
            json={"name": "María García", "email": "maria@test.com", "role": "host"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "María García"

    def test_patch_participant(self, client):
        create_resp = client.post(
            "/participants/",
            json={"name": "Pedro", "email": "pedro@test.com", "role": "guest"},
        )
        participant_id = create_resp.json()["id"]

        response = client.patch(
            f"/participants/{participant_id}",
            json={"role": "host"},
        )
        assert response.status_code == 200
        assert response.json()["role"] == "host"
        assert response.json()["name"] == "Pedro"  # No cambió

    def test_delete_participant(self, client):
        create_resp = client.post(
            "/participants/",
            json={"name": "Borrar", "email": "borrar@test.com", "role": "test"},
        )
        participant_id = create_resp.json()["id"]

        response = client.delete(f"/participants/{participant_id}")
        assert response.status_code == 204

        response = client.get(f"/participants/{participant_id}")
        assert response.status_code == 404

    def test_create_participant_missing_fields(self, client):
        response = client.post("/participants/", json={"name": "Incompleto"})
        assert response.status_code == 422

    def test_update_participant_not_found(self, client):
        response = client.put(
            "/participants/9999",
            json={"name": "No existe", "email": "no@test.com", "role": "test"},
        )
        assert response.status_code == 404

    def test_patch_participant_not_found(self, client):
        response = client.patch("/participants/9999", json={"name": "No existe"})
        assert response.status_code == 404

    def test_delete_participant_not_found(self, client):
        response = client.delete("/participants/9999")
        assert response.status_code == 404