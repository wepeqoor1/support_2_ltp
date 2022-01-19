import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers import views
import uvicorn


app = FastAPI()

origins = [
    "http://10.49.5.31:8000",
            ]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(views.router)


@app.get("/")
def main():
    return FileResponse("app/web/dist/index.html")


app.mount("/static", StaticFiles(directory="app/web/dist/"))
uvicorn.run(app, host="0.0.0.0", port=8000, debug=False)
