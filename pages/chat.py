import streamlit as st
from src.agent.agent import WeeabooBudddy
from langchain_core.messages import HumanMessage

st.title("🎌 Weeaboo-Buddy")
agent = WeeabooBudddy()

# Initialize session state for messages, processing status, and memory choice
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "memory_choice" not in st.session_state:
    st.session_state.memory_choice = True  # Default memory to True

# --- Main Chat Interface ---
if not st.session_state.messages:
    st.info(
        "Hello! I'm your Weeaboo-Buddy! Ask me anything about anime, manga, characters, or anything otaku-related!"
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
            # Use memory choice from session state, which is set in 'Chat Options'
            config = {"configurable": {"thread_id": st.session_state.user_email}}
            if not st.session_state.memory_choice:
                config["configurable"]["thread_id"] = None

            last_user_prompt = st.session_state.messages[-1]["content"]
            input_message = [HumanMessage(content=last_user_prompt)]
            response_placeholder = st.empty()
            full_response = ""

            try:
                for chunk in agent.stream(
                    {"messages": input_message}, config, stream_mode="values"
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
