#!/bin/env python3
import os
import streamlit as st
from streamlit_chat import message
from rag import ChatPDF

st.set_page_config(page_title="Q&A Assistant")


def display_messages():
    #st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatPDF()

    st.header("Q&A assistant")

    # Specify the PDF file path here
    
    file_path = r"Path to the.pdf"

    if os.path.exists(file_path) and file_path.lower().endswith('.pdf'):
        with st.spinner():     #with st.spinner(f"{os.path.basename(file_path)}"):
            st.session_state["assistant"].ingest(file_path)
        #st.success("started successfully!")

        display_messages()
        st.text_input("Message", key="user_input", on_change=process_input)
    else:
        st.error("Please specify a valid PDF file path.")

if __name__ == "__main__":
    page()

