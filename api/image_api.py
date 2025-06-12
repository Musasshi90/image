from fastapi import File, UploadFile, HTTPException, APIRouter, Request
from datetime import datetime
import httpx
import uuid
import shutil
import constant
from database import image_database
from model.image import Image

router = APIRouter()

# Use httpx client for REST API calls to Supabase
headers = {
    "apikey": constant.SUPABASE_KEY,
    "Authorization": f"Bearer {constant.SUPABASE_KEY}"
}


@router.post("/upload-image/")
async def upload_image(request: Request, file: UploadFile = File(...)):
    if constant.USE_LOCAL_DB:
        return await upload_image_save_local(request, file)
    else:
        return await upload_image_cloud(file)


async def upload_image_cloud(file: UploadFile = File(...)):
    # Generate unique filename with timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_name = f"{timestamp}_{file.filename}"

    # Upload to Supabase Storage
    upload_url = f"{constant.SUPER_BASE_URL}/storage/v1/object/{constant.STORAGE_BUCKET}/{file_name}"

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
        return {
            "status": upload_response.status_code,
            "message": f"Failed to upload image: {upload_response.text}",
            "data": None
        }

    # Public URL of the uploaded image
    public_url = f"{constant.SUPER_BASE_URL}/storage/v1/object/public/{constant.STORAGE_BUCKET}/{file_name}"

    created_date = datetime.utcnow().isoformat()
    item = Image(id=1, file_name=file_name, created_date=created_date, url=public_url)
    image = image_database.insert_image(item)
    return image


async def upload_image_save_local(request: Request, file: UploadFile = File(...)):
    # Validate file type (optional)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image type")

    # Generate unique filename
    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}_{file.filename}"
    file_path = constant.UPLOAD_DIR / filename

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create public URL
    public_url = f"/static/uploads/{filename}"

    # Save URL to DB
    created_date = datetime.utcnow().isoformat()
    item = Image(id=1, file_name=filename, created_date=created_date, url=public_url)
    image = image_database.insert_image(item)
    base_url = str(request.base_url).rstrip("/")
    image.url = f"{base_url}{public_url}"

    return image


@router.get("/get_image/{image_id}")
async def get_image(request: Request, image_id: int):
    try:
        item = image_database.get_image(image_id)
        if constant.USE_LOCAL_DB:
            item.url = str(request.base_url).rstrip("/") + item.url
        return {
            "status": 200,
            "message": "Success get mage",
            "data": item
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in get_image:{str(e)}',
            "data": None
        }
