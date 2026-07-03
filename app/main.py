from fastapi import FastAPI

app = FastAPI(title="M-Motors API")

@app.get("/")
def read_root():
    return {"message": "API M-Motors opérationnelle"}
