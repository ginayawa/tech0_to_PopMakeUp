import sqlite3
import pandas as pd

def select_tbl_sqlite(mytable):
    # SQLiteデータベースに接続
    conn = sqlite3.connect('pop-make-up_DB.db')
    cursor = conn.cursor()

    # SELECTクエリの作成
    select_query = f"""
        SELECT 
            employee_ID, LastName, FirstName, Gender, birthday,HireDate, Department
        FROM {mytable}
    """

    # クエリの実行a
    cursor.execute(select_query)

    # データを取得
    data = cursor.fetchall()

    # DataFrameに変換
    df = pd.DataFrame(data, columns=['employee_ID', 'LastName', 'FirstName', 'Gender', 'birthday', 'HireDate', 'Department'])

    # 接続を閉じる
    cursor.close()
    conn.close()

    return df


