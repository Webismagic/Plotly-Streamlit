import plotly.express as px
import streamlit as st
from model import Graphic as gph

gf = gph.Graphics(2023)
fig1 = gf.get_graphic_type_1(2023)
fig2 = gf.get_graphic_type_2(2023)

tab1, tab2 = st.tabs(["Chart 1", "Chart 2"])
with tab1:
    # 1.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
with tab2:
    # 2.
    st.plotly_chart(fig2, theme=None, use_container_width=True)

