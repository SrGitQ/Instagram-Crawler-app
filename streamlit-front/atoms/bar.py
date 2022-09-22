import streamlit as st
def navbar():
  col1, col2 = st.columns([1,3])
  col1.markdown("<h1 style='text-align: center; color: white;'>Statigram</h1>", unsafe_allow_html=True)
  return col2.text_input(' ', placeholder = 'Search',)