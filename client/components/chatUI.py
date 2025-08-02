import streamlit as st
from utils.api import ask_question

def render_chat():
    st.subheader("💬 Chat with your AI-powered assistant")

    if "messages" not in st.session_state:
        st.session_state.messages=[]

    # render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Type your question....")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = ask_question(user_input)
        if response.status_code == 200:
            data=response.json()
            answer=data["response"]
            sources=data.get("sources", [])

            output = answer if not sources else answer + "\n\n" + format_sources_str(sources)
            print("OUTPUT:", output)

            st.chat_message("assistant").markdown(output)

            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Error: {response.text}")

def format_sources_str(sources):
    if not sources:
        return ""
    
    sources_header_text = "🗂️ Sources (Pinecone):  "
    res = sources_header_text

    for source_str in sources:
        res += f"\n\n= `{source_str}`"

    return res

