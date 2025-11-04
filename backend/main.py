from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.ai_debugger import analyze_code, analyze_project_dependencies

app = FastAPI()

# 🧩 Enable CORS (for frontend/extension access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🏁 Root route
@app.get("/")
def root():
    return {"message": "🚀 IntelliDebug Backend is running!"}


# 📥 Model for /debug route
class CodeInput(BaseModel):
    code: str


# 🧠 Static AI debugging endpoint (single code check)
@app.post("/debug")
async def debug_code(input_data: CodeInput):
    code = input_data.code.strip()
    if not code:
        return {"error": "No code provided"}
    result = analyze_code(code)
    return {"result": result}


# ⚙️ Project-level AI analysis (multiple file dependency check)
@app.post("/analyze_project")
async def analyze_project(files: dict):
    """
    files = {
        "index.js": "...code here...",
        "app.js": "...code here...",
        "utils.js": "...code here..."
    }
    """
    result = analyze_project_dependencies(files)
    return {"project_analysis": result}


# 💬 WebSocket (live debugging - while typing)
@app.websocket("/ws/debug")
async def websocket_debug(websocket: WebSocket):
    """
    Real-time debugging while user types code
    Frontend connects via ws://localhost:8000/ws/debug
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = analyze_code(data)
            await websocket.send_json({"feedback": response})
    except Exception as e:
        await websocket.close()
