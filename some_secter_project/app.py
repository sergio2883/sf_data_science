# импортируем требуемые модули 
from typing import Optional
from fastapi import FastAPI


# создаём приложение FastAPI
app = FastAPI()

#регистрируем обработчик для стартовой страницы
@app.get("/")
async def read_root():
   return {"Hello": "World"}


#регистрируем обработчик для конкретной страницы
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}  