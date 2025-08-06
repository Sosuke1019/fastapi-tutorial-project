from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing_extensions import Annotated, Literal

# class ModelName(str, Enum):
#     alexnet= "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

app = FastAPI()

# # ボディ -ネストされたモデル
# class Image(BaseModel):
#     url: HttpUrl
#     name: str

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()
#     image: list[Image] | None = None

# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     items: list[Item]

# @app.post("/index-weights/")
# async def create_index_weights(weights: dict[int, float]):
#     return weights

# @app.post("/images/multiple")
# async def create_multiple_images(image: list[Image]):
#     return image

# @app.post("/offers/")
# async def create_offer(offer: Offer):
#     return {"offer": offer}

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"アイテムid": item_id, "アイテム": item}
#     return results

# # ボディ -フィールド
# class Item(BaseModel):
#     name: str
#     description: str | None = Field(
#         default=None, title="The description of the item", max_length = 300
#     ),
#     price: float = Field(gt=0, description="The price must be greater than zero")
#     tax: float | None = None

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
#     results = {"アイテムid": item_id, "アイテム": item}
#     return results

# # ボディ -複数のパラメーター
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Annotated[Item, Body()]):
#     results = {"item_id": item_id, "item": item}
#     return results


# # クエリパラメータモデル
# class FilterParams(BaseModel):
#     model_config = {"extra": "forbid"}

#     limit: int = Field(100, gt=0, le=100)
#     offset: int = Field(0, ge=0)
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     tags: list[str] = []

# @app.get("/items/")
# async def read_items(filter_query: Annotated[FilterParams, Query()]):
#     return filter_query


# # パスパラメータと数値の検証
# @app.get("/items/{item_id}")
# async def read_items2(
#     item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
#     q: str,
# ):
#     results = {"item-id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# # クエリパラメータと文字列の検証
# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(alias="item-query", deprecated=True)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# # # リクエストボディ
# # @app.post("/items/{item_id}")
# # # パラメータがPydanticモデル型で宣言された場合、リクエストボディとして解釈される
# # async def create_item(item_id: int, item: Item, q: str | None = None):
# #     item_dict = item.dict()
# #     if item.tax is not None:
# #         price_with_tax = item.price + item.tax
# #         item_dict.update({"price_with_tax": price_with_tax})
# #     return item_dict

# # # クエリパラメータ
# # fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# # @app.get("/users/{item_id}")
# # async def read_user_item(item_id: str, user_id: str, q: str | None = None):
# #     item = {"アイテム番号": item_id, "ユーザー番号" :user_id, "option": q}
# #     return item

# # # パスパラメータ
# # @app.get("/models/{model_name}") # パスオペレーションデコレータを記述
# # async def get_model(model_name: ModelName): # パスオペレーション関数を定義
# #     if model_name is ModelName.alexnet:
# #         return {"mode_name": model_name, "message": "Deep Learning FTW!"}
    
# #     if model_name.value == "resnet":
# #         return {"mode_name": model_name, "message": "LeCNN all the images"}
    
# #     return {"mode_name": model_name, "message": "Have some residuals"}

# # @app.get("/files/{path:path}")
# # async def read_file(path: str):
# #     return {"file_path": path}