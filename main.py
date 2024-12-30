# encoding: utf-8 
from flask import Flask  
from api import conversation

app = Flask(__name__)

@app.route('/') 
def home_route(): 
    return "Bonjour C'est C2Copine"

@app.route('/api/conversation/audio', methods=['POST']) 
def api_conversation_audio():
    return conversation.executor()

@app.route('/api/conversation/audio/download', methods=['GET']) 
def api_conversation_audio_download():
    return conversation.audio_download()

if __name__ == '__main__': 
    print("C2Copine Python Server is running at port http://localhost:9020")
    app.run(host="0.0.0.0", port=9020, debug=True)




