import streamlit as st

def square(n):
    return n ** 2

def cube(n):
    return n ** 3

def fourth_power(n):
    return n ** 4

def fifth_power(n):
    return n ** 5

st.title("Power calculator")
st.write("This app calculates the power of a number raised to an exponent.")

num = st.number_input("Enter a base number:", value=1, step=1)

if st.button("Calculate"):
    st.write(f"{num} squared is {square(num)}")
    st.write(f"{num} cubed is {cube(num)}")
    st.write(f"{num} to the fourth power is {fourth_power(num)}")
    st.write(f"{num} to the fifth power is {fifth_power(num)}")
