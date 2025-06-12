from fastapi import APIRouter
from fastapi import Query
from database import item_database
from model.item import Item

router = APIRouter()


@router.post("/insert_item/")
def insert_item(item: Item):
    try:
        if item.name is None or not item.name:
            return {
                "status": 400,
                "message": "Name is required",
                "data": None
            }
        if item.description is None or not item.description:
            return {
                "status": 400,
                "message": "Description is required",
                "data": None
            }
        item = item_database.insert_item(item)
        return {
            "status": 200,
            "message": "Success insert item",
            "data": item
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in insert_item:{str(e)}',
            "data": None
        }


@router.get("/get_items/")
def get_items(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    try:
        items = item_database.get_items(limit, offset)
        return {
            "status": 200,
            "message": "Success get items",
            "data": items
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in get_items:{str(e)}',
            "data": None
        }


@router.get("/get_item/{item_id}")
def get_item(item_id: int):
    try:
        item = item_database.get_item(item_id)
        if item is None:
            return {
                "status": 400,
                "message": "Item not found",
                "data": None
            }
        return {
            "status": 200,
            "message": "Success get item",
            "data": item
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in get_items:{str(e)}',
            "data": None
        }


@router.put("/update_item/{item_id}")
def update_item(item_id: int, item: Item):
    try:
        temp = item_database.get_item(item_id)
        if temp is None:
            return {
                "status": 400,
                "message": "Item not found",
                "data": None
            }
        item = item_database.update_item(item_id, item)
        if isinstance(item, bool):
            return {
                "status": 400,
                "message": "Item not update",
                "data": None
            }
        return {
            "status": 200,
            "message": "Success update item",
            "data": item
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in update_item:{str(e)}',
            "data": None
        }

@router.delete("/delete_item/{item_id}")
def delete_item(item_id: int):
    try:
        item = item_database.get_item(item_id)
        if item is None:
            return {
                "status": 400,
                "message": "Item not found",
                "data": None
            }
        status = item_database.delete_item(item_id)
        if not status:
            return {
                "status": 400,
                "message": "Item not delete",
                "data": None
            }
        else:
            return {
                "status": 200,
                "message": "Success delete item",
                "data": None
            }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in delete_item:{str(e)}',
            "data": None
        }