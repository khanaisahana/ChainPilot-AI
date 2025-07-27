# from langgraph_config import graph

# def run_logistics_graph(order_text: str):
#     state = {
#         "order_text": order_text
#     }

#     result = graph.invoke(
#         state,
#         config={"run_trace": True, "run_timing": True}
#     )

#     final_state = result["output"]
#     trace = result.get("trace", {})
#     timing = result.get("timing", {})

#     return final_state, trace, timing
