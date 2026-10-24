from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def home():
    return {"message":"Job API tracker is running"}
@app.post("/applications")
def create_application():
    return {"message":"application created"}