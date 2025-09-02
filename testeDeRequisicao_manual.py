import requests

headers = {
    #"Authorization": "Bearer your_token_here"
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzU3Mzc1NDgxLCJ0aXBvIjoidXN1YXJpbyJ9.Xhv07say2BCVflUu1w37deQDb8OUYuRsVjqi9_EU8fo"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh_token", headers=headers)
print(requisicao)
print(requisicao.json())