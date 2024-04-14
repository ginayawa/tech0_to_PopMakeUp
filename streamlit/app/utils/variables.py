import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import datetime

from utils.crud_alchemy import *
from utils.crud_sqlite import *
# from app import *


########### col1表示データ ###########

trn = select_tbl('transaction_records')

def fnc1(target_dt):
  this_month_trn = trn[ (trn['DATE'].dt.year == target_dt.year) & (trn['DATE'].dt.month == target_dt.month) ]  #指定月のtransitionデータ
  trn_num_ct = this_month_trn.shape[0] #総利用食数
  trn_user_ct = len(this_month_trn['USER_ID'].unique()) #利用人数
  _user_trn_ct = this_month_trn[['USER_ID','DATE']].drop_duplicates()
  _user_trn_ct['use_dt_ct'] = 1
  user_trn_ct = _user_trn_ct.groupby('USER_ID',as_index=False)['use_dt_ct'].sum() #ユーザーごとの利用日数
  user_trn_ct['use_dt_ct_per_week'] = round(user_trn_ct['use_dt_ct']/4,0) 
  def labeling(x):
    if x>=5:
      return '5回以上'
    elif x<1:
      return '1回未満'
    else:
      return f'{int(x)}回'
  user_trn_ct['label'] = user_trn_ct['use_dt_ct_per_week'].apply(lambda x: labeling(x))
  user_trn_ct_sum = user_trn_ct.groupby('label',as_index=False).size() # 円グラフ用のテーブル
  mean_ct = user_trn_ct['use_dt_ct_per_week'].mean() #平均利用者数
  user_3over_week = user_trn_ct[user_trn_ct['use_dt_ct_per_week']>=3] 
  user_ct_3over_week = len(user_3over_week['USER_ID'])
  rate_3over_week = user_ct_3over_week/trn_user_ct #週3回以上の利用率
  return this_month_trn, trn_num_ct, trn_user_ct, user_trn_ct, user_trn_ct_sum, mean_ct, rate_3over_week



#当月
this_month = pd.to_datetime('2024-04-01')
this_month_trn, trn_num_ct, trn_user_ct, user_trn_ct, user_trn_ct_sum, mean_ct, rate_3over_week = fnc1(this_month)

# 前月
target_pre_month = this_month - pd.DateOffset(months=1)
last_month_trn, trn_num_ct_pre, trn_user_ct_pre, user_trn_ct_pre, user_trn_ct_sum_pre, mean_ct_pre, rate_3over_week_pre = fnc1(target_pre_month)

#前月との比較
dif_mean_ct = mean_ct - mean_ct_pre
plus_minus_mean_ct = "+" if mean_ct >= 0 else "-"
dif_3over_rate = rate_3over_week - rate_3over_week_pre
plus_minus_mean_ct = "+" if dif_3over_rate >= 0 else "-"

#円グラフ
labels = user_trn_ct_sum['label']
values = user_trn_ct_sum['size']
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
fig.update_layout(
    annotations=[
      dict(text=f'平均{mean_ct.round(1)}回', x=0.5, y=0.5, font_size=20, showarrow=False),
      ],
    legend=dict(orientation='h', y=1.2, x=0.2),
    # width=400,
    height=250,
    margin=dict(l=0, r=0, t=0, b=0)
)
fig.update_traces(direction="clockwise")

#####################################





########### col2表示データ ###########
emp = select_tbl_sqlite('employee')

#クレンジング
def month(text):
  start_index = text.index('-') + 1  # '/'の次の位置から開始
  end_index = text.index('-', start_index)  # 2番目の'/'が出現する位置
  substring = text[start_index:end_index]
  substring = "{:02d}".format(int(substring))
  return substring
def day(text):
  start_index = text.rindex('-') + 1  # '/'の次の位置から開始
  substring = text[start_index:]
  substring = "{:02d}".format(int(substring))
  return substring

emp['birthday'] = emp['birthday'].str.replace('/','-')
emp['birthday'] = emp['birthday'].str[:4] + '-' + emp['birthday'].apply(lambda x: month(x))+ '-' + emp['birthday'].apply(lambda x: day(x))
emp['birthday'] = pd.to_datetime(emp['birthday'])
emp['HireDate'] = emp['HireDate'].str.replace('/','-')
emp['HireDate'] = emp['HireDate'].str[:4] + '-' + emp['HireDate'].apply(lambda x: month(x))+ '-' + emp['HireDate'].apply(lambda x: day(x))
emp['HireDate'] = pd.to_datetime(emp['HireDate'])


# 年代を追加
today = datetime.datetime.now()
def age(birthdate):
  age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
  age = age // 10 * 10 # 年代に変換
  return age
emp['age'] = emp['birthday'].apply(lambda x: age(x))
#####################################




########### col3表示データ ###########
#社員マスタに利用者フラグを付与
users = select_tbl('users')
users_emp = pd.merge(users, emp, on='employee_ID', how='left')
trn_user_id_li = this_month_trn['USER_ID'].unique().tolist()
users_emp['use_fg'] = users_emp['ID'].apply(lambda x: 1 if x in trn_user_id_li else 0)

#年代別に集計
users_emp['emp_ct'] = 1
age_tbl = users_emp.groupby('age',as_index=False)[['emp_ct','use_fg']].sum()
age_tbl['利用者'] = age_tbl['use_fg']/age_tbl['emp_ct'] * 100
age_tbl['未利用者'] = 100 - age_tbl['利用者']
age_tbl = pd.melt(
    age_tbl,
    id_vars=['age','emp_ct','use_fg'],
    value_name='利用率',
    var_name='分類'
  )
age_tbl['age'] = age_tbl['age'].astype(str) + '代'
age_tbl = age_tbl.sort_values('age', ascending=False)

#グラフ作成
color_map = {'利用者': '#415ce0', '未利用者': '#b3b3b3'}
fig2 = px.bar(age_tbl, x='利用率', y='age', color='分類', color_discrete_map=color_map)
fig2.update_yaxes(title_text='')
fig2.update_layout(
  legend=dict(orientation='h', y=1.2),
)
#####################################




########### 部署別グラフ ###########
#ユーザーごとに集計
user_records = this_month_trn.groupby('USER_ID',as_index=False).size()
users_emp = pd.merge(users_emp, user_records, left_on='ID', right_on='USER_ID', how='left' )
users_emp = users_emp.rename(columns={'size':'利用食数'})

#部署別に集計
department_use = users_emp.groupby('Department',as_index=False)['利用食数'].sum()

#グラフ
fig3 = px.bar(department_use, x='Department', y='利用食数', color='利用食数')
fig3.update_yaxes(title_text='')
fig3.update_xaxes(title_text='')
fig3.update_layout(
  # width=1000
)
#####################################