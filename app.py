import plotly.express as px
import streamlit as st
from model import Graphic as gph

if 'active_year' not in st.session_state:
    st.session_state.active_year = 2023
  
year = st.session_state.active_year

species = {
    0: 'bateau',
    1: 'Balaenoptera borealis',
    2: 'Globicephala macrorhynchus',
    3: 'Stenella coeruleoalba',
    4: 'Stenella frontalis',
    5: 'Delphinus delphis',
    6: 'Grampus griseus',
    7: 'Physeter macrocephalus',
    8: 'Tursiops truncatus'
}

if 'species_number' not in st.session_state:
    st.session_state.species_number = 0
  
species_chosen = st.session_state.species_number

gf = gph.Graphics(year)
fig1 = gf.get_graphic_type_1(year)
fig1h = gf.get_graphic_type_1(year,2)
fig2 = gf.get_graphic_type_2(year)
fig3 = gf.get_graphic_type_3(year)
#fig4 = gf.get_graphic_type_4(year)
#fig5 = gf.get_graphic_type_5(year)
fig6 = gf.get_graphic_type_6(year)
fig7 = gf.get_graphic_type_7(year)
fig8 = gf.get_graphic_type_8()
#fig9 = gf.get_graphic_type_9()
#fig10 = gf.get_graphic_type_10()
fig11 = gf.get_graphic_type_11(int(species_chosen))
fig12 = gf.get_graphic_type_12(year)
fig13 = gf.get_graphic_type_13(year)

tab1, tab1h, tab2, tab3, tab6, tab7, tab8, tab11, tab12, tab13 = st.tabs(["Chart 1", "Chart 2", "Chart 3",
                                                                        "Chart 4","Chart 5", "Chart 6", "Chart 7",
                                                                        "Chart 8", "Chart 9", "Chart 10"])
with tab1:
    # 1.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
with tab1h:
    # 1h.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig1h, theme="streamlit", use_container_width=True)
with tab2:
    # 2.
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
with tab3:
    # 3.
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
#with tab4:
    # 4.
    #st.plotly_chart(fig4, theme="streamlit", use_container_width=True)
#with tab5:
    # 5.
    #st.plotly_chart(fig5, theme="streamlit", use_container_width=True)
with tab6:
    # 6.
    st.plotly_chart(fig6, theme="streamlit", use_container_width=True)
with tab7:
    # 7.
    st.plotly_chart(fig7, theme="streamlit", use_container_width=True)
with tab8:
    # 8.
    st.plotly_chart(fig8, theme="streamlit", use_container_width=True)
#with tab9:
    # 9.
    #st.plotly_chart(fig9, theme="streamlit", use_container_width=True)
#with tab10:
    # 10.
    #st.plotly_chart(fig10, theme="streamlit", use_container_width=True)
with tab11:
    # 11.
    species_chosen = st.selectbox('choose a species?', options=list(species.keys()),format_func=lambda x: species[x], key="species_number")
    st.plotly_chart(fig11, theme="streamlit", use_container_width=True)
with tab12:
    # 12.
    st.plotly_chart(fig12, theme="streamlit", use_container_width=True)
with tab13:
    # 13.
    st.plotly_chart(fig13, theme="streamlit", use_container_width=True)

year = st.select_slider(
    'Select a year',
    options=[2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023], value=2023, key="active_year")

st.write('Chosen year:', year)
  
