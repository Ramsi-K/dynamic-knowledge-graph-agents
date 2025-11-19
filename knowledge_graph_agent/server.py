from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import base64
from knowledge_graph_agent.main import run_agent

app = FastAPI(title="Dynamic Knowledge Graph Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files are no longer needed as we use Streamlit
# app.mount("/static", StaticFiles(directory="knowledge_graph_agent/static"), name="static")

class GenerateRequest(BaseModel):
    topic: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/generate")
async def generate_graph(request: GenerateRequest):
    try:
        # Run the agent
        result = await run_agent(request.topic)
        
        # Read the generated image and encode to base64
        image_path = result.get("image_path")
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                result["image_base64"] = encoded_string
        else:
            result["image_base64"] = None
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
