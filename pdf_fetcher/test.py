import requests

response = requests.post(
    "http://dgx-spark.waveaccess.ru:2347/embed",
    json={"text": "anemia treatment"},
)

print(response.json())
