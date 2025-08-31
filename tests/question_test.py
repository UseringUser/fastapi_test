import requests
import json
from back.models import Question

BASE_URL = "http://localhost:8000"

class TestQuestion:
    def test_question_list_404(self):
        response = requests.get(BASE_URL + "/questions")
        assert response.status_code == 404
        assert response.json()['detail'] == 'Question not found'

    def test_question_assert(self):
        body = {
            "text": "2+5"
        }
        response = requests.post(BASE_URL + "/questions/", json=body)
        assert response.status_code == 200
        assert response.json()['text'] == '2+5'

    def test_question_list(self):
        response = requests.get(BASE_URL + "/questions")
        questions = json.loads(response.text)
        for question in questions:
            assert isinstance(question['text'], str)

    def test_question_assert_400(self):
        body = {
            "text": " "
        }
        response = requests.post(BASE_URL + "/questions", json=body)
        assert response.status_code == 400
        assert response.json()['detail'] == 'Question text is required'

    def test_delete_404(self):
        response = requests.delete(BASE_URL + "/questions/999")
        assert response.status_code == 404
        assert response.json()['detail'] == 'Question not found'
