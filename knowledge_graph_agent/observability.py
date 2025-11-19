from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from .graph_tools import kb

class GraphBuilderPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="graph_builder_plugin")
        self.triplets_added = 0
        self.viz_generated = 0

    async def after_tool_callback(self, **kwargs):
        """Monitor tool usage to track graph growth."""
        tool = kwargs.get("tool")
        tool_result = kwargs.get("tool_result")
        
        if tool and tool.name == "add_triplet" and tool_result and tool_result.get("status") == "success":
            self.triplets_added += 1
            print(f"📈 [GraphPlugin] New Knowledge! Total Triplets Added: {self.triplets_added}")
            
        if tool and tool.name == "get_graph_state":
            # Just logging the current size when state is checked
            # Just logging the current size when state is checked
            state = kb.get_state()
            print(f"🔍 [GraphPlugin] Graph State Checked: {len(state['nodes'])} Nodes, {len(state['edges'])} Edges")

    async def after_agent_callback(self, **kwargs):
        """Track when the visualization is complete."""
        agent = kwargs.get("agent")
        if agent and agent.name == "VisualizationAgent":
            self.viz_generated += 1
            print(f"🎨 [GraphPlugin] Visualization Agent finished. Check for 'knowledge_graph.png'!")

    def get_stats(self):
        return {
            "total_triplets_added": self.triplets_added,
            "visualizations_generated": self.viz_generated,
            "final_graph_size": {
                "nodes": len(kb.get_state()["nodes"]),
                "edges": len(kb.get_state()["edges"])
            }
        }
