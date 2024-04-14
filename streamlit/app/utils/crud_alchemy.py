from sqlalchemy import create_engine, MetaData, Table
import pandas as pd

# SQLiteデータベースファイルへのパス
db_path = 'sqlite:///pop-make-up_DB.db'

# SQLAlchemyエンジンの作成
engine = create_engine(db_path)

# メタデータの作成
metadata = MetaData()

def select_tbl(mytable):
  # テーブルの定義
  your_table = Table(mytable, metadata, autoload_with=engine)

  # SELECTクエリの作成
  select_query = your_table.select()

  # クエリの実行
  with engine.connect() as connection:
      result = connection.execute(select_query)
      df = pd.DataFrame(result.fetchall(), columns=result.keys())

  return df


