# langgraph_config.py (Updated for Full Trace, Map, Retry Simulation, Explainable AI)

from typing import TypedDict, Optional, Dict, List
from langgraph.graph import StateGraph, END
from agents.order_manager import extract_order_info
from agents.inventory_checker import check_inventory
from agents.route_optimizer import optimize_route
from agents.delivery_agent import delivery_agent
from agents.delay_handler import delay_handler
from agents.issue_resolver import issue_resolver

# ✅ Define extended state for enhanced Streamlit UI
class OrderState(TypedDict):
    order_text: str
    parsed_order: Optional[Dict]
    inventory_ok: Optional[bool]
    available_stock: Optional[int]
    route: Optional[str]
    distance_km: Optional[float]
    duration_minutes: Optional[float]
    delivery_status: Optional[str]
    issue_detected: Optional[bool]
    issue_type: Optional[str]
    route_coords: Optional[List[Dict[str, float]]]
    api_key: Optional[str] 
    ors_api_key: Optional[str] 

    # 🔍 Agent execution trace
    trace: Optional[List[Dict[str, str]]]

    # 📉 Time tracking for each step
    timing: Optional[Dict[str, float]]

    # 🧠 Explainability store
    explanations: Optional[Dict[str, str]]


import time

# Utility: Add trace with timing and explanation

def trace_and_time(func, name):
    def wrapper(state: OrderState):
        start = time.time()
        result = func(state)
        end = time.time()

        trace = state.get("trace", [])
        trace.append({"agent": name, "input": str(state), "output": str(result)})

        timing = state.get("timing", {})
        timing[name] = round(end - start, 3)

        explanations = state.get("explanations", {})
        if name == "route_optimizer":
            explanations["route_choice"] = f"Chose shortest or optimal path from Mumbai to {state['parsed_order']['destination']} based on distance/time."

        return {
            **state,
            **result,
            "trace": trace,
            "timing": timing,
            "explanations": explanations
        }
    return wrapper

# ✅ Wrap all agent functions
order_manager_node = trace_and_time(lambda s: {
    "order_text": s["order_text"],
    "parsed_order": extract_order_info(s)
}, "order_manager")

check_inventory_wrapped = trace_and_time(check_inventory, "inventory_checker")
optimize_route_wrapped = trace_and_time(optimize_route, "route_optimizer")
delivery_agent_wrapped = trace_and_time(delivery_agent, "delivery_agent")
delay_handler_wrapped = trace_and_time(delay_handler, "delay_handler")
issue_resolver_wrapped = trace_and_time(issue_resolver, "issue_resolver")

# ✅ Create Graph
builder = StateGraph(OrderState)

builder.add_node("order_manager", order_manager_node)
builder.add_node("inventory_checker", check_inventory_wrapped)
builder.add_node("route_optimizer", optimize_route_wrapped)
builder.add_node("delivery_agent", delivery_agent_wrapped)
builder.add_node("delay_handler", delay_handler_wrapped)
builder.add_node("issue_resolver", issue_resolver_wrapped)

builder.set_entry_point("order_manager")
builder.add_edge("order_manager", "inventory_checker")
builder.add_edge("inventory_checker", "route_optimizer")
builder.add_edge("route_optimizer", "delivery_agent")


# Conditional branching based on issue type
def handle_delivery_issue(state: dict) -> str:
    if not state.get("issue_detected"):
        return "__end__"
    return {
        "delay": "delay_handler",
        "failure": "issue_resolver"
    }.get(state.get("issue_type"), "__end__")

builder.add_conditional_edges("delivery_agent", handle_delivery_issue)

builder.set_finish_point("delivery_agent")
builder.set_finish_point("delay_handler")
builder.set_finish_point("issue_resolver")

# ✅ Export compiled LangGraph
graph = builder.compile()
