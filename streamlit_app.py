import streamlit as st
from langgraph_config import graph
import os
from dotenv import load_dotenv
import graphviz

load_dotenv()

st.set_page_config(page_title="Multi-Agent Logistics Optimizer", layout="wide")

# API Key Input UI
st.sidebar.header("🔐 Authentication")
api_key = st.sidebar.text_input("Enter your OpenRouter API Key", type="password")

# Store API key in session state and set environment variable
if api_key:
    st.session_state["OPENROUTER_API_KEY"] = api_key
    os.environ["OPENROUTER_API_KEY"] = api_key  # Optional: If your LangGraph code reads from os.environ
else:
    st.sidebar.warning("Please enter your OpenRouter API key to run the agents.")


st.title("📦 Multi-Agent Logistics Chain Optimizer")
st.write("Powered by LangGraph + LLM + Generative AI")

order_input = st.text_input("📝 Enter Order:", "Ship 10 phones to Hyderabad")

if st.button("🚀 Run Agents"):
    if not api_key:
        st.error("❗Please provide your OpenRouter API key in the sidebar.")
    else:
        with st.spinner("Running LangGraph..."):
            # final_state = graph.invoke({"order_text": order_input})
            final_state = graph.invoke({
                "order_text": order_input,
                "api_key": api_key   # pass it to the graph
                })


        st.success("✅ Agents completed execution!")
        # st.subheader("📦 Final State")
        # st.json(final_state)
        
        if "inventory_ok" in final_state:
            if final_state['inventory_ok']==True:
                st.markdown("Inventory Check: ✅ Available Stock")
            else:
                st.markdown("Inventory Check: ❌ Insufficient Stock")
            st.markdown(f"**Available Stock:** {final_state['available_stock']} units")
            
        if "route" in final_state:
            st.markdown(f"**Optimized Route:** {final_state['route']}")
            st.markdown(f"**Distance:** {final_state['distance_km']} km")
            st.markdown(f"**ETA:** {final_state['duration_minutes']} mins")
    
        
        # ----------------- Delivery Status Handling -----------------
        delivery_status = final_state.get("delivery_status", "Unknown")
        
        if final_state.get("issue_detected"):
            issue_type = final_state.get("issue_type", "Unknown")
            st.markdown("### 🚚 Delivery Status: ⚠️ **Delivery Issue Detected**")
            st.warning(f"**Issue Type:** `{issue_type}`")
            
        
            # Route to specific issue handler based on issue_type
            if issue_type == "delay":
                from agents.delay_handler import delay_handler
                resolution = delay_handler(final_state)
                st.info(f"🕒 {resolution.get('delivery_status')}")
                st.success(f"🔄 Next Step: {resolution.get('next_step')}")
            
            elif issue_type == "failure":
                from agents.issue_resolver import issue_resolver
                resolution = issue_resolver(final_state)
                st.success(f"🛠️ Issue Resolved: {resolution.get('resolution')}")
        
            else:
                st.warning("⚠️ No handler found for this issue type.")
        
        else:
            st.markdown(f"### 🚚 Delivery Status: ✅ `{delivery_status}`")
        
    
        
    
        # ➕ Visual LangGraph execution flow in sidebar
        if "trace" in final_state:
            with st.sidebar:
                st.markdown("### 📈 Agent Execution Flow")
                dot = graphviz.Digraph()
        
                for idx, step in enumerate(final_state["trace"]):
                    agent_name = step.get("agent", f"agent_{idx}")
                    time_taken = final_state.get("timing", {}).get(agent_name, "N/A")
                    label = f"{agent_name}\\n⏱️ {time_taken}s"
                    dot.node(agent_name, label=label, shape="box", style="filled", color="#cce5ff")
        
                    if idx > 0:
                        prev_agent = final_state["trace"][idx - 1]["agent"]
                        dot.edge(prev_agent, agent_name)
        
                st.graphviz_chart(dot, use_container_width=True)
    
    
    
        if "route_coords" in final_state and len(final_state["route_coords"]) == 2:
            st.markdown("### 🗺️ Delivery Route Map")
        
            import pandas as pd
            import pydeck as pdk
        
            coords = final_state["route_coords"]
        
            df = pd.DataFrame([{
                "from_lon": coords[0]["lon"],
                "from_lat": coords[0]["lat"],
                "to_lon": coords[1]["lon"],
                "to_lat": coords[1]["lat"]
            }])
        
            line_layer = pdk.Layer(
                "LineLayer",
                data=df,
                get_source_position=["from_lon", "from_lat"],
                get_target_position=["to_lon", "to_lat"],
                get_width=5,
                get_color=[255, 0, 0],  # red line
                pickable=True
            )
        
            view_state = pdk.ViewState(
                latitude=(df["from_lat"][0] + df["to_lat"][0]) / 2,
                longitude=(df["from_lon"][0] + df["to_lon"][0]) / 2,
                zoom=5
            )
        
            deck = pdk.Deck(
                layers=[line_layer],
                initial_view_state=view_state,
                tooltip={"text": "Route Line"}
            )
        
            st.pydeck_chart(deck)
        