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

# Ensure API key is set (should be in environment from notebook setup)
if "GOOGLE_API_KEY" not in os.environ:
    print("⚠️ Warning: GOOGLE_API_KEY not found in environment variables.")

async def main():
    print("🚀 Initializing Dynamic Knowledge Graph Architect...")
    
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
    
    # 4. Interactive Loop (or single run for demo)
    topic = "The relationships between the main characters in Harry Potter"
    print(f"\n🎯 Topic: {topic}")
    print("-" * 60)
    
    user_msg = types.Content(parts=[types.Part(text=f"Build a knowledge graph about: {topic}")])
    
    async for event in runner.run_async(
        user_id="user_1",
        session_id="session_1",
        new_message=user_msg
    ):
        # Print the agent's thought process and final response
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text)
                    
    print("-" * 60)
    print("📊 Final Stats:")
    print(graph_plugin.get_stats())
    print("\n✅ Done! Check for 'knowledge_graph.png' in the current directory.")

if __name__ == "__main__":
    asyncio.run(main())
