import plotly.express as px
import streamlit as st
from model import Graphic as gph

gf = gph.Graphics(2023)
fig1 = gf.get_graphic_type_1(2023)
fig2 = gf.get_graphic_type_2(2023)
fig3 = gf.get_graphic_type_3(2023)
fig4 = gf.get_graphic_type_4(2023)
fig12 = gf.get_graphic_type_12b(2023)

tab1, tab2, tab3, tab4, tab12 = st.tabs(["Chart 1", "Chart 2", "Chart 3", "Chart 4", "Chart 12"])
with tab1:
    # 1.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
with tab2:
    # 2.
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
with tab3:
    # 3.
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
with tab4:
    # 4.
    st.plotly_chart(fig4, theme="streamlit", use_container_width=True)
with tab12:
    # 12.
    st.plotly_chart(fig12, theme="streamlit", use_container_width=True)
