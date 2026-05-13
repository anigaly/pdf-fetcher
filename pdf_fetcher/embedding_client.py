import time
import requests


class EmbeddingClient:
    def __init__(self):
        self.url = "http://dgx-spark.waveaccess.ru:2347/embed"

    def embed(self, text: str) -> list[float]:

        for attempt in range(3):
            try:
                response = requests.post(
                    self.url,
                    json={"inputs": [text]},
                    timeout=120,
                )

                response.raise_for_status()

                data = response.json()

                # [[...]]
                if isinstance(data, list):
                    return data[0]

                # {"embeddings": [[...]]}
                if "embeddings" in data:
                    return data["embeddings"][0]

                # {"embedding": [...]}
                if "embedding" in data:
                    return data["embedding"]

                raise ValueError(f"Unknown response: {data}")

            except Exception as e:
                print(f"Embedding error (attempt {attempt + 1}): {e}")

                time.sleep(5)

        raise RuntimeError("Failed to get embedding after retries")
