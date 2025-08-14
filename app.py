import streamlit as st

st.title("Power calculator")
st.write("This app calculates the power of a number raised to an exponent.")

num = st.number_input("Enter a base number:",value=1,step=1)

if st.button("Calculate"):
    result_2 = num ** 2
    result_3 = num ** 3
    result_4 = num ** 4
    result_5 = num ** 5
    st.write(f"{num} raised to the power of  2  is : {result_2}.")
    st.write(f"{num} raised to the power of  3  is : {result_3}.")
    st.write(f"{num} raised to the power of  4  is : {result_4}.")
    st.write(f"{num} raised to the power of  5  is : {result_5}.")