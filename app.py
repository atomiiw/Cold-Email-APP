import streamlit as st
from page import page1, page2, page3, page4

if "page" not in st.session_state:
    st.session_state.page = 1

# Display the appropriate page in the container
if st.session_state.page == 1:
    page1()
elif st.session_state.page == 2:
    page2()
elif st.session_state.page == 3:
    page3()
elif st.session_state.page == 4:
    page4()