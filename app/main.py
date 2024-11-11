from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def welcome() -> dict:
    return {
        'project': 'ReferralAPI',
        'author': 'Kornev Stepan',
        'GitHub': 'https://github.com/stepkacorporation/ReferralAPI.git'
    }
