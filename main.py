from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import api.item_api as item_api
import api.image_api as image_api
import api.payment_api as payment_api
import constant
import database.item_database as item_database
import database.image_database as image_database
import database.payment_database as payment_database

app = FastAPI()

# Mount static files so uploaded images can be served
if constant.USE_LOCAL_DB:
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routers
app.include_router(image_api.router)
app.include_router(item_api.router)
app.include_router(payment_api.router)

item_database.create_table()
image_database.create_table()
payment_database.create_table()


# Optional root route
@app.get("/")
def read_root():
    return {"message": "API is running"}
