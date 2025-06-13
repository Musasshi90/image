from pydantic import BaseModel


class Payment(BaseModel):
    id: int = None
    remitter: str = None
    botToken: str = None
    accountId: str = None
    referenceCode: str = None
    currency: str = None
    amount: float = None
    title: str = None
    smsUniqueCode: str = None
    content: str = None
