import streamlit as st
import pandas as pd
from utils.variables import *

st.set_page_config(
  layout="wide"
)


with st.container(border=True):
  st.header('XXXX株式会社')
   
col1, col2, col3 = st.columns(3)

with col1:
  with st.container(border=True, height=500):
    st.markdown('<h5>2024年4月</h5></br></br>', unsafe_allow_html=True)
    st.markdown('総利用食数')
    st.markdown(f"<h2 style='text-align:center; font-weight:bold;'>{trn_num_ct}<span style='font-size:0.5em;'>食</span></h2>", unsafe_allow_html=True)
    st.markdown('総利用者数')
    st.markdown(f"<h2 style='text-align:center; font-weight:bold;'>{trn_user_ct}<span style='font-size:0.5em;'>人</span></h2>", unsafe_allow_html=True)

with col2:
    with st.container(border=True, height=500):
      st.markdown('<h5>一人当たりの週平均利用日数</h5>', unsafe_allow_html=True)
      with st.container(height=300, border=False):
        st.write('<div style="display: flex; justify-content: center; ">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
      st.markdown(f"<h5 style='text-align:center; font-weight:bold;'>前月比  {plus_minus_mean_ct}{abs(dif_mean_ct).round(1)}回</h5>", unsafe_allow_html=True)
      st.write(f'週3回以上の利用者　{round(rate_3over_week*100,1)}%')
      st.write(f'前月比　{plus_minus_mean_ct}{round(abs(rate_3over_week - rate_3over_week_pre)*100,1)}%')

with col3:
   with st.container(border=True,height=500):
      st.markdown('<h5>年代別利用率</h5>', unsafe_allow_html=True)
    #  st.plotly_chart(fig2)
      st.write('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
      st.plotly_chart(fig2, use_container_width=True)

with st.container(border=True):
  st.markdown(f"<h4 style='text-align:center; font-weight:bold;'>部署別利用食数</h4>", unsafe_allow_html=True)
  st.write('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
  st.plotly_chart(fig3, use_container_width=True)













# config適用
# streamlit config show