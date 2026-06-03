from fastapi import FastAPI

app = FastAPI(title="MIS CloudOps Dashboard")


@app.get("/")
def root():
    return {
        "message": "Welcome to MIS CloudOps Dashboard",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mis-cloudops-dashboard"
    }