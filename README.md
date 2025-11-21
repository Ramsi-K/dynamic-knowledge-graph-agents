# Dynamic Knowledge Graph Architect

## 1. The Pitch

### Problem
We live in an age of information overload. While LLMs are great at summarizing text, they often produce linear, unstructured outputs that are hard to visualize or analyze structurally. Understanding complex systems—like the relationships in a novel, an ecosystem, or a corporate structure—requires more than just text; it requires a **map**.

### Solution
The **Dynamic Knowledge Graph Architect** is an AI agent pipeline that transforms unstructured natural language into structured, visual knowledge graphs. It doesn't just tell you about a topic; it **builds a map** of it.

By combining **Sequential Agents**, **Structured Ontology Extraction**, and **Code Execution**, this system:
1.  **Researches** a topic to find key entities.
2.  **Structures** the data into a formal Knowledge Graph (Nodes & Edges).
3.  **Visualizes** the result by writing and executing Python code to generate a high-quality image.

### Value
This tool bridges the gap between unstructured text and structured data visualization. It allows researchers, students, and analysts to instantly visualize complex relationships without manually drawing diagrams or writing code.

## 2. Demo

### Interactive UI
![Main Interface](assets/frontend.png)

### Visualization Styles
The agent supports multiple layout algorithms to best represent different types of data:

| Barnes Hut (Default) | Force Atlas 2 |
| :---: | :---: |
| ![Barnes Hut](assets/barnes_hut_viz.png) | ![Force Atlas](assets/force_atlas_viz.png) |

| Repulsion | Hierarchical (Mind Map) |
| :---: | :---: |
| ![Repulsion](assets/repulsion_viz.png) | ![Hierarchical](assets/heirarchical_viz.png) |

---

## 3. The Implementation

### Architecture
The system uses a **Sequential Multi-Agent Architecture** powered by the Google Agent Development Kit (ADK).

1.  **ResearchAgent** (The Librarian):
    -   **Role**: Gathers information and synthesizes a rich textual summary.
    -   **Model**: Gemini 2.5 Flash Lite.
    
2.  **OntologyAgent** (The Structurer):
    -   **Role**: Analyzes text and extracts structured triplets (Subject -> Predicate -> Object).
    -   **Tools**: `add_triplet`, `get_graph_state`.
    
3.  **VisualizationAgent** (The Artist):
    -   **Role**: Converts the graph state into a visual asset.
    -   **Capability**: **Code Execution**. It writes Python code using `networkx` and `matplotlib` to render the graph to a PNG file.

### Key Concepts Applied 
1.  **Multi-Agent System**: A sequential pipeline where each agent passes context to the next.
2.  **Tools & Code Execution**: Custom tools for graph management and the built-in `BuiltInCodeExecutor` for visualization.
3.  **Observability**: A custom `GraphBuilderPlugin` that tracks metrics (triplets added, graphs generated) and logs agent activities.

### File Structure
-   `app.py`: Streamlit frontend application.
-   `knowledge_graph_agent/`
    -   `main.py`: Backend logic and agent runner.
    -   `server.py`: FastAPI server for the backend.
    -   `architect.py`: Defines the `SequentialAgent` pipeline.
    -   `agents.py`: Configures the individual agents and their prompts.
    -   `graph_tools.py`: Implements the in-memory graph database and tools.
    -   `observability.py`: Custom plugin for metrics and logging.
-   `assets/`: Images for documentation.

---

## 4. How to Run

### Prerequisites
-   Python 3.10+
-   `uv` (recommended) or `pip`
-   `GOOGLE_API_KEY` set in your environment.

### Setup
```bash
# 1. Clone the repository
git clone https://github.com/Ramsi-K/dynamic-knowledge-graph-agents
cd dynamic-knowledge-graph-agents

# 2. Create a virtual environment and install dependencies
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install google-adk networkx matplotlib streamlit pyvis fastapi uvicorn requests

# 3. Run the Application
# Start the backend server
uv run python -m knowledge_graph_agent.server

# Start the Streamlit UI (in a new terminal)
uv run streamlit run app.py
```

### Output
Open your browser to `http://localhost:8501` to interact with the agent.
