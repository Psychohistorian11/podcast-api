class TestEpisode:
    def _create_dependencies(self, client):
        """Crear un participant y un podcast para las foreign keys."""
        participant = client.post(
            "/participants/",
            json={"name": "Host Test", "email": "host@test.com", "role": "host"},
        ).json()
        podcast = client.post(
            "/v2/podcasts/",
            json={"title": "Test Podcast", "category": "Test"},
        ).json()
        return participant["id"], podcast["id"]

    def test_create_episode(self, client):
        part_id, pod_id = self._create_dependencies(client)
        response = client.post(
            "/episodes/",
            json={
                "title": "Episodio Piloto",
                "description": "Primer episodio",
                "duration_minutes": 45,
                "podcast_id": pod_id,
                "participant_id": part_id,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Episodio Piloto"
        assert data["description"] == "Primer episodio"
        assert data["duration_minutes"] == 45
        assert "id" in data

    def test_get_episodes(self, client):
        part_id, pod_id = self._create_dependencies(client)
        client.post(
            "/episodes/",
            json={
                "title": "Ep 1",
                "description": "Descripción del episodio 1",
                "duration_minutes": 30,
                "podcast_id": pod_id,
                "participant_id": part_id,
            },
        )
        response = client.get("/episodes/")
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_episode_by_id(self, client):
        part_id, pod_id = self._create_dependencies(client)
        create_resp = client.post(
            "/episodes/",
            json={
                "title": "Ep Especial",
                "duration_minutes": 60,
                "podcast_id": pod_id,
                "participant_id": part_id,
            },
        )
        episode_id = create_resp.json()["id"]

        response = client.get(f"/episodes/{episode_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Ep Especial"

    def test_get_episode_not_found(self, client):
        response = client.get("/episodes/9999")
        assert response.status_code == 404

    def test_update_episode(self, client):
        part_id, pod_id = self._create_dependencies(client)
        create_resp = client.post(
            "/episodes/",
            json={
                "title": "Original",
                "duration_minutes": 30,
                "podcast_id": pod_id,
                "participant_id": part_id,
            },
        )
        episode_id = create_resp.json()["id"]

        response = client.put(
            f"/episodes/{episode_id}",
            json={
                "title": "Actualizado",
                "duration_minutes": 50,
                "podcast_id": pod_id,
                "participant_id": part_id,
            },
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Actualizado"
        assert response.json()["duration_minutes"] == 50

    def test_patch_episode(self, client):
        part_id, pod_id = self._create_dependencies(client)
        create_resp = client.post(
            "/episodes/",
            json={
                "title": "Patch Test",
                "duration_minutes": 25,
                "podcast_id": pod_id,
                "participant_id": part_id,
            },
        )
        episode_id = create_resp.json()["id"]

        response = client.patch(
            f"/episodes/{episode_id}",
            json={"duration_minutes": 40},
        )
        assert response.status_code == 200
        assert response.json()["duration_minutes"] == 40
        assert response.json()["title"] == "Patch Test"

    def test_delete_episode(self, client):
        part_id, pod_id = self._create_dependencies(client)
        create_resp = client.post(
            "/episodes/",
            json={
                "title": "To Delete",
                "duration_minutes": 15,
                "podcast_id": pod_id,
                "participant_id": part_id,
            },
        )
        episode_id = create_resp.json()["id"]

        response = client.delete(f"/episodes/{episode_id}")
        assert response.status_code == 204

        response = client.get(f"/episodes/{episode_id}")
        assert response.status_code == 404

    def test_create_episode_missing_fields(self, client):
        response = client.post("/episodes/", json={"title": "Episodio con datos incompletos"})
        assert response.status_code == 422

    def test_update_episode_not_found(self, client):
        response = client.put(
            "/episodes/9999",
            json={
                "title": "No",
                "duration_minutes": 10,
                "podcast_id": 1,
                "participant_id": 1,
            },
        )
        assert response.status_code == 404

    def test_patch_episode_not_found(self, client):
        response = client.patch("/episodes/9999", json={"title": "No"})
        assert response.status_code == 404

    def test_delete_episode_not_found(self, client):
        response = client.delete("/episodes/9999")
        assert response.status_code == 404