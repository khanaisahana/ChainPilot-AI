# import streamlit as st
# from langgraph_config import graph
# import os
# from dotenv import load_dotenv
# import graphviz
# from utils.graph_renderer import render_agent_flow_pyvis
# import time
# import pandas as pd

# load_dotenv()

# import streamlit as st

# st.set_page_config(page_title="Multi-Agent Logistics Optimizer", layout="wide")

# # Custom CSS for center alignment and input box styling
# st.markdown("""
#     <style>
#     .center-title {
#         text-align: center;
#         font-size: 2.5em;
#         font-weight: 700;
#         margin-bottom: 0.2em;
#     }
#     .subtext {
#         text-align: center;
        
#         font-size: 1.1em;
#         margin-bottom: 2em;
#     }
#     .centered-input .stTextInput>div>div>input {
#         text-align: center;
#     }
#     .agent-card {
    
#     padding: 1.5rem;
#     margin-bottom: 1rem;
#     border-radius: 1rem;
#     box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#     transition: transform 0.2s ease, box-shadow 0.3s ease;
#     }
#     .agent-card:hover {
#         transform: translateY(-4px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.2);
#     }
#     .agent-name {
#         font-size: 1.5em;
#         font-weight: bold;
#         margin-bottom: 0.5rem;
#     }
#     .code-block {
#         background-color: #1e1e1e;
#         color: #ffffff;
#         padding: 1rem;
#         border-radius: 0.5rem;
#         font-family: monospace;
#         white-space: pre-wrap;
#     }
#     .time-badge {
#         display: inline-block;
#         background-color: #007acc;
#         color: white;
#         padding: 0.3rem 0.7rem;
#         font-size: 0.9rem;
#         border-radius: 0.5rem;
#         margin-top: 0.5rem;
#     }
#             .element-container:has(> .stGraphvizChart) {
#         max-height: 500px;
#         overflow-y: auto;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Title and subtext centered
# st.markdown('<div class="center-title">📦 Multi-Agent Logistics Chain Optimizer</div>', unsafe_allow_html=True)
# st.markdown('<div class="subtext">Powered by <strong>LangGraph + LLM + Generative AI</strong></div>', unsafe_allow_html=True)

# # Input field centered using columns
# col1, col2, col3 = st.columns([2, 4, 2])
# with col2:
#     order_input = st.text_input("📝 Enter Order:", value="Ship 10 phones to Hyderabad", key="order_input")

# # Centered Run Button and Results
# col4, col5, col6 = st.columns([2, 4, 2])
# with col2:
#     run_btn = st.button("🚀 Run Agents")

# if run_btn:
#     with col5:  # Keep spinner and success message centered
#         # Inside the `if run_btn` block
#         with st.spinner("🧠 Running LangGraph agents..."):
#             time.sleep(0.5)  # Optional for smooth feel
#             final_state = graph.invoke({"order_text": order_input})
#         st.success("Agents completed execution!", icon="✅")
      
#     st.subheader("📦 Final State")
#     st.json(final_state)
    
#     # 📍 Step-by-step output display per agent
#     if "trace" in final_state:
#         st.subheader("🔎 Step-by-Step Agent Execution")
    
#         agent_icons = {
#             "order_manager": "📋",
#             "inventory_checker": "📦",
#             "route_optimizer": "🗺️",
#             "delivery_agent": "🚚",
#             "issue_resolver": "🧯",
#             "delay_handler": "⏳",  # NEW: Added icon for Delay Handler
#         }
    
#         # Modern Agent Output Display


#     for idx, step in enumerate(final_state["trace"]):
#         agent = step.get("agent", f"Agent {idx + 1}")
#         icon = agent_icons.get(agent, "🤖")
#         output = step.get("output", "{}")
#         time_taken = final_state.get("timing", {}).get(agent, "N/A")

#         st.markdown(f"""
#         <div class="agent-card">
#             <div class="agent-name">{icon} {agent}</div>
#             <div class="code-block">{output}</div>
#             <div class="time-badge">⏱️ {time_taken} seconds</div>
#         </div>
#         """, unsafe_allow_html=True)
       
    
#         # Optional Delivery Status
#     if final_state.get("delivery_status"):
#         st.success(f"✅ Delivery Status: {final_state['delivery_status']}")


#     # 📍 Step-by-step output display per agent
#     if "trace" in final_state:
#         st.subheader("🔎 Step-by-Step Agent Execution")

#         for idx, step in enumerate(final_state["trace"]):
#             agent = step.get("agent", f"agent_{idx}")
#             st.markdown(f"### 🔹 Step {idx + 1}: `{agent}`")
            
#             with st.expander("📥 Input"):
#                 st.code(step.get("input", "{}"), language="json")

#             with st.expander("📤 Output"):
#                 st.code(step.get("output", "{}"), language="json")

#             time_taken = final_state.get("timing", {}).get(agent, "N/A")
#             st.caption(f"⏱️ Time Taken: `{time_taken}` seconds")

#         # Optional Delivery Status
#         if final_state.get("delivery_status"):
#             st.success(f"✅ Delivery Status: {final_state['delivery_status']}")

    
#     # ➕ Visual LangGraph execution flow in sidebar
#     if "trace" in final_state:
#         with st.sidebar:
#             st.markdown("### 📈 Agent Execution Flow")
#             dot = graphviz.Digraph()
    
#             for idx, step in enumerate(final_state["trace"]):
#                 agent_name = step.get("agent", f"agent_{idx}")
#                 time_taken = final_state.get("timing", {}).get(agent_name, "N/A")
#                 label = f"{agent_name}\\n⏱️ {time_taken}s"
#                 dot.node(agent_name, label=label, shape="box", style="filled", color="#cce5ff")
    
#                 if idx > 0:
#                     prev_agent = final_state["trace"][idx - 1]["agent"]
#                     dot.edge(prev_agent, agent_name)
    
#             st.graphviz_chart(dot, use_container_width=True)


#     # Show issue if detected
#     if final_state.get("issue_detected"):
#         st.warning("⚠️ Issue detected during execution")
