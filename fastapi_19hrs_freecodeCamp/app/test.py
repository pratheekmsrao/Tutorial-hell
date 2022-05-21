import requests
import json
from faker import Faker


def create_post():
    fake = Faker()
    global url, payload, headers, response
    url = "http://127.0.0.1:8000/posts"
    payload = json.dumps(
        {"title": fake.sentence(), "content": fake.text(), "published": True, "rating": 0}
    )
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NTMxNTcwMzh9.iSrTy5j_m23sgFBK9KKtZb4n9HsOJrTc_dyig2eHTlk',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


for i in range(15):
    create_post()

