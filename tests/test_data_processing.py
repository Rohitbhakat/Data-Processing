import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

base_path = "/data"


class TestAPI:
    file_id = None

    def test_upload_file(self):
        file_path = os.path.join("tests", "sample_data.csv")

        with open(file_path, "rb") as f:
            response = client.post(f"{base_path}/upload", files={"file": f})

        assert response.status_code == 200
        assert "file_id" in response.json()
        assert response.json()["message"] == "File uploaded successfully"
        TestAPI.file_id = response.json()["file_id"]

    def test_data_summary(self):
        print(TestAPI.file_id)
        response = client.get(f"{base_path}/summary/{TestAPI.file_id}")

        assert response.status_code == 200
        summary = response.json()["summary"]

        assert isinstance(summary, dict)
        for col in summary:
            assert "mean" in summary[col]
            assert "median" in summary[col]
            assert "std" in summary[col]
            assert "dtype" in summary[col]

    def test_data_transformation(self):

        transformation_payload = {
            "transformations": {"normalize": ["Age"], "fill_missing": {}}
        }

        response = client.post(
            f"{base_path}/transform/{TestAPI.file_id}", json=transformation_payload
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Transformations applied successfully"

    def test_data_visualization(self):

        response = client.get(
            f"{base_path}/visualize/{TestAPI.file_id}?chart_type=histogram&columns=Age"
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    def test_summary_with_invalid_file_id(self):
        response = client.get(f"{base_path}/summary/invalid_file_id")
        assert response.status_code == 404
