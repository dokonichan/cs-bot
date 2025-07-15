import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def tanya_gemini(pesan_user):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    data = {
        "contents": [{
            "parts": [{"text": pesan_user}]
        }]
    }
    res = requests.post(url, json=data)
    return res.json()['candidates'][0]['content']['parts'][0]['text']

def kirim_pesan_ke_fonnte(no_hp, isi_pesan):
    headers = {
        "Authorization": FONNTE_TOKEN
    }
    data = {
        "target": no_hp,
        "message": isi_pesan
    }
    response = requests.post("https://api.fonnte.com/send", data=data, headers=headers)
    return response.json()

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    sender = data.get('number')
    message = data.get('message')

    if sender and message:
        jawaban = tanya_gemini(message)
        kirim_pesan_ke_fonnte(sender, jawaban)
        return jsonify({"status": "sukses"}), 200
    return jsonify({"error": "data tidak lengkap"}), 400

@app.route('/', methods=['GET'])
def home():
    return "CS WhatsApp AI aktif!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
