from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/ping')
async def ping_message():
    return {"msg": "success" }

@app.get("/redirect")
async def redirect_user():
    return RedirectResponse(url="http://apps.local.openedx.io/learner-dashboard/")