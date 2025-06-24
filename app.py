import streamlit as st
from src.agent import WeeabooBudddy
from langchain_core.messages import HumanMessage, AIMessage
import json
from datetime import datetime

st.set_page_config(page_title="Weeaboo-Buddy", page_icon="🎌", layout="wide")

st.title("🎌 Weeaboo-Buddy")

agent = WeeabooBudddy()
message_count = 0

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "current_session" not in st.session_state:
    st.session_state.current_session = "default"
# Add a new session state variable to track if the AI is thinking
if "processing" not in st.session_state:
    st.session_state.processing = False

# Sidebar with enhanced controls
with st.sidebar:
    st.header("🎮 Chat Controls")

    # Session management
    st.subheader("💾 Session Management")

    # Current session info
    current_session = st.session_state.current_session
    message_count = len(st.session_state.messages)
    st.write(f"Current session: **{current_session}**")
    st.write(f"Messages: **{message_count}**")

    col1, col2 = st.columns(2)

    with col1:
        # Clear current session
        if st.button("🗑️ Clear Current", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with col2:
        # Save current session
        if st.button("💾 Save Session", type="secondary", use_container_width=True):
            if st.session_state.messages:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                session_name = f"Chat_{timestamp}"
                st.session_state.chat_sessions[session_name] = (
                    st.session_state.messages.copy()
                )
                st.success(f"Saved as: {session_name}")

    # Load saved sessions
    if st.session_state.chat_sessions:
        st.subheader("📂 Saved Sessions")
        selected_session = st.selectbox(
            "Load a saved session:",
            options=[""] + list(st.session_state.chat_sessions.keys()),
            index=0,
        )

        if selected_session:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Load", key="load_session"):
                    st.session_state.messages = st.session_state.chat_sessions[
                        selected_session
                    ].copy()
                    st.session_state.current_session = selected_session
                    st.rerun()

            with col2:
                if st.button("🗑️ Delete", key="delete_session"):
                    del st.session_state.chat_sessions[selected_session]
                    st.rerun()

    st.divider()

    # Export options
    st.subheader("📤 Export Options")

    if message_count > 0:
        # Export as Markdown
        if st.button("📝 Export as Markdown", use_container_width=True):
            chat_export = f"# Weeaboo-Buddy Chat Export\n**Session:** {current_session}\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            for i, msg in enumerate(st.session_state.messages, 1):
                role = "You" if msg["role"] == "user" else "Weeaboo-Buddy"
                chat_export += f"## Message {i} - {role}\n{msg['content']}\n\n"

            st.download_button(
                label="💾 Download Markdown",
                data=chat_export,
                file_name=f"weeaboo_buddy_{current_session}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

        # Export as JSON
        if st.button("🔗 Export as JSON", use_container_width=True):
            export_data = {
                "session_name": current_session,
                "export_date": datetime.now().isoformat(),
                "message_count": message_count,
                "messages": st.session_state.messages,
            }

            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"weeaboo_buddy_{current_session}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )

    st.divider()

    # Performance indicators
    st.subheader("⚡ Performance")

    if message_count > 100:
        st.error("🚨 Very long conversation! Consider starting fresh.")
    elif message_count > 50:
        st.warning("⚠️ Long conversation detected.")
    elif message_count > 0:
        st.success("✅ Performance optimal")

    # Memory usage estimate
    total_chars = sum(len(str(msg["content"])) for msg in st.session_state.messages)
    st.caption(f"Estimated memory: ~{total_chars:,} characters")

    st.divider()
    st.caption(
        "💡 **Tips:**\n- Save important conversations\n- Clear history for better performance\n- Export chats for future reference"
    )

# Main chat interface
if len(st.session_state.messages) == 0:
    st.info(
        "👋 Hello! I'm your Weeaboo-Buddy! Ask me anything about anime, manga, characters, or anything otaku-related!"
    )

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if not st.session_state.processing:
    if prompt := st.chat_input("What would you like to know about anime/manga?"):
        # Store as simple dict with string content
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Set processing to True to hide the input and show a spinner
        st.session_state.processing = True
        st.rerun()

if st.session_state.processing:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            config = {"configurable": {"thread_id": st.session_state.current_session}}

            # Convert session state messages to proper LangChain message format
            messages = []
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

            # Use placeholder for response collection
            response_placeholder = st.empty()
            full_response = ""

            # Stream the response
            try:
                for chunk in agent.stream(
                    {"messages": messages},
                    config,  # type: ignore
                    stream_mode="values",
                ):
                    # Extract the actual content from the chunk
                    if chunk.get("messages") and len(chunk["messages"]) > 0:
                        last_message = chunk["messages"][-1]
                        if (
                            hasattr(last_message, "content")
                            and last_message.type == "ai"
                        ):
                            full_response = last_message.content
                            response_placeholder.markdown(full_response)

                response = full_response
            except Exception as e:
                response = f"Sorry, I encountered an error: {str(e)}"
                st.error(response)

            # Store assistant response as simple dict with string content
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Set processing to False to show the input again
            st.session_state.processing = False
            st.rerun()
