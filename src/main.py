# src/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agent import run_agent_logic
from src.cache import check_cache, save_cache
import uvicorn

app = FastAPI(title="LunchMoney AI Agent")

# Định nghĩa dữ liệu đầu vào (REST Payload)
class ChatRequest(BaseModel):
    chat_logs: str
    request_id: str  # ID để định danh request phục vụ Caching

@app.get("/")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

# --- ĐÂY LÀ API ENDPOINT ---
@app.post("/calculate-lunch")
async def calculate_lunch(request: ChatRequest):
    # 1. CACHING: Kiểm tra xem request này đã xử lý chưa
    cached_result = check_cache(request.request_id)
    if cached_result:
        return {"source": "cache", "data": cached_result}

    # 2. Xử lý Logic (Gọi Agent)
    try:
        result = run_agent_logic(request.chat_logs)
        
        # 3. Lưu kết quả vào Cache
        save_cache(request.request_id, result)
        
        return {"source": "generated", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)