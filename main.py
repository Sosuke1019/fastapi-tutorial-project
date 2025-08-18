from typing import Union, Dict, Any
from enum import Enum
from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi import FastAPI, Query, Body, Cookie, Header, Form, File, UploadFile, HTTPException, Request, status, Depends
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from typing_extensions import Annotated, Literal
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# # yieldを持つ依存関係
# # yeildはリソースの取得と解放を自動的に管理するための仕組み
# async def get_db():
#     # ①リクエスト処理前に実行される部分。データベースセッションを作成する。
#     db = DBSession()
#     # エンドポイント内でエラーが発生しても、正常に処理が完了しても確実にリソースが解放されるように、try-finallyを使う
#     try:
#         # ②ここで一時停止し、dbをエンドポイントに渡す。
#         yeild db
#     finally:
#         # ③ レスポンス送信後に実行される部分。リソースの解放処理を行う。
#         # ここではレスポンスはすでに送信済みのため、ここでのHTTPExceptionは意味ないので注意!
#         # HTTPExceptionを投げるなら、yeildの前か、エンドポイント内にする。
#         db.close()

# async def dependency_a():
#     dep_a = generate_dep_a()
#     try:
#         yield dep_a
#     finally:
#         dep_a.close()


# async def dependency_b(dep_a: Annotated[DepA, Depends(dependency_a)]):
#     dep_b = generate_dep_b()
#     try:
#         yield dep_b
#     finally:
#         dep_b.close(dep_a)


# async def dependency_c(dep_b: Annotated[DepB, Depends(dependency_b)]):
#     dep_c = generate_dep_c()
#     try:
#         yield dep_c
#     finally:
#         dep_c.close(dep_b)

# # path operation デコレータの依存関係
# async def verify_token(x_token: Annotated[str, Header()]):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

# async def verify_key(x_key: Annotated[str, Header()]):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key

# # dependenciesを利用することで認証ロジック(verify_token, verify_key)とビジネスロジック(read_items)を分離できる
# # 引数としてdependencies=[]を利用した場合、エンドポイント関数に返り値は渡されない
# # 一方で、引数としてDepends()を利用した場合、エンドポイント関数に返り値が渡される
# @app.get("/items", dependencies=[Depends(verify_token), Depends(verify_key)])
# async def read_items():
#     return [{"item": "Foo"}, {"item": "Bar"}]

# # サブ依存関係
# def query_extractor(q: str | None = None):
#     return q

# def query_or_cookie_extractor(
#     q: Annotated[str, Depends(query_extractor)],
#     last_query: Annotated[str|None, Cookie()] = None
# ):
#     if not q:
#         return last_query
#     return q

# @app.get("/items/")
# async def read_query(
#     query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
# ):
#     return {"q_or_cookie": query_or_default}

# # 依存関係としてのクラス
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# class CommonQueryParams:
#     def __init__(self, q: str | None = None, skip: int = 0, limit:int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit

# @app.get("/items/")
# async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
#     response = {}
#     if commons.q:
#         response.update({"q": commons.q})
#     items = fake_items_db[commons.skip: commons.skip + commons.limit]
#     response.update({"items": items})
#     return response

# # 依存関係 -最初のステップ
# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}

# @app.get("/items/")
# # 型情報（dict） と FastAPIのメタデータ（Depends） を組み合わせている
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons

# @app.get("/users/")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons

# # ボディ -更新
# class Item(BaseModel):
#     name: str | None = None
#     description: str | None = None
#     price: float | None = None
#     tax: float = 10.5
#     tags: list[str] = []

# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},

# }

# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]

# @app.patch("/items/{item_id}", response_model=Item)
# async def update_item(item_id: str, item: Item):
#     stored_item_data = items[item_id]
#     stored_item_model = Item(**stored_item_data)
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item

# # JSON互換エンコーダ
# fake_db = {}

# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description: str | None = None

# @app.put("/items/{id}")
# async def update_item(id: str, item: Item):
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[id] = json_compatible_item_data
#     return fake_db[id]

# # Path Operationの設定
# # Path Operationデコレータにパラメータを渡すことで、Path Operationのメタデータを簡単に設定・追加できる
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = set()

# @app.post("/items/", response_model=Item, tags=["items"], summary="Create an item", response_description="The created item")
# async def create_item(item: Item):
#     """
#     Create an item with all the information:

#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item

# @app.get("/elements/", tags=["items"], deprecated=True)
# async def read_elements():
#     return [{"item_id": "Foo"}]

# # エラーハンドリング
# class UnicornException(Exception):
#     def __init__(self, name: str):
#         self.name = name

# class Item(BaseModel):
#     title: str
#     size: int

# items = {"foo": "The Foo Wrestlers"}

# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f"OMG! An HTTP error!: {repr(exc)}")    
#     return await http_exception_handler(request, exc)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
#     )

# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code= 418,
#         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
#     )

# @app.post("/items/")
# async def create_item(item: Item):
#     return item

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3")
#     return {"item_id": item_id}

# # /unicorns/yoloをリクエストすると、path operationはUnicornExceptionをraiseする。しかし、これはunicorn_exception_handlerで処理される。
# @app.get("/unicorns/{name}")
# async def read_unicorn(name: str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}

# @app.get("/items-header/{item_id}")
# async def read_item_header(item_id: str):
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404, 
#             detail="Item not found",
#             headers={"X-Error": "There goes my error"}
#         )
#     return {"item": items[item_id]}

# # リクエストフォームとファイル
# @app.post("/files?")
# async def create_file(
#     file: Annotated[bytes, File()],
#     fileb: Annotated[UploadFile, File()],
#     token: Annotated[str, Form()],
# ):
#     return {
#         "filesize": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type
#     }

