import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types

# Load environment variables from .env file
load_dotenv()

from knowledge_graph_agent.architect import graph_architect
from knowledge_graph_agent.observability import GraphBuilderPlugin
from knowledge_graph_agent.graph_tools import kb

# Ensure API key is set (should be in environment from notebook setup)
if "GOOGLE_API_KEY" not in os.environ:
    print("⚠️ Warning: GOOGLE_API_KEY not found in environment variables.")

async def run_agent(topic: str):
    print(f"🚀 Initializing Dynamic Knowledge Graph Architect for topic: {topic}...")
    
    # Reset the knowledge base for a fresh run
    kb.reset()
    
    # 1. Setup Services
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    graph_plugin = GraphBuilderPlugin()
    
    # 2. Create Runner
    runner = Runner(
        agent=graph_architect,
        app_name="KnowledgeGraphApp",
        session_service=session_service,
        memory_service=memory_service,
        plugins=[graph_plugin]
    )
    
    # 3. Create Session
    session = await session_service.create_session(
        app_name="KnowledgeGraphApp",
        user_id="user_1",
        session_id="session_1"
    )
    
    # 4. Run Agent
    print(f"\n🎯 Topic: {topic}")
    print("-" * 60)
    
    user_msg = types.Content(parts=[types.Part(text=f"Build a knowledge graph about: {topic}")])
    
    final_response_text = ""
    
    async for event in runner.run_async(
        user_id="user_1",
        session_id="session_1",
        new_message=user_msg
    ):
        # Capture the agent's output
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text)
                    final_response_text += part.text + "\n"
                    
    print("-" * 60)
    print("📊 Final Stats:")
    stats = graph_plugin.get_stats()
    graph_state = kb.get_state()
    print(stats)
    
    # The image path is now dynamic, but for the API we might just return the latest one
    # or we can rely on the tool output if we captured it. 
    # For simplicity, let's assume the tool saved it and we can find the latest file in examples/
    # OR better, let's just return the graph state and let the frontend handle visualization if needed,
    # but the user wants the PNG download too.
    # Since save_graph_image returns the filename, we could capture it if we were calling it directly,
    # but here the agent calls it.
    # We'll find the most recent file in examples/
    
    import glob
    list_of_files = glob.glob('examples/*.png') 
    latest_file = max(list_of_files, key=os.path.getctime) if list_of_files else None

    return {
        "summary": final_response_text,
        "stats": stats,
        "graph_state": graph_state,
        "image_path": latest_file
    }

if __name__ == "__main__":
    topic = "The relationships between the main characters in Harry Potter"
    asyncio.run(run_agent(topic))
