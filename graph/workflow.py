# Builds and compiles the LangGraph workflow by connecting all nodes

from langgraph.graph import StateGraph, START, END

from schemas.state import SafeWatchState
from agents.cleaner import run_cleaner
from agents.classifier import run_classifier


from graph.nodes import (
    load_raw_post_node,
    check_existing_incident_node,
    create_incident_node,
    save_outputs_node,
    route_after_existing_check,
)


graph_builder = StateGraph(SafeWatchState)

# Add database/pipeline nodes.
graph_builder.add_node("load_raw_post", load_raw_post_node)
graph_builder.add_node("check_existing_incident", check_existing_incident_node)
graph_builder.add_node("create_incident", create_incident_node)
graph_builder.add_node("save_outputs", save_outputs_node)

# Add AI agent nodes.
graph_builder.add_node("cleaner", run_cleaner)
graph_builder.add_node("classifier", run_classifier)

# Define workflow order.
graph_builder.add_edge(START, "load_raw_post")
graph_builder.add_edge("load_raw_post", "check_existing_incident")

# If incident already exists, skip processing.
# Otherwise, create a new incident and continue.
graph_builder.add_conditional_edges(
    "check_existing_incident",
    route_after_existing_check,
    {
        "create_incident": "create_incident",
        "end": END,
    },
)

graph_builder.add_edge("create_incident", "cleaner")
graph_builder.add_edge("cleaner", "classifier")
graph_builder.add_edge("classifier", "save_outputs")
graph_builder.add_edge("save_outputs", END)

# Compile graph for use by process_post.py.
graph = graph_builder.compile()