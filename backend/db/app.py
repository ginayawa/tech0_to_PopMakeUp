import streamlit as st
import pandas as pd
from utils import *



with st.container(border=True):
  st.header('XXXX株式会社')
   
col1, col2, col3 = st.columns(3)

with col1:
   with st.container(border=True, height=650):
    st.markdown('<h3>2024年4月</h3></br></br></br>', unsafe_allow_html=True)
    st.markdown('総利用食数')
    st.markdown(f"<h2 style='text-align:right; font-weight:bold;'>{trn_num_ct}<span style='font-size:0.5em;'>食</span></h2></br>", unsafe_allow_html=True)
    st.markdown('総利用者数')
    st.markdown(f"<h2 style='text-align:right; font-weight:bold;'>{trn_user_ct}<span style='font-size:0.5em;'>人</span></h2>", unsafe_allow_html=True)

with col2:
    with st.container(border=True, height=650):
      st.markdown('<h5>一人当たりの週平均利用日数</h5>', unsafe_allow_html=True)
      st.plotly_chart(fig)
      st.write(f'週3回以上の利用者　{round(rate_3over_week*100,1)}%')
      st.write(f'前月比　{plus_minus_mean_ct}{round(abs(rate_3over_week - rate_3over_week_pre)*100,1)}%')

with col3:
   with st.container(border=True,height=650):
     st.header('---')

with st.container(border=True):
  st.header('---')













# config適用
# streamlit config show