# # リクエストファイル
# @app.post("/files?")
# async def create_file(files: Annotated[list[bytes], File(description="A file read as bytes")]):
#     return {"file_size": [len(file) for file in files]}

# @app.post("/uploadfile/")
# async def create_upload_file(files: Annotated[list[UploadFile], File(description="A file read as UploadFile")]):
#     return {"filename": [file.filename for file in files]}

# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)

# # フォームモデル
# class FormData(BaseModel):
#     username: str
#     password: str
#     model_config = {"extra": "forbid"}

# @app.post("/login/")
# async def login(data: Annotated[FormData, Form()]):
#     return data

# # フォームデータ
# @app.post("/login/")
# async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
#     return {"username": username}

# # レスポンスステータスコード
# @app.post("/items/")
# async def create_item(name: str):
#     return {"name": name}

# # モデル -より詳しく
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None

# class UserIn(UserBase):
#     password: str

# class UserOut(UserBase):
#     pass

# class UserInDB(BaseModel):
#     hashed_password: str

# def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password

# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     # user_in.dict()でPydanticモデルを辞書に変換。**で辞書を関数の引数として展開。
#     # ※ UserIn には password フィールドがあるが、UserInDB には hashed_password フィールドしかない。**user_in.dict() で展開された password は、UserInDB のフィールドに存在しないため無視される。
#     #  ** （アスタリスク2つ）: Pythonの「辞書展開」（dictionary unpacking）演算子。辞書のキーと値のペアを、関数の引数として展開する。
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("User saved! ..not really")
#     return user_in_db

# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved

# class BaseItem(BaseModel):
#     description: str
#     type: str

# class CarItem(BaseItem):
#     type: str = "car"

# class PlaneItem(BaseItem):
#     type: str = "plane"
#     size: int

# items = {
#     "item1": {"description": "All my friends drive a low rider", "type": "car"},
#     "item2": {
#         "description": "Music is my aeroplane, it's my aeroplane",
#         "type": "plane",
#         "size": 5,
#     },
# }

# @app.get("/items/{imte_id}", response_model=Union[PlaneItem, CarItem])
# async def read_item(item_id: str):
#     return items[item_id]

# @app.get("/keyword_weights/", response_model=dict[str, float])
# async def read_keyword_weights():
#     return {"foo": 2.3, "bar": 3.4}

# # レスポンスモデル
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5
#     tags: list[str] = []

# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
#     "baz": {
#         "name": "Baz",
#         "description": "There goes my baz",
#         "price": 50.2,
#         "tax": 10.5,
#     },
# }

# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include={"name", "description"},
# )
# async def read_item_name(item_id: str):
#     return items[item_id]

# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
# async def read_item(item_id: str):
#     return items[item_id]

# # ヘッダーパラメータモデル
# class CommonHeaders(BaseModel):
#     model_config = {"extra": "forbid"}

#     host: str
#     save_data: bool
#     if_modified_since: str | None = None
#     traceparent: str | None = None
#     x_tag: list[str] = []

# @app.get("/items/")
# async def read_items(headers: Annotated[CommonHeaders, Header()]):
#     return {"headers": headers}

# # クッキーパラメータモデル
# class Cookies(BaseModel):
#     model_config = {"extra": "forbid"}

#     session_id: str
#     fatebook_tracker: str | None
#     googall_tracker: str | None = None

# @app.get("/items/")
# async def read_items(cookies: Annotated[Cookies, Cookie()]):
#     return {"cookies": cookies}

# # ヘッダーのパラメータ
# @app.get("/items/")
# async def read_items(user_agent: Annotated[str | None, Header()] = None):
#     return {"User-Agent": user_agent}

# # クッキーのパラメータ
# @app.get("/items/")
# async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
#     return {"ads_id": ads_id}

# スキーマの追加 -例
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_datetime: Annotated[datetime, Body()],
#     end_datetime: Annotated[datetime, Body()],
#     process_after: Annotated[timedelta, Body()],
#     repeat_at: Annotated[time | None, Body()] = None
# ):
#     start_process = start_datetime + process_after
#     duration = end_datetime - start_datetime
#     return {
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "process_after": process_after,
#         "repeat_at": repeat_at,
#         "start_process": start_process,
#         "duration": duration,
#     }

# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int, 
#     item: Annotated[
#         Item,
#         Body(
#             examples=[
#                 {
#                     "name": "hogehuga",
#                     "description": "A very nice Item",
#                     "price": 35.4,
#                     "tax": 3.2,
#                 }
#             ],
#         )
#     ]
    
# ):
#     results = {"item_id": item_id, "item": item}
#     return results

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

# # リクエストボディ
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# @app.post("/items/{item_id}")
# # パラメータがPydanticモデル型で宣言された場合、リクエストボディとして解釈される
# async def create_item(item_id: int, item: Item, q: str | None = None):
#     item_dict = item.dict()
#     if item.tax is not None:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# # クエリパラメータ
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/users/{item_id}")
# async def read_user_item(item_id: str, user_id: str, q: str | None = None):
#     item = {"アイテム番号": item_id, "ユーザー番号" :user_id, "option": q}
#     return item

# # パスパラメータ
# class ModelName(str, Enum):
#     alexnet= "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"

# @app.get("/models/{model_name}") # パスオペレーションデコレータを記述
# async def get_model(model_name: ModelName): # パスオペレーション関数を定義
#     if model_name is ModelName.alexnet:
#         return {"mode_name": model_name, "message": "Deep Learning FTW!"}
    
#     if model_name.value == "resnet":
#         return {"mode_name": model_name, "message": "LeCNN all the images"}
    
#     return {"mode_name": model_name, "message": "Have some residuals"}

# @app.get("/files/{path:path}")
# async def read_file(path: str):
#     return {"file_path": path}