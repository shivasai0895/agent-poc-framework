"""Streamlit demo UI."""
import asyncio
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents import root_agent
from agents.runner import create_runner, run_turn

st.set_page_config(page_title=root_agent.name, page_icon="🤖")
st.title(root_agent.name)

# Initialise session state
if "runner" not in st.session_state:
    st.session_state.runner = create_runner(root_agent)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = "streamlit-session"

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle new input
if prompt := st.chat_input("Message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(
                run_turn(
                    st.session_state.runner,
                    prompt,
                    session_id=st.session_state.session_id,
                )
            )
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
