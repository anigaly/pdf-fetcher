import pandas as pd
from pathlib import Path

data = [
    {"ID": "4_2", "Наименование": "Преждевременные роды"}
]

df = pd.DataFrame(data)

Path("data").mkdir(exist_ok=True)
df.to_excel("data/registry.xlsx", index=False, engine="openpyxl")

print("data/registry.xlsx created successfully")
