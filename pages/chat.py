import streamlit as st
from src.agent.agent import WeeabooBudddy
from langchain_core.messages import HumanMessage
import base64
import tempfile
import os


st.title("🎌 Weeaboo-Buddy")
agent = WeeabooBudddy()

# Initialize session state for messages, processing status, and memory choice
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "temp_files" not in st.session_state:
    st.session_state.temp_files = []
if "history_loaded" not in st.session_state:
    st.session_state.history_loaded = False


def load_chat_history():
    """Load chat history from LangGraph state for cross-device sync"""
    if st.session_state.history_loaded:
        return

    try:
        # Get the thread ID (user email)
        thread_id = st.session_state.get("user_email", "default")

        # Configure for getting state
        config = {"configurable": {"thread_id": thread_id}}

        # Get the current state from LangGraph
        state = agent.get_state(config)

        # Extract messages from the state
        if state and hasattr(state, "values") and "messages" in state.values:
            langgraph_messages = state.values["messages"]

            # Convert LangGraph messages to Streamlit chat format
            converted_messages = []
            for msg in langgraph_messages:
                if hasattr(msg, "type") and hasattr(msg, "content"):
                    # Convert LangGraph message types to chat roles
                    if msg.type == "human":
                        role = "user"
                    elif msg.type == "ai":
                        role = "assistant"
                    else:
                        continue  # Skip system messages or other types

                    # Handle both string and multimodal content
                    content = msg.content
                    if isinstance(content, str):
                        converted_messages.append({"role": role, "content": content})
                    elif isinstance(content, list):
                        # Handle multimodal content (text + images)
                        converted_messages.append({"role": role, "content": content})

            # Only update if we have messages and haven't loaded before
            if converted_messages and not st.session_state.messages:
                st.session_state.messages = converted_messages
                st.success(
                    f"Loaded {len(converted_messages)} messages from chat history!"
                )

        st.session_state.history_loaded = True

    except Exception as e:
        st.error(f"Error loading chat history: {str(e)}")
        st.session_state.history_loaded = True  # Mark as loaded to prevent retry loops


def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary location and return the path"""
    try:
        # Create a temporary file with the same extension
        file_extension = os.path.splitext(uploaded_file.name)[1]
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)

        # Write the uploaded file content to temp file
        temp_file.write(uploaded_file.read())
        temp_file.close()

        # Reset the uploaded file pointer
        uploaded_file.seek(0)

        # Store temp file path for cleanup later
        st.session_state.temp_files.append(temp_file.name)

        return temp_file.name
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None


def encode_image_to_base64(image_file):
    """Convert uploaded image to base64 string"""
    try:
        # If it's a file-like object from Streamlit
        if hasattr(image_file, "read"):
            image_bytes = image_file.read()
            image_file.seek(0)  # Reset file pointer
        else:
            image_bytes = image_file

        # Convert to base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        return image_base64
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None


def create_multimodal_message_content(text, images, image_paths):
    """Create message content with text, images, and file paths"""
    content = []

    # Add text if provided
    if text:
        content.append({"type": "text", "text": text})

    # Add file paths as text for the agent to use with tools
    if image_paths:
        paths_text = "Uploaded image file paths: " + ", ".join(image_paths)
        content.append({"type": "text", "text": paths_text})

    # Add images as base64 for visual processing
    for image_file in images:
        image_base64 = encode_image_to_base64(image_file)
        if image_base64:
            # Get image format
            image_format = (
                image_file.type.split("/")[-1]
                if hasattr(image_file, "type")
                else "jpeg"
            )
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{image_format};base64,{image_base64}"
                    },
                }
            )

    return content


def cleanup_temp_files():
    """Clean up temporary files"""
    for temp_file in st.session_state.temp_files:
        if os.path.exists(temp_file):
            os.unlink(temp_file)
    st.session_state.temp_files = []


# Load chat history from LangGraph state when page loads
load_chat_history()

# --- Main Chat Interface ---
if not st.session_state.messages:
    st.info(
        "Hello! I'm your Weeaboo-Buddy! Ask me anything about anime, manga, characters, or anything otaku-related! You can also upload images!"
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], str):
            st.markdown(message["content"])
        else:
            # Handle multimodal content
            for content_item in message["content"]:
                if content_item["type"] == "text":
                    # Don't show the file paths text to users, only the actual message
                    if not content_item["text"].startswith(
                        "Uploaded image file paths:"
                    ):
                        st.markdown(content_item["text"])
                elif content_item["type"] == "image_url":
                    st.image(content_item["image_url"]["url"], caption="Uploaded image")

if not st.session_state.processing:
    if prompt := st.chat_input(
        "What would you like to know about anime/manga?", accept_file="multiple"
    ):
        user_text = prompt.text if prompt.text else ""
        uploaded_files = prompt.files if prompt.files else []

        # Display user message and process files
        if user_text or uploaded_files:
            # Save uploaded files and get paths
            image_paths = []

            # Display the user message immediately
            with st.chat_message("user"):
                if user_text:
                    st.markdown(user_text)

                # Display and process each uploaded file
                for image_file in uploaded_files:
                    st.image(image_file, caption=f"Uploaded: {image_file.name}")

                    # Save file and get path
                    temp_path = save_uploaded_file(image_file)
                    if temp_path:
                        image_paths.append(temp_path)

            # Create content for the agent (includes both visual data and file paths)
            if uploaded_files:
                message_content = create_multimodal_message_content(
                    user_text, uploaded_files, image_paths
                )
            else:
                message_content = user_text

            # Store message in session state
            st.session_state.messages.append(
                {"role": "user", "content": message_content}
            )

        st.session_state.processing = True
        st.rerun()

# Process the AI response
if st.session_state.processing:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            config = {
                "configurable": {
                    "thread_id": st.session_state.get("user_email", "default")
                }
            }

            # Get the last user message
            last_user_message = st.session_state.messages[-1]

            # Create the input message for the agent
            input_message = [HumanMessage(content=last_user_message["content"])]

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
