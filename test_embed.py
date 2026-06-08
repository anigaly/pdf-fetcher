import requests

url = "http://dgx-spark.waveaccess.ru:2347/embed"

response = requests.post(
    url,
    json={"inputs": ["test"]},
    timeout=90,
)

print("Status:", response.status_code)

data = response.json()

print(type(data))

if isinstance(data, list):
    print("Embedding size:", len(data[0]))
else:
    print(data)
