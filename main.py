from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

class ModelName(str, Enum):
    alexnet= "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

# リクエストボディ
@app.post("/items/{item_id}")
# パラメータがPydanticモデル型で宣言された場合、リクエストボディとして解釈される
async def create_item(item_id: int, item: Item, q: str | None = None):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# クエリパラメータ
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/users/{item_id}")
async def read_user_item(item_id: str, user_id: str, q: str | None = None):
    item = {"アイテム番号": item_id, "ユーザー番号" :user_id, "option": q}
    return item

# パスパラメータ
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