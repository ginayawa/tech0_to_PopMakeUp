import plotly.graph_objects as go
import pandas as pd

from crud import select_tbl




stores = select_tbl('stores')
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
  return trn_num_ct, trn_user_ct, user_trn_ct, user_trn_ct_sum, mean_ct, rate_3over_week

#当月
this_month = pd.to_datetime('2024-04-01')
trn_num_ct, trn_user_ct, user_trn_ct, user_trn_ct_sum, mean_ct, rate_3over_week = fnc1(this_month)

# 前月
target_pre_month = this_month - pd.DateOffset(months=1)
trn_num_ct_pre, trn_user_ct_pre, user_trn_ct_pre, user_trn_ct_sum_pre, mean_ct_pre, rate_3over_week_pre = fnc1(this_month)

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
      dict(text=f'前月比  {plus_minus_mean_ct}{abs(dif_mean_ct).round(1)}回', x=0.5, y=0, font_size=20, showarrow=False)
      ],
    legend=dict(orientation='h', y=1.1),
    width=200
)
fig.update_traces(direction="clockwise")