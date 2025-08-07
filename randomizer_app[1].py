import streamlit as st
import pandas as pd
import numpy as np
from itertools import filterfalse
from io import StringIO

if 'winner_text' not in st.session_state:
    st.session_state.winner_text = ""
if 'file' not in st.session_state:
    st.session_state.file = None
if 'random_df' not in st.session_state:
    st.session_state.random_df = []
if 'length_df' not in st.session_state:
    st.session_state.length_df = 0
if 'refreshed' not in st.session_state:
    st.session_state.refreshed = False
if 'count' not in st.session_state:
    st.session_state.count = 0

def raffle():
    if st.session_state.length_df > 0:
        st.session_state.count+=1
        np.random.shuffle(st.session_state.random_df)
        winner = st.session_state.random_df[-1]
        st.session_state.winner_text = "Winner #" + str(st.session_state.count) + " is " + str(winner)
        st.balloons()
        clean = [*filterfalse(lambda i: i == winner, st.session_state.random_df)]
        st.session_state.random_df = clean
        st.session_state.length_df = len(st.session_state.random_df)
    else:
        st.session_state.winner_text = "No more entries to pick from :("

def reset():
    if st.session_state.file is not None:
        file_content = st.session_state.file.getvalue().decode("utf-8")
        st.session_state.winner_text = ""
        st.session_state.count = 0
        df = pd.read_csv(StringIO(file_content))
        repeat_df = df.loc[df.index.repeat(df.iloc[:, 1])]
        st.session_state.random_df = list(repeat_df.iloc[:, 0])
        st.session_state.length_df = len(st.session_state.random_df)
        st.session_state.refreshed = True

st.title("RAFFLE TIME")
st.write("by :red[Emirates Skywards]")

st.subheader("File Selection: ")
st.session_state.file = st.file_uploader("Pick the csv file", type="csv")

if (st.session_state.file is not None and not st.session_state.refreshed):
    reset()

st.button("Start/Reset", on_click=reset, use_container_width=True)

st.subheader("Select a Winner: ")
st.button("Find A Winner", disabled=(st.session_state.file is None), icon="🎉", on_click=raffle, use_container_width=True)

st.title(st.session_state.winner_text)