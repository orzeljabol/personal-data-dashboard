from fastapi import FastAPI

app = FastAPI(title="Personal Data Dashboard (V1)")

@app.get("/")
def root():
    return {"Hello world"}
