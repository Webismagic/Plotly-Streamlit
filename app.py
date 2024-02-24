import plotly.express as px
import streamlit as st
from model import Graphic as gph

gf = gph.Graphics(2023)
fig1 = gf.get_graphic_type_1(2023)
fig2 = gf.get_graphic_type_2(2023)
fig3 = gf.get_graphic_type_3(2023)
fig4 = gf.get_graphic_type_4(2023)
fig5 = gf.get_graphic_type_5(2023)
fig6 = gf.get_graphic_type_6(2023)
fig7 = gf.get_graphic_type_7(2023)
fig8 = gf.get_graphic_type_8()
fig9 = gf.get_graphic_type_9()
fig10 = gf.get_graphic_type_10()
fig11 = gf.get_graphic_type_11()
fig12 = gf.get_graphic_type_12b(2023)
fig13 = gf.get_graphic_type_13(2023)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs(["Chart 1", "Chart 2", "Chart 3",
                                                                              "Chart 4", "Chart 5", "Chart 6",
                                                                              "Chart 7", "Chart 8", "Chart 9",
                                                                              "Chart 10", "Chart 11", "Chart 12", "Chart 13"])
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
with tab5:
    # 5.
    st.plotly_chart(fig5, theme="streamlit", use_container_width=True)
with tab6:
    # 6.
    st.plotly_chart(fig6, theme="streamlit", use_container_width=True)
with tab7:
    # 7.
    st.plotly_chart(fig7, theme="streamlit", use_container_width=True)
with tab8:
    # 8.
    st.plotly_chart(fig8, theme="streamlit", use_container_width=True)
with tab9:
    # 9.
    st.plotly_chart(fig9, theme="streamlit", use_container_width=True)
with tab10:
    # 10.
    st.plotly_chart(fig10, theme="streamlit", use_container_width=True)
with tab11:
    # 11.
    st.plotly_chart(fig11, theme="streamlit", use_container_width=True)
with tab12:
    # 12.
    st.plotly_chart(fig12, theme="streamlit", use_container_width=True)
with tab13:
    # 13.
    st.plotly_chart(fig13, theme="streamlit", use_container_width=True)
