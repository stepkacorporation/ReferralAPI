from fastapi import FastAPI

from app import routers

app = FastAPI()


@app.get('/')
async def welcome() -> dict:
    return {
        'project': 'ReferralAPI',
        'author': 'Kornev Stepan',
        'GitHub': 'https://github.com/stepkacorporation/ReferralAPI.git'
    }


app.include_router(routers.auth.router)
app.include_router(routers.referral_code.router)
