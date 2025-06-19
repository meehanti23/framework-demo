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

class NameRequest(BaseModel):
    name: str

class NameAnalysisResponse(BaseModel):
    name: str
    age: int | None
    gender: str | None
    probability: float | None
    countries: list

class DogImageResponse(BaseModel):
    imageUrl: str

@app.post("/api/analyze-name", response_model=NameAnalysisResponse)
async def analyze_name(request: NameRequest):
    try:
        name = request.name.strip()
        if not name:
            raise HTTPException(status_code=400, detail="Name is required")
        
        async with httpx.AsyncClient() as client:
            # Make parallel API calls
            tasks = [
                client.get(f"https://api.agify.io?name={name}"),
                client.get(f"https://api.genderize.io?name={name}"),
                client.get(f"https://api.nationalize.io?name={name}")
            ]
            
            age_response, gender_response, nationality_response = await asyncio.gather(*tasks)
            
            age_data = age_response.json()
            gender_data = gender_response.json()
            nationality_data = nationality_response.json()
            
            return NameAnalysisResponse(
                name=name,
                age=age_data.get("age"),
                gender=gender_data.get("gender"),
                probability=gender_data.get("probability"),
                countries=nationality_data.get("country", [])
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze name: {str(e)}")

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