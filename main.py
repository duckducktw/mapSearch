from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, StreamingResponse
import httpx
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Map Search API Proxy"}

@app.get("/search")
async def search(keyword: str, loc: str = "25.09108,121.5598"):
    response = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={loc}&radius=1500&keyword={keyword}&language=zh-TW&key={GOOGLE_API_KEY}").json()['results']
    result = []
    for place in response:
        place_info = {
            "name": place.get("name"),
            "address": [place["geometry"]["location"]["lng"],
                        place["geometry"]["location"]["lat"]],
            "photo": "/photo/" + place.get("photos")[0].get("photo_reference") if place.get("photos") else None
        }
        result.append(place_info)
    return result

@app.get("/photo")
async def get_place_photo(photo_reference: str, max_width: int = 400):
    if not GOOGLE_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server API Key not configured. Please set GOOGLE_API_KEY environment variable."
        )

    google_photo_url = (
        f"https://maps.googleapis.com/maps/api/place/photo?"
        f"maxwidth={max_width}&"
        f"photoreference={photo_reference}&"
        f"key={GOOGLE_API_KEY}"
    )

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(google_photo_url, follow_redirects=True)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            return StreamingResponse(
                content=response.aiter_bytes(chunk_size=8192),
                media_type=content_type,
                status_code=response.status_code
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error connecting to Google API: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error from Google API: {e.response.text} (Status: {e.response.status_code})"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {str(e)}"
            )