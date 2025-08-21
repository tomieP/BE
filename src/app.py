from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from api.appraisals import router
from config import config

app = FastAPI(title="Watch Appraisers API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)