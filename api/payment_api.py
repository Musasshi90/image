from fastapi import APIRouter, Request, Form
from database import payment_database
from model.payment import Payment

router = APIRouter()


@router.post("/insertTransaction")
async def insert_transaction(request: Request):
    try:
        item = Payment()
        try:
            data = await request.json()
            item.accountId = data.get("accountId")
            item.botToken = data.get("botToken")
            item.amount = data.get("amount")
            item.currency = data.get("currency")
            item.title = data.get("title")
            item.referenceCode = data.get("referenceCode")
            item.smsUniqueCode = data.get("smsUniqueCode")
            item.remitter = data.get("remitter")
            item.content = data.get("content")
        except Exception:
            # Fallback to form data
            form = await request.form()
            item.accountId = form.get("accountId")
            item.botToken = form.get("botToken")
            item.amount = form.get("amount")
            item.currency = form.get("currency")
            item.title = form.get("title")
            item.referenceCode = form.get("referenceCode")
            item.smsUniqueCode = form.get("smsUniqueCode")
            item.remitter = form.get("remitter")
            item.content = form.get("content")
        if item.accountId is None or not item.accountId:
            return {
                "status": 400,
                "message": "Account id is required",
                "data": None
            }
        if item.botToken is None or not item.botToken:
            return {
                "status": 400,
                "message": "Bot token is required",
                "data": None
            }
        if item.amount is None or not item.amount:
            return {
                "status": 400,
                "message": "Amount is required",
                "data": None
            }
        if item.referenceCode is None or not item.referenceCode:
            return {
                "status": 400,
                "message": "Reference code is required",
                "data": None
            }
        if item.smsUniqueCode is None or not item.smsUniqueCode:
            return {
                "status": 400,
                "message": "Sms unique code code is required",
                "data": None
            }
        if item.remitter is None or not item.remitter:
            return {
                "status": 400,
                "message": "Remitter is required",
                "data": None
            }
        if item.content is None or not item.content:
            return {
                "status": 400,
                "message": "Content is required",
                "data": None
            }
        if item.title is None or not item.title:
            return {
                "status": 400,
                "message": "Title is required",
                "data": None
            }
        item = payment_database.insert_payment(item, False)
        return {
            "status": 200,
            "message": "Success insert transaction ",
            "data": item
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in insert_transaction:{str(e)}',
            "data": None
        }


@router.post("/insertSmsTransaction")
async def insert_sms_transaction(request: Request):
    try:
        item = Payment()
        try:
            data = await request.json()
            item.accountId = data.get("accountId")
            item.botToken = data.get("botToken")
            item.amount = data.get("amount")
            item.currency = data.get("currency")
            item.title = data.get("title")
            item.referenceCode = data.get("referenceCode")
            item.smsUniqueCode = data.get("smsUniqueCode")
            item.remitter = data.get("remitter")
            item.content = data.get("content")
        except Exception:
            # Fallback to form data
            form = await request.form()
            item.accountId = form.get("accountId")
            item.botToken = form.get("botToken")
            item.amount = form.get("amount")
            item.currency = form.get("currency")
            item.title = form.get("title")
            item.referenceCode = form.get("referenceCode")
            item.smsUniqueCode = form.get("smsUniqueCode")
            item.remitter = form.get("remitter")
            item.content = form.get("content")
        if item.accountId is None or not item.accountId:
            return {
                "status": 400,
                "message": "Account id is required",
                "data": None
            }
        if item.botToken is None or not item.botToken:
            return {
                "status": 400,
                "message": "Bot token is required",
                "data": None
            }
        if item.amount is None or not item.amount:
            return {
                "status": 400,
                "message": "Amount is required",
                "data": None
            }
        if item.referenceCode is None or not item.referenceCode:
            return {
                "status": 400,
                "message": "Reference code is required",
                "data": None
            }
        if item.smsUniqueCode is None or not item.smsUniqueCode:
            return {
                "status": 400,
                "message": "Sms unique code code is required",
                "data": None
            }
        if item.remitter is None or not item.remitter:
            return {
                "status": 400,
                "message": "Remitter is required",
                "data": None
            }
        if item.content is None or not item.content:
            return {
                "status": 400,
                "message": "Content is required",
                "data": None
            }
        if item.title is None or not item.title:
            return {
                "status": 400,
                "message": "Title is required",
                "data": None
            }
        item = payment_database.insert_payment(item, True)
        return {
            "status": 200,
            "message": "Success insert sms transaction",
            "data": item
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in insert_sms_transaction:{str(e)}',
            "data": None
        }


@router.post("/checkTransaction")
async def check_transaction(request: Request):
    try:
        item = Payment()
        try:
            data = await request.json()
            item.accountId = data.get("accountId")
            item.smsUniqueCode = data.get("smsUniqueCode")
        except Exception:
            # Fallback to form data
            form = await request.form()
            item.accountId = form.get("accountId")
            item.smsUniqueCode = form.get("smsUniqueCode")
        item = payment_database.get_payment(item.accountId, item.smsUniqueCode, False)
        if item is None:
            return {
                "status": 200,
                "message": "Ok to use",
                "data": None
            }
        return {
            "status": 400,
            "message": "Payment exist",
            "data": item
        }
    except Exception as e:
        return {
            "status": 500,
            "message": f'Error happen in check_transaction:{str(e)}',
            "data": None
        }
