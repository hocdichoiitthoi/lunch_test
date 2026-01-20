# src/agent.py
import os
# Kích hoạt MONITORING (LangSmith)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__..." # Key của bạn

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Giả lập gRPC Client (Trong thực tế, đây là code gọi sang server khác bằng Protocol Buffers)
class MockGRPCCalculator:
    def sum_values(self, numbers):
        print("--- Đang gọi gRPC tới Calculator Microservice ---")
        return sum(numbers)

grpc_client = MockGRPCCalculator()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def run_agent_logic(chat_logs: str):
    # Bước 1: Agent phân tích text để ra danh sách số tiền
    prompt = ChatPromptTemplate.from_template(
        "Trích xuất danh sách số tiền các món ăn từ đoạn chat này dưới dạng list Python: {chat_logs}"
    )
    chain = prompt | llm
    
    # MONITORING: Bước này sẽ hiện trên LangSmith (Input/Output/Latency)
    ai_response = chain.invoke({"chat_logs": chat_logs})
    
    # Giả sử AI trả về text "[35000, 40000, 50000]"
    # Ta convert string đó thành list (Code minh họa đơn giản)
    import ast
    try:
        money_list = ast.literal_eval(ai_response.content)
    except:
        money_list = [0]

    # Bước 2: Gọi gRPC để tính tổng (Thay vì tự tính)
    # Tại sao dùng gRPC? Vì giả sử đây là phép tính siêu phức tạp cần server riêng
    total_cost = grpc_client.sum_values(money_list)
    
    return {
        "breakdown": money_list,
        "total": total_cost,
        "note": "Processed by AI + gRPC Calculator"
    }