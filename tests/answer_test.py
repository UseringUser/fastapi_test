import requests
import json
from fastapi.testclient import TestClient
from main import app



BASE_URL = "http://localhost:8000"

class TestAnswer:

    def test_answer_get_404(self):
        response = requests.get(BASE_URL+"/answers/99")
        assert response.status_code == 404
        assert response.json()['detail'] == 'Answer not found'

    def test_answer_assert_404(self):
        body = {
            "text": "7"
        }
        response = requests.post(BASE_URL+"/questions/99/answers", json=body)
        assert response.status_code == 404
        assert response.json()['detail'] == 'Question not found'

    def test_answer_assert_400(self):
        body = {
            "text": " "
        }
        response = requests.post(BASE_URL + "/questions/1/answers", json=body)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Answer text is required'

    def test_answer_assert(self):
        body = {
            "text": "7"
        }
        response = requests.post(BASE_URL + "/questions/1/answers", json=body)
        assert response.status_code == 200
        assert response.json()['text'] == '7'

    def test_answer_valid(self):
        response = requests.get(BASE_URL+"/answers/1")
        assert response.status_code == 200
        assert response.json()['text'] == '7'

    def test_answer_delete_404(self):
        response = requests.delete(BASE_URL+"/answers/99")
        assert response.status_code == 404
        assert response.json()['detail'] == 'Answer not found'


