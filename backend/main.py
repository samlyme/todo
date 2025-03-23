from fastapi import FastAPI, HTTPException

from backend.database import create_tables, drop_tables

app = FastAPI()


@app.get("/")
async def read_root():
    return {
        "message": "Hello, World!"
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post('/initdb')
async def initdb():
    try:
        drop_tables()
        create_tables()
        return {"message": "Tables dropped"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error {e}"
        )
