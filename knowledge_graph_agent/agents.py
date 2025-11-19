from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types
from knowledge_graph_agent.graph_tools import add_triplet, get_graph_state, save_graph_image

# Retry config for robustness
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# 1. Research Agent: The Librarian
research_agent = LlmAgent(
    name="ResearchAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    You are an expert researcher. Your goal is to provide a comprehensive but concise summary of the user's topic.
    Focus on identifying key entities and their relationships.
    Output clear, factual text that can be easily parsed into a knowledge graph.
    """,
)

# 2. Ontology Agent: The Structurer
ontology_agent = LlmAgent(
    name="OntologyAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    You are a Knowledge Graph Ontology expert.
    Your task is to read the provided research text and extract structured knowledge triplets.
    
    Use the `add_triplet` tool to save every important relationship you find.
    - Subject: The source entity
    - Predicate: The relationship (keep it short, e.g., "is_a", "located_in", "authored_by")
    - Object: The target entity
    
    Extract as many meaningful triplets as possible to build a rich graph.
    Finally, call `get_graph_state` and **include the full JSON output in your final response** so the next agent can use it.
    """,
    tools=[add_triplet, get_graph_state]
)

# 3. Visualization Agent: The Artist (Code Execution)
viz_agent = LlmAgent(
    name="VisualizationAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    You are a Data Visualization expert.
    Your goal is to visualize the Knowledge Graph that has been built.
    
    Simply call the `save_graph_image` tool to generate and save the visualization.
    You do not need to write any code, just use the tool.
    """,
    tools=[save_graph_image]
)
