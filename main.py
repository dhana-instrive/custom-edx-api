from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

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

@app.get("/enroll")
async def enroll_user(course_id: str, csrf_token: str, session_id: str):
    try:
        data = {
            "course_id": course_id,
            "enrollment_action": "enroll"
        }
        redirect_url = f"http://apps.local.openedx.io/learning/course/{course_id}/home"
        headers = {
            "x-csrftoken": csrf_token,
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"csrftoken={csrf_token};sessionid={session_id}"
        }

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(
                "http://local.openedx.io/change_enrollment",
                headers=headers,
                data=data
            )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=response.text)

        # Redirect after successful enrollment
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
