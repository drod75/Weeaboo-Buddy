import streamlit as st
import json
from rich import Console
import os


st.title("Chat Options")

# Initialize session state for memory choice if it doesn't exist
if "memory_choice" not in st.session_state:
    st.session_state.memory_choice = True


def cleanup_temp_files():
    """Clean up temporary files"""
    if "temp_files" in st.session_state:
        for temp_file in st.session_state.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                st.error(f"Error cleaning up temp file {temp_file}: {str(e)}")
        st.session_state.temp_files = []


st.header("Memory Settings")

# This checkbox controls the 'memory_choice' session state variable.
# This state is used by the chat_page to decide whether to include chat history.
st.metric(
    label="Total Messages in Current Session",
    value=len(st.session_state.get("messages", [])),
)

st.divider()

# Temporary Files Management
st.header("File Management")

# Show number of temporary files
temp_files_count = len(st.session_state.get("temp_files", []))
st.metric(
    label="Temporary Image Files",
    value=temp_files_count,
    help="Images uploaded during the chat session are stored as temporary files",
)

# Clean up temp files button
if temp_files_count > 0:
    if st.button("🗑️ Clean up temporary files", type="secondary"):
        cleanup_temp_files()
        st.success("Temporary files cleaned up!")
        st.rerun()

    # Show file details in an expander
    with st.expander("View temporary file details"):
        for i, temp_file in enumerate(st.session_state.get("temp_files", [])):
            file_exists = os.path.exists(temp_file)
            file_size = ""
            if file_exists:
                try:
                    size_bytes = os.path.getsize(temp_file)
                    file_size = f" ({size_bytes} bytes)"
                except Exception as e:
                    console = Console()
                    console.print(e)
                    file_size = " (size unknown)"

            st.code(f"{i + 1}. {temp_file}{file_size}")
            if not file_exists:
                st.caption("⚠️ File no longer exists")
else:
    st.caption("No temporary files currently stored.")

st.divider()

# Export Options
st.header("Export Chat")
if st.session_state.get("messages"):
    # Create a markdown string from the chat history
    chat_export_md = ""
    for msg in st.session_state.messages:
        role = msg["role"].title()
        content = msg["content"]

        # Handle multimodal content
        if isinstance(content, list):
            text_parts = []
            image_count = 0
            for item in content:
                if item["type"] == "text":
                    if not item["text"].startswith("Uploaded image file paths:"):
                        text_parts.append(item["text"])
                elif item["type"] == "image_url":
                    image_count += 1

            content_str = " ".join(text_parts)
            if image_count > 0:
                content_str += f" [Contains {image_count} image(s)]"
            chat_export_md += f"**{role}**: {content_str}\n\n"
        else:
            chat_export_md += f"**{role}**: {content}\n\n"

    st.download_button(
        "Download as Markdown (.md)",
        chat_export_md,
        "chat_history.md",
        "text/markdown",
    )

    # Create a JSON string from the chat history (excluding base64 image data for size)
    export_messages = []
    for msg in st.session_state.messages:
        if isinstance(msg["content"], list):
            # Filter out base64 image data for export
            filtered_content = []
            for item in msg["content"]:
                if item["type"] == "text":
                    filtered_content.append(item)
                elif item["type"] == "image_url":
                    filtered_content.append(
                        {
                            "type": "image_url",
                            "image_url": "[IMAGE DATA REMOVED FOR EXPORT]",
                        }
                    )
            export_messages.append({"role": msg["role"], "content": filtered_content})
        else:
            export_messages.append(msg)

    chat_export_json = json.dumps(export_messages, indent=2)
    st.download_button(
        "Download as JSON (.json)",
        chat_export_json,
        "chat_history.json",
        "application/json",
    )
else:
    st.caption("No messages to export yet. Start a conversation first!")

st.divider()

# Clear Chat Option
st.header("Clear Chat")
if st.session_state.get("messages"):
    st.warning(
        "This will permanently delete your chat history and clean up temporary files."
    )
    if st.button("🗑️ Clear All Chat History", type="secondary"):
        # Clean up temp files first
        cleanup_temp_files()
        # Clear messages
        st.session_state.messages = []
        st.success("Chat history cleared!")
        st.rerun()
else:
    st.caption("No chat history to clear.")
