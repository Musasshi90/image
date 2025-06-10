from fastapi import FastAPI, File, UploadFile, HTTPException
from datetime import datetime
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Supabase config
SUPABASE_URL = os.getenv("SUPER_BASE_URL")
print("DEBUG - SUPABASE_KEY =", SUPABASE_URL)
SUPABASE_KEY = os.getenv("SUPER_BASE_API_KEY")
print("DEBUG - SUPABASE_KEY =", SUPABASE_KEY)
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "images")
print("DEBUG - STORAGE_BUCKET =", STORAGE_BUCKET)

# Use httpx client for REST API calls to Supabase
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Generate unique filename with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        file_name = f"{timestamp}_{file.filename}"

        # Upload to Supabase Storage
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET}/{file_name}"

        async with httpx.AsyncClient() as client:
            upload_response = await client.post(
                upload_url,
                content=await file.read(),
                headers={
                    **headers,
                    "Content-Type": file.content_type
                }
            )

        if upload_response.status_code not in (200, 201):
            raise HTTPException(
                status_code=upload_response.status_code,
                detail=f"Failed to upload image: {upload_response.text}"
            )

        # Public URL of the uploaded image
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET}/{file_name}"

        # Save metadata to Supabase table
        created_date = datetime.utcnow().isoformat()
        insert_data = {
            "file_name": file_name,
            "created_date": created_date,
            "url": public_url
        }

        insert_url = f"{SUPABASE_URL}/rest/v1/images"
        async with httpx.AsyncClient() as client:
            insert_response = await client.post(
                insert_url,
                json=insert_data,
                headers={
                    **headers,
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                }
            )

        if insert_response.status_code not in (200, 201):
            raise HTTPException(
                status_code=insert_response.status_code,
                detail=f"Failed to insert record: {insert_response.text}"
            )

        inserted_record = insert_response.json()[0]

        return {
            "status": 200,
            "message": "Success",
            "data": inserted_record
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/images/")
async def get_all_images():
    url = f"{SUPABASE_URL}/rest/v1/images?select=*"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch images", "detail": response.text}

    return {
        "status": 200,
        "message": "Success",
        "data": response.json()
    }

@app.get("/images/{image_id}")
async def get_image_by_id(image_id: int):  # change to str if UUID
    url = f"{SUPABASE_URL}/rest/v1/images?id=eq.{image_id}&select=*"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch image")

    data = response.json()

    if not data:
        raise HTTPException(status_code=404, detail="Image not found")

    return {
        "status": 200,
        "message": "Success",
        "data": data[0]
    }
