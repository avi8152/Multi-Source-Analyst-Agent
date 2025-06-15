import streamlit as st
import os
from main import get_answer_response
from fpdf import FPDF

# Create folders if not present
os.makedirs("src/data/sheets", exist_ok=True)
os.makedirs("src/data/docs", exist_ok=True)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📊 Multi-Source Analyst Agent")

# Sidebar: Upload and Settings
with st.sidebar:
    st.header("📁 Upload Files")

    if "web_search" not in st.session_state:
        st.session_state.web_search = True

    uploaded_file = st.file_uploader("Upload a CSV or PDF", type=["csv", "pdf"])
    if uploaded_file:
        filename = uploaded_file.name
        folder = "src/data/sheets" if filename.endswith(".csv") else "src/data/docs"
        file_path = os.path.join(folder, filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded `{filename}`")
        st.rerun()

    csv_files = [f for f in os.listdir("src/data/sheets") if f.endswith(".csv")]
    pdf_files = [f for f in os.listdir("src/data/docs") if f.endswith(".pdf")]

    st.markdown("### 📄 Uploaded Files")
    if not csv_files and not pdf_files:
        st.info("No files uploaded yet.")
    else:
        for file in csv_files:
            st.write(f"📊 {file}")
        for file in pdf_files:
            st.write(f"📄 {file}")

    files_uploaded = bool(csv_files or pdf_files)
    st.markdown("### 🌐 Web Search Option")
    if files_uploaded:
        st.session_state.web_search = st.toggle("Enable Web Search", value=st.session_state.web_search)
    else:
        st.toggle("Enable Web Search", value=True, disabled=True)

# Chat State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input with form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask your question:", placeholder="Type your question here...", key="user_input")
    submitted = st.form_submit_button("Submit")
# --- Buttons: Clear & Export ---
col2, col3 = st.columns([3, 3])
with col2:
    clear = st.button("🗑️ Clear Chat", use_container_width=True)
with col3:
    export = st.button("📥 Export PDF", use_container_width=True)

if clear:
    st.session_state.chat_history = []
    for folder in ["src/data/sheets", "src/data/docs"]:
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
    st.success("✅ Chat and files cleared.")
    st.rerun()


if export and st.session_state.chat_history:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for chat in st.session_state.chat_history:
        pdf.multi_cell(0, 10, f"User: {chat['user']}")
        pdf.multi_cell(0, 10, f"Bot: {chat['bot']}")
        pdf.multi_cell(0, 10, f"Source: {chat['source']}")
        pdf.ln()
    export_path = "chat_history_export.pdf"
    pdf.output(export_path)
    with open(export_path, "rb") as f:
        st.download_button("📄 Download Chat History", f, file_name="chat_history_export.pdf", mime="application/pdf")



# Handle submit
if submitted and user_input.strip():
    with st.spinner("🧠 Generating answer..."):
        try:
            result = get_answer_response.get_answer(user_input, web_search=st.session_state.web_search)
            st.session_state.chat_history.append({
                "user": user_input,
                "bot": result.get("answer", "No answer found."),
                "source": result.get("source", "Unknown")
            })
        except Exception as e:
            st.session_state.chat_history.append({
                "user": user_input,
                "bot": f"Error: {e}",
                "source": "N/A"
            })

# Chat Display

if st.session_state.chat_history:
    st.markdown("### 🗨️ Conversation")
    for chat in st.session_state.chat_history:
        # User message (right)
        st.markdown(
            f"""
            <div class='chat-bubble user'>
                <strong>🧑‍💻 You:</strong><br>{chat['user']}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Bot message (left)
        st.markdown(
            f"""
            <div class='chat-bubble bot'>
                <strong>🤖 Bot:</strong><br>{chat['bot']}
                <div class='source'>📎 Source: {chat['source']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
