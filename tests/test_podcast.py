class TestPodcast:
    def test_create_podcast(self, client):
        response = client.post(
            "/podcasts/",
            json={
                "title": "Tech Talks",
                "description": "Podcast sobre tecnología",
                "category": "Tecnología",
                "language": "Español",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Tech Talks"
        assert data["category"] == "Tecnología"
        assert "id" in data

    def test_get_podcasts(self, client):
        client.post(
            "/podcasts/",
            json={"title": "DevOps Cast", "category": "Tecnología"},
        )
        response = client.get("/podcasts/")
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_podcast_by_id(self, client):
        create_resp = client.post(
            "/podcasts/",
            json={"title": "Mi Podcast", "category": "Educación"},
        )
        podcast_id = create_resp.json()["id"]

        response = client.get(f"/podcasts/{podcast_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Mi Podcast"

    def test_get_podcast_not_found(self, client):
        response = client.get("/podcasts/9999")
        assert response.status_code == 404

    def test_update_podcast(self, client):
        create_resp = client.post(
            "/podcasts/",
            json={"title": "Old Name", "category": "General"},
        )
        podcast_id = create_resp.json()["id"]

        response = client.put(
            f"/podcasts/{podcast_id}",
            json={"title": "New Name", "category": "Ciencia"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "New Name"
        assert response.json()["category"] == "Ciencia"

    def test_patch_podcast(self, client):
        create_resp = client.post(
            "/podcasts/",
            json={"title": "Patch Test", "category": "Tech"},
        )
        podcast_id = create_resp.json()["id"]

        response = client.patch(
            f"/podcasts/{podcast_id}",
            json={"title": "Patched Title"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Patched Title"
        assert response.json()["category"] == "Tech"

    def test_delete_podcast(self, client):
        create_resp = client.post(
            "/podcasts/",
            json={"title": "To Delete", "category": "Test"},
        )
        podcast_id = create_resp.json()["id"]

        response = client.delete(f"/podcasts/{podcast_id}")
        assert response.status_code == 204

        response = client.get(f"/podcasts/{podcast_id}")
        assert response.status_code == 404

    def test_create_podcast_missing_fields(self, client):
        response = client.post("/podcasts/", json={"title": "Solo titulo"})
        assert response.status_code == 422

    def test_update_podcast_not_found(self, client):
        response = client.put(
            "/podcasts/9999",
            json={"title": "No existe", "category": "Test"},
        )
        assert response.status_code == 404

    def test_patch_podcast_not_found(self, client):
        response = client.patch("/podcasts/9999", json={"title": "No"})
        assert response.status_code == 404

    def test_delete_podcast_not_found(self, client):
        response = client.delete("/podcasts/9999")
        assert response.status_code == 404

    def test_create_podcast_default_idioma(self, client):
        response = client.post(
            "/podcasts/",
            json={"title": "Default Language", "category": "Test"},
        )
        assert response.status_code == 201
        assert response.json()["language"] == "Español"