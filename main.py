from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
import os
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

app = FastAPI(title="AI Trip Planner API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "AI Trip Planner API is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(f"Received query: {query.question}")
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()
        
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        
        # Prepare messages for the AI
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        # Extract the AI response
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        print(f"AI Response: {final_output[:100]}...")  # Log first 100 chars
        return {"answer": final_output}
        
    except Exception as e:
        print(f"Error in query_travel_agent: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Trip Planner API...")
    print("📡 API will be available at: http://localhost:8000")
    print("🔍 Health check: http://localhost:8000/health")
    print("💬 Chat endpoint: http://localhost:8000/query")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )