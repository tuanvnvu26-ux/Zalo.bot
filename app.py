import requests
from flask import Flask, jsonify, request
from google import genai

app = Flask(__name__)

# Điền các mã của bạn vào đây
GEMINI_API_KEY = "AQ.Ab8RN6KW0YOvkIZ08pb1QH7Gnsl1M1nbTWA0vaWFs1cSdCTLSQ"
BOT_TOKEN = "1726766149999057268:zYxabjPVSkmMnUjFMAxnoTGEyGoHQCfRSixMOGwfuthzZqyXqOxDxlRwNMWzUdIq"

client = genai.Client(api_key=GEMINI_API_KEY)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(data)

    # Trích xuất nội dung tin nhắn và ID người gửi từ Zalo
    message_text = data.get("message", {}).get("text", "")
    user_id = data.get("sender", {}).get("id", "")

    if message_text and user_id:
        # 1. Gửi câu hỏi sang Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message_text,
        )
        reply_text = response.text

        # 2. Gửi phản hồi lại cho người dùng Zalo
        zalo_api_url = "https://bot-api.zaloplatforms.com/bot1726766149999057268:zYxabjPVSkmMnUjFMAxnoTGEyGoHQCfRSixMOGwfuthzZqyXqOxDxlRwNMWzUdIq/sendMessage"
        headers = {
            "access_token": BOT_TOKEN,
            "Content-Type": "application/json",
        }
        payload = {
            "recipient": {"user_id": user_id},
            "message": {"text": reply_text},
        }
        requests.post(zalo_api_url, json=payload, headers=headers)

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
