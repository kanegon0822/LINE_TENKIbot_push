import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.models import messages
import psycopg2
import requests

def get_connection():
    dsn=os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)
conn=get_connection()
cur=conn.cursor()

# 取得した天気APIキーを入力
apiKey = os.environ['TENKI_API']
# ベースURL
baseUrl = "http://api.openweathermap.org/data/2.5/weather?"

CHANNEL_ACCESS_TOKEN=os.environ['CHANNEL_ACCESS_TOKEN']
line_bot_api=LineBotApi(CHANNEL_ACCESS_TOKEN)

def main():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM USER_info')
            table=cur.fetchall()
            cur.close()
        conn.close()
    for infolist in table:
        USER_ID=infolist[1]
        place=infolist[2]
        # URL作成
        completeUrl = baseUrl + "q=" + place+"&appid=" + apiKey
        # レスポンス
        response = requests.get(completeUrl) 
        # レスポンスの内容をJSONフォーマットからPythonフォーマットに変換
        cityData = response.json()

        messages=TextSendMessage(text=
            '今日の天気は、'+cityData["weather"][0]["description"]+'です。\n最高気温は、'+cityData["main"]["temp_max"] - 273.15+'℃です。\n今日も気を付けて行ってらっしゃい！！'
        )
        line_bot_api.push_message(USER_ID,messages=messages)

if __name__=='__main__':
    main()
