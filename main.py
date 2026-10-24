from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def home():
    return {"message":"Job API tracker is running"}