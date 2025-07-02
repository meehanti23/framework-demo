from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio

app = FastAPI(title="Name Analysis API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DogImageResponse(BaseModel):
    imageUrl: str

@app.get("/api/random-dog", response_model=DogImageResponse)
async def get_random_dog():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://dog.ceo/api/breeds/image/random")
            data = response.json()
            
            return DogImageResponse(imageUrl=data["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dog image: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Name Analysis API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)