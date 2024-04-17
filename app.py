from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def hello_world():
    return "Hello,World"

@app.get("/responses/{response_id}")
async def get_response(response_id):
    return {"response_id": response_id}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)