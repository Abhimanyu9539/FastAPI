from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def get_root():
    return {"Message":"Hello World"}


@app.get("/items/{item_id}")
async def read_items(item_id:str, q:str | None = None):
    return {"item_id": item_id, "q":q}