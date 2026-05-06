from fastapi import Request, FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
from util import verify_hmac, generate_hmac
from base64 import b64decode

app = FastAPI()

db: Dict[int, Dict[str, str]] = {}

class Memo(BaseModel):
    title: str
    content: str

class Item(BaseModel):
    secret_key: str
    path :str

class MemoDetailResponse(BaseModel):
    id:      int
    title:   str
    content: str

current_id = 1

async def hmac_validator(req: Request):
    signature = req.headers.get("X-Authorization")
    if not signature:
        raise HTTPException(status_code=401, detail="Missing X-Authorization header")
    
    path = req.url.path

    if not req.cookies.get("auth"):
        raise HTTPException(status_code=401, detail="Missing Auth cookie")
    
    SECRET_KEY = b64decode(req.cookies.get("auth").encode()).decode()

    if (SECRET_KEY == 'admin'):
        raise HTTPException(status_code=403, detail="Admin privileges are not allowed")
    
    if not verify_hmac(path, signature):
        raise HTTPException(status_code=403, detail="Invalid HMAC signature")


async def check_auth(req: Request):
    if b64decode(req.cookies.get("auth").encode()).decode() == 'guest':
        raise HTTPException(status_code=403, detail="Do not have permission")


@app.post("/api/v1/admin/register", response_model=Dict[str, str], dependencies=[Depends(hmac_validator),Depends(check_auth)])
async def create_memo(memo: Memo):
    global current_id
    db[current_id] = {"id": current_id, "title": memo.title, "content": memo.content}
    response = {"message": "Memo created successfully", "id": str(current_id)}
    current_id += 1
    return response


@app.get("/api/v1/admin/flag", response_model=Dict[str, str], dependencies=[Depends(hmac_validator), Depends(check_auth)])
async def flag():
    with open('/flag') as f:
        try: 
            FLAG = f.read().strip()
        except:
            FLAG = 'DH{test}'
    response = {"message": FLAG}
    return response

@app.post("/api/v1/admin/getSignature", response_model=Dict[str, str])
async def get_signature(item: Item):
    signature = generate_hmac(item.secret_key, item.path)
    response = {"message": signature}
    return response


@app.put("/api/v1/admin/{memo_id}", response_model=Dict[str, str], dependencies=[Depends(hmac_validator),Depends(check_auth)])
async def update_memo(memo_id: int, memo: Memo):
    if memo_id not in db:
        raise HTTPException(status_code=404, detail="Memo not found")
    
    db[memo_id]["title"] = memo.title
    db[memo_id]["content"] = memo.content
    return {"message": "Memo updated successfully", "id": str(memo_id)}


@app.delete("/api/v1/admin/{memo_id}", response_model=Dict[str, str], dependencies=[Depends(hmac_validator),Depends(check_auth)])
async def delete_memo(memo_id: int):
    if memo_id not in db:
        raise HTTPException(status_code=404, detail="Memo not found")
    
    del db[memo_id]
    return {"message": "Memo deleted successfully", "id": str(memo_id)}


@app.post("/api/v1/guest/register", response_model=Dict[str, str], dependencies=[Depends(hmac_validator)])
async def create_memo(memo: Memo):
    global current_id
    db[current_id] = {"id": current_id, "title": memo.title, "content": memo.content}
    response = {"message": "Memo created successfully", "id": str(current_id)}
    current_id += 1
    return response


@app.get("/api/v1/guest/show/{memo_id}", response_model=MemoDetailResponse, dependencies=[Depends(hmac_validator)])
async def get_memo_detail(memo_id: int):
    if memo_id not in db:
        raise HTTPException(status_code=404, detail="Memo not found")
    return db[memo_id]
