from google.adk.agents import SequentialAgent
from .agents import research_agent, ontology_agent, viz_agent

# The Graph Architect
# A Sequential Agent that orchestrates the entire pipeline.
# 1. ResearchAgent: Gets the raw info.
# 2. OntologyAgent: Structures it into the graph.
# 3. VisualizationAgent: Draws the graph.

graph_architect = SequentialAgent(
    name="GraphArchitect",
    description="A pipeline that researches a topic, builds a knowledge graph, and visualizes it.",
    sub_agents=[research_agent, ontology_agent, viz_agent],
    # We don't strictly need output_keys here because SequentialAgent passes the previous output
    # as part of the prompt history to the next agent automatically.
)
