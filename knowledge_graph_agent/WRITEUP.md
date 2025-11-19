# Kaggle Submission Writeup

**Title**: Dynamic Knowledge Graph Architect
**Subtitle**: Transforming Unstructured Thought into Structured Visual Maps
**Track**: Freestyle Track

## Project Description

### Problem Statement
In the era of Large Language Models, we have access to infinite information, but "understanding" often requires structure. Reading a 5-page summary of a complex ecosystem, a novel's plot, or a corporate hierarchy is inefficient. Humans understand complex systems best through **visual maps**, not linear text. Existing tools either require manual diagramming or are limited to pre-defined schemas.

### The Solution
The **Dynamic Knowledge Graph Architect** is an intelligent agent pipeline that automatically transforms natural language queries into structured, visual Knowledge Graphs. It doesn't just summarize; it **architects** a map of the information.

By simply asking "Explain the political structure of Dune," the agent:
1.  **Researches** the topic to identify key entities and relationships.
2.  **Structures** the data into a formal graph ontology (Nodes & Edges).
3.  **Visualizes** the result by writing and executing Python code to generate a high-quality image file.

### Architecture
The solution leverages the **Google Agent Development Kit (ADK)** to orchestrate a **Sequential Multi-Agent System**:

1.  **ResearchAgent (The Librarian)**: Uses Gemini 2.5 Flash Lite to synthesize a comprehensive summary of the user's topic, ensuring all key entities are identified.
2.  **OntologyAgent (The Structurer)**: A specialized agent that analyzes the research and extracts structured triplets (Subject -> Predicate -> Object) using custom tools (`add_triplet`). It builds the graph state in memory.
3.  **VisualizationAgent (The Artist)**: Demonstrates the power of **Code Execution**. It reads the graph state and writes a complete Python script (using `networkx` and `matplotlib`) to render the graph visually. This allows for infinite customization and perfect rendering of complex structures.

### Key Features (ADK Concepts)
*   **Multi-Agent System**: A sequential pipeline where agents pass context and refine data at each step.
*   **Tools & Code Execution**: Custom tools for graph state management and the built-in `BuiltInCodeExecutor` for generating the final visual asset.
*   **Observability**: A custom `GraphBuilderPlugin` tracks the "Knowledge Velocity" (triplets added per session) and logs agent activities for debugging.

### Value
This project demonstrates that Agents can be creators, not just talkers. By bridging the gap between unstructured text and structured visualization, the Knowledge Graph Architect empowers users to instantly grasp complex systems, making it a powerful tool for education, research, and systems analysis.

---

## Video Script Outline (For your 3-min video)

1.  **Intro (0:00-0:30)**: "Hi, I'm [Name]. LLMs are great at writing, but bad at mapping. Today I'm presenting the Knowledge Graph Architect."
2.  **The Problem (0:30-1:00)**: Show a wall of text. "This is hard to understand."
3.  **The Solution (1:00-2:00)**: Show the Agent running.
    *   "First, the Research Agent finds the facts."
    *   "Then, the Ontology Agent builds the structure."
    *   "Finally, the Viz Agent writes Python code to draw this..." -> **Reveal the generated Image**.
4.  **Architecture (2:00-2:30)**: Show a diagram of the 3 agents and the ADK pipeline.
5.  **Conclusion (2:30-3:00)**: "Built with Google ADK. Thanks for watching."
