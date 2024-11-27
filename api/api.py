import asyncio
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from parser import get_all_products
from starlette.concurrency import run_in_threadpool
from sqlmodel import Field, SQLModel, create_engine, Session, select

app = FastAPI()
sqlite_url = "sqlite:///parser.db"
engine = create_engine(sqlite_url)

class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    myindex: str
    name: str
    price: int

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

create_db_and_tables()

class ItemBase(BaseModel):
    myindex: str
    name: str
    price: int

def add_item(title, price, index):
    item = Item(myindex=str(index), name=title, price=price)
    
    with Session(engine) as session:
        existing_item = session.exec(select(Item).filter(Item.myindex == str(index))).first()
        if not existing_item:
            session.add(item)
            session.commit()

# Асинхронный парсер для получения и обработки товаров
async def background_parser_async():
    while True:
        print("Starting to get prices...")
        await asyncio.sleep(12 * 60 * 60)
        products = await run_in_threadpool(get_all_products, "https://ekaterinburg.technopark.ru/smartfony/samsung/")
        for index, product in enumerate(products):
            title = product['Название']
            price = product['Цена']
            print(f"Adding {title} - {price} to the database...")
            add_item(title, price, index)

# Функция для обработки получения товаров в синхронном режиме
def background_add_item():
    products = get_all_products("https://ekaterinburg.technopark.ru/smartfony/samsung/")
    for index, product in enumerate(products):
        title = product['Название']
        price = product['Цена']
        add_item(title, price, index)

# Эндпоинт для старта парсера
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_parser_async())

# Эндпоинты API для работы с товарами
@app.get("/start_parser")
async def start_parser(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_add_item)
    return {}

@app.get("/prices_sync")
async def read_prices():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
    return items

@app.get("/prices_async")
async def read_prices_async():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
    return items

@app.get("/prices/{item_id}")
async def read_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
    return item

@app.put("/prices/{item_id}")
async def update_item(item_id: int, data: ItemBase):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if item:
            item.name = data.name
            item.price = data.price
            session.commit()
            return item
    return {"error": "Item not found"}

@app.post("/prices/create")
async def create_item(item: ItemBase):
    new_item = Item(myindex=item.myindex, name=item.name, price=item.price)
    with Session(engine) as session:
        session.add(new_item)
        session.commit()
        session.refresh(new_item)
    return new_item

@app.delete("/prices/{item_id}")
async def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if item:
            session.delete(item)
            session.commit()
            return {"status": "ok"}
    return {"error": "Item not found"}