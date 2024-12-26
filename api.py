import asyncio
from fastapi import FastAPI, BackgroundTasks, WebSocket
from pydantic import BaseModel
from parser import get_all_products
from starlette.concurrency import run_in_threadpool
from starlette.websockets import WebSocketDisconnect
from sqlmodel import Field, SQLModel, create_engine, Session, select
import json

# Настройка FastAPI и подключения к базе данных
app = FastAPI()
sqlite_url = "sqlite:///parser.db"
engine = create_engine(sqlite_url)
website_url = "https://ekaterinburg.technopark.ru/smartfony/samsung/"

# Менеджер WebSocket-соединений
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Модель данных для товаров
class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    myindex: str
    name: str
    price: int

class ItemBase(BaseModel):
    myindex: str
    name: str
    price: int

# Создание таблиц БД, если они не существуют
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()

# Функция для добавления товара в БД
def add_item(title, price, index):
    item = Item(myindex=str(index), name=title, price=price)
    
    with Session(engine) as session:
        existing_item = session.exec(select(Item).filter(Item.myindex == str(index))).first()
        if not existing_item:
            session.add(item)
            session.commit()

# Асинхронная функция для парсинга товаров
async def background_parser_async():
    while True:
        print("Starting to get prices...")
        await asyncio.sleep(12 * 60 * 60)
        await run_in_threadpool(get_all_products, website_url)

# Функция для добавления товаров в БД
def background_add_item():
    products = get_all_products(website_url)
    for index, product in enumerate(products):
        title = product['Название']
        price = product['Цена']
        add_item(title, price, index)

# Эндпоинты API для работы с товарами
# Запуск парсера и добавление товаров в фоновом режиме
@app.get("/start_parser")
async def start_parser(background_tasks: BackgroundTasks):
    asyncio.create_task(background_parser_async())
    background_tasks.add_task(background_add_item)
    return {}

# Получение списка всех товаров
@app.get("/prices")
async def read_prices():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
    return items

# Получение товара по ID
@app.get("/prices/{item_id}")
async def read_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if item:
            return item
    return {"error": "Item not found"}

# Обновление данных о товаре
@app.put("/prices/{item_id}")
async def update_item(item_id: int, data: ItemBase):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if item:
            item.name = data.name
            item.price = data.price
            session.commit()

            print({"myindex": item.myindex, "name": item.name, "price": item.price, "id": item.id})
            
            await manager.broadcast(f'Updated item: {json.dumps(item.dict())}')
            return item
    return {"error": "Item not found"}

# Создание нового товара
@app.post("/prices/create")
async def create_item(item: ItemBase):
    new_item = Item(myindex=item.myindex, name=item.name, price=item.price)
    with Session(engine) as session:
        session.add(new_item)
        session.commit()
        session.refresh(new_item)
        await manager.broadcast(f'Created new item: {new_item.model_dump_json()}')
    return new_item

# Удаление товара по ID
@app.delete("/prices/{item_id}")
async def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if item:
            session.delete(item)
            session.commit()
            await manager.broadcast(f'Deleted item: {item.model_dump_json()}')
            return {"status": "ok"}
    return {"error": "Item not found"}

# Обработка WebSocket-соединений
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message from client: {data}")
            await websocket.send_text(data * 10)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client {websocket} disconnected")