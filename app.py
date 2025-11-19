import streamlit as st
import requests
import json
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os
import base64

# Page Config
st.set_page_config(
    page_title="Dynamic Knowledge Graph Architect",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look - Neutral/Purple Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0f0f12; /* Very dark almost black */
        color: #e2e8f0;
    }
    .stButton>button {
        background-color: #8b5cf6; /* Violet-500 */
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #7c3aed; /* Violet-600 */
        transform: translateY(-1px);
    }
    .stTextInput>div>div>input {
        background-color: #1e1e24;
        color: #e2e8f0;
        border-radius: 0.5rem;
        border: 1px solid #2d2d3a;
    }
    .metric-card {
        background-color: #1e1e24;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #2d2d3a;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #a78bfa; /* Violet-400 */
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    h1, h2, h3 {
        color: #f8fafc;
    }
    .stSpinner > div {
        border-top-color: #8b5cf6 !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🕸️ Graph Controls")
    st.markdown("---")
    
    st.subheader("Visualization Settings")
    show_physics = st.toggle("Enable Physics", value=True)
    show_labels = st.toggle("Show Node Labels", value=True)
    layout_type = st.selectbox("Layout Algorithm", ["Barnes Hut", "Force Atlas 2 Based", "Repulsion"])
    
    st.markdown("---")
    st.subheader("Filters")
    max_edges = st.slider("Max Edges to Display", min_value=10, max_value=500, value=100)
    
    st.markdown("---")
    st.markdown("Powered by **Google Gemini** & **ADK**")

# Main Content
st.title("Dynamic Knowledge Graph Architect")
st.markdown("Transform any topic into a structured, interactive knowledge graph.")

# Input Section
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("Research Topic", placeholder="e.g., The History of Artificial Intelligence")
with col2:
    st.write("") # Spacer
    st.write("") # Spacer
    generate_btn = st.button("Generate Graph", use_container_width=True, type="primary")

# Session State for Results
if "graph_data" not in st.session_state:
    st.session_state.graph_data = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "image_base64" not in st.session_state:
    st.session_state.image_base64 = None

# Logic
if generate_btn and topic:
    with st.spinner("🤖 Agents are researching and building the graph..."):
        try:
            # Reset session state before new generation
            st.session_state.graph_data = None
            st.session_state.summary = None
            st.session_state.image_base64 = None
            
            response = requests.post(
                "http://localhost:8000/generate",
                json={"topic": topic},
                timeout=300 # 5 min timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.graph_data = data.get("graph_state")
                st.session_state.summary = data.get("summary")
                st.session_state.image_base64 = data.get("image_base64")
                st.success("Graph generated successfully!")
            else:
                st.error(f"Error: {response.text}")
                
        except Exception as e:
            st.error(f"Connection Error: {str(e)}")

# Display Results
if st.session_state.graph_data:
    st.markdown("---")
    
    # Stats Row
    nodes = st.session_state.graph_data["nodes"]
    edges = st.session_state.graph_data["edges"]
    
    # Calculate most connected node
    if nodes and edges:
        node_degrees = {}
        for edge in edges:
            node_degrees[edge["source"]] = node_degrees.get(edge["source"], 0) + 1
            node_degrees[edge["target"]] = node_degrees.get(edge["target"], 0) + 1
        most_connected = max(node_degrees, key=node_degrees.get) if node_degrees else "N/A"
    else:
        most_connected = "N/A"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(nodes)}</div><div class="metric-label">Nodes</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(edges)}</div><div class="metric-label">Edges</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{most_connected}</div><div class="metric-label">Top Entity</div></div>""", unsafe_allow_html=True)

    st.markdown("### 🕸️ Interactive Graph")
    
    # PyVis Visualization
    # Create a subset of edges based on slider
    display_edges = edges[:max_edges]
    
    net = Network(height="700px", width="100%", bgcolor="#1e1e24", font_color="white")
    
    # Add nodes
    for node in nodes:
        # node is a string ID
        net.add_node(node, label=node if show_labels else " ", title=node, color="#8b5cf6")
        
    # Add edges
    for edge in display_edges:
        net.add_edge(edge["source"], edge["target"], title=edge["relation"], label=edge["relation"], color="#475569")
        
    # Physics options
    if layout_type == "Barnes Hut":
        net.barnes_hut()
    elif layout_type == "Force Atlas 2 Based":
        net.force_atlas_2based()
    elif layout_type == "Repulsion":
        net.repulsion()
        
    net.toggle_physics(show_physics)
    
    # Save and display
    try:
        path = "tmp_graph.html"
        net.save_graph(path)
        with open(path, 'r', encoding='utf-8') as f:
            html_string = f.read()
        # Use a larger height and scrolling to ensure visibility
        components.html(html_string, height=700, scrolling=False)
        os.remove(path)
    except Exception as e:
        st.error(f"Error rendering graph: {e}")

    # Downloads
    st.markdown("### 📥 Downloads")
    d1, d2 = st.columns(2)
    
    with d1:
        # Download JSON
        json_str = json.dumps(st.session_state.graph_data, indent=2)
        st.download_button(
            label="Download Graph JSON",
            data=json_str,
            file_name="knowledge_graph.json",
            mime="application/json",
            use_container_width=True
        )
        
    with d2:
        # Download PNG (from backend)
        if st.session_state.image_base64:
            img_bytes = base64.b64decode(st.session_state.image_base64)
            st.download_button(
                label="Download Graph PNG",
                data=img_bytes,
                file_name="knowledge_graph.png",
                mime="image/png",
                use_container_width=True
            )

    # Summary
    with st.expander("📝 Agent Summary", expanded=False):
        st.text(st.session_state.summary)
