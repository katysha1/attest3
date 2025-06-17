from fastapi import FastAPI

app = FastAPI()

@app.get("/greet")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}
