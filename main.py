from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet= "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

@app.get("/models/{model_name}") # パスオペレーションデコレータを記述
async def get_model(model_name: ModelName): # パスオペレーション関数を定義
    if model_name is ModelName.alexnet:
        return {"mode_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "resnet":
        return {"mode_name": model_name, "message": "LeCNN all the images"}
    
    return {"mode_name": model_name, "message": "Have some residuals"}

@app.get("/files/{path:path}")
async def read_file(path: str):
    return {"file_path": path}