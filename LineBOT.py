from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import datetime

app = Flask(__name__)

# 請將下方的變數替換為你的Channel Access Token和Channel Secret
line_bot_api = LineBotApi('b0VnxuVxisPGfY0cWs5euuAeb43LxslKl//TsrA26jS88J2L98odvJDbjTHkSbOLsSYKQJSCMB/sVvGedFZz27/gyO8dgBwVjLaQpxuEIlc1gePykXTu7ju7E1JxkIIfUOn82fYGP8gjffAevdvUGQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d118994b9d3e9352e1c369935d75733b')

# 定義提醒時間
reminders = {
    "08:00": "早上八點囉，可以開始喝水了，建議每天攝取 3000 C.C. 的水份",
    "10:30": "十點半囉，你有喝 800~1000 c.c. 了嗎",
    "13:00": "下午一點，應該至少要喝 1500 c.c. 囉",
    "15:30": "下午三點半，快下班了，你離 2000 c.c. 還多遠？",
    "18:00": "下午六點啦，該不會2000還沒達標吧？建議要喝到 3000 C.C. 噢",
    "20:30": "八點半了，這批喝完就可以慢慢停囉，晚上喝太多反而影響睡眠了，明天繼續吧"
}

# 處理 Line 的 Webhook 請求
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # 獲取請求體
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理收到的消息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當用戶傳送「喵嗷」時，回覆「嘎阿」
    if event.message.text == '喵嗷':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='嘎阿')
        )
        
# 定時發送提醒消息
def send_reminders():
    now = datetime.datetime.now().strftime("%H:%M")
    if now in reminders:
        line_bot_api.push_message('<YOUR_USER_ID>', TextSendMessage(text=reminders[now]))

if __name__ == "__main__":
    # 設定定時任務，每分鐘檢查一次是否需要發送提醒消息
    import threading
    reminder_thread = threading.Thread(target=lambda: schedule.every().minute.do(send_reminders))
    reminder_thread.start()

    # 執行 Flask 應用
    app.run()
