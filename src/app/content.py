import streamlit as st
from ..agent.agent import WeeabooBudddy
from langchain_core.messages import HumanMessage
import json
from datetime import datetime
from ..app.authentication import sign_out  # NEW: Import the sign_out function


def app_content():
    """
    This function encapsulates the main chat interface of the application.
    """
    agent = WeeabooBudddy()

    # Initialize session state for messages and processing status
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processing" not in st.session_state:
        st.session_state.processing = False

    # --- Sidebar ---
    with st.sidebar:
        st.header("🎮 Chat Controls")

        # NEW: Total message count display
        message_count = len(st.session_state.messages)
        st.metric(label="Total Messages", value=message_count)
        st.divider()

        # --- Export Options ---
        st.subheader("📤 Export Chat")

        if message_count > 0:
            # Export as Markdown
            chat_export = f"# Weeaboo-Buddy Chat\n**User:** {st.session_state.user_email}\n**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            for i, msg in enumerate(st.session_state.messages, 1):
                role = "You" if msg["role"] == "user" else "Weeaboo-Buddy"
                chat_export += f"## Message {i} - {role}\n{msg['content']}\n\n"

            st.download_button(
                label="📝 Download Markdown",
                data=chat_export,
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

            # Export as JSON
            export_data = {
                "user_email": st.session_state.user_email,
                "export_date": datetime.now().isoformat(),
                "message_count": message_count,
                "messages": st.session_state.messages,
            }

            st.download_button(
                label="🔗 Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )
        else:
            st.caption("Chat is empty. Nothing to export.")

        st.divider()

        # --- Socials/Contact ---
        st.subheader("🤙 Contact Me")
        st.link_button("GitHub", "https://github.com/drod75", use_container_width=True)
        st.link_button(
            "LinkedIn",
            "https://www.linkedin.com/in/david-rodriguez-nyc/",
            use_container_width=True,
        )

        # NEW: Logout Button at the bottom of the sidebar
        st.divider()
        if st.button("Log Out", use_container_width=True, type="primary"):
            sign_out()

    # --- Main Chat Interface ---
    if not st.session_state.messages:
        st.info(
            "👋 Hello! I'm your Weeaboo-Buddy! Ask me anything about anime, manga, characters, or anything otaku-related!"
        )

    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle chat input if not currently processing a response
    if not st.session_state.processing:
        if prompt := st.chat_input("What would you like to know about anime/manga?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            st.session_state.processing = True
            st.rerun()

    # Process the AI response
    if st.session_state.processing:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Use the user's email as the unique thread_id
                config = {"configurable": {"thread_id": st.session_state.user_email}}

                # Get only the content of the most recent user message
                last_user_prompt = st.session_state.messages[-1]["content"]

                # The input only needs to be the new HumanMessage
                input_message = [HumanMessage(content=last_user_prompt)]

                response_placeholder = st.empty()
                full_response = ""

                try:
                    # Pass only the new message to the stream
                    for chunk in agent.stream(
                        {"messages": input_message}, config, stream_mode="values"  # type: ignore
                    ):
                        if chunk.get("messages"):
                            last_message = chunk["messages"][-1]
                            if (
                                hasattr(last_message, "content")
                                and last_message.type == "ai"
                            ):
                                full_response = last_message.content
                                response_placeholder.markdown(full_response + "▌")

                    response_placeholder.markdown(full_response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": full_response}
                    )

                except Exception as e:
                    error_message = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_message}
                    )

                st.session_state.processing = False
                st.rerun()
