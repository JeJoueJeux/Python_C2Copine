from datetime import datetime
import os
from pathlib import Path
from api.conversation.secret_keys import AZURE_API_KEY_TEXT, AZURE_API_KEY_TEXT_ENDPOINT, AZURE_API_KEY_TTSHD, AZURE_API_KEY_TTSHD_ENDPOINT, AZURE_API_KEY_WHISPER, AZURE_API_KEY_WHISPER_ENDPOINT
from api.models.response import ResponseModel
from flask import request  
from flask import current_app
from flask import Flask, send_file
from openai import AzureOpenAI


class AzureOpenAIAudioConversations:
      
    def __init__(self): 
        pass
    
    def handler(self): 
        t = request.form['type'] 
        if t == "audio":
            return self.audio() 
        elif t == "tts":
            return self.tts_test()
        elif t == "stt":
            return self.stt_test()
        elif t == "text": 
            return self.text_completion_test()
        else:
            return ResponseModel("Params error!", {}).failure_json()
  

    def audio(self):
        if request.files is None or len(request.files) == 0:
            return ResponseModel("No audio found", {}).failure_json()
        f = request.files["file"] 
        user_audio_filepath = self.get_audio_filepath()
        f.save(user_audio_filepath) 
        user_text = self.stt(user_audio_filepath)
        gpt_responded_text = self.text_completion(user_text)
        gen_audio_filepath = self.get_audio_filepath(True)
        result = self.tts(gpt_responded_text, gen_audio_filepath) 
        if result:
            data = {
                "audio_name": self.get_audio_filepath_only(gen_audio_filepath),
                "user_text": user_text,
                "copine_text": gpt_responded_text,
            }
            return ResponseModel("success", data).success_json()
        else:
            return ResponseModel("Try again please", {}).failure_json()
    

    def audio_download(self):
        audio_name = request.args.get('audio_name')
        audio_fullpath = self.get_root_audio_folder() + "/" + audio_name
        return send_file(audio_fullpath, mimetype='audio/wav')


    def tts_test(self):
        speech_file_path = Path(__file__).parent / "speech.wav"
        text = "Bonjour comment ça va? Quel temps fait-il aujourd'hui?"
        result = self.tts(text, speech_file_path)
        return ResponseModel("", result).success_json()
    

    def tts(self, text, audio_to_filepath):
        try:
            client = AzureOpenAI(
              api_key=AZURE_API_KEY_TTSHD,  
              api_version="2024-08-01-preview",
              azure_endpoint=AZURE_API_KEY_TTSHD_ENDPOINT
            )  
            response = client.audio.speech.create(
                model="tts-1",
                voice="nova",
                input=text
            )
            response.stream_to_file(audio_to_filepath)
            return True
        except Exception as e:
            print(f"{e}")
            return False
    

    def stt_test(self):
        speech_file_path = Path(__file__).parent / "speech.wav"
        result = self.stt(speech_file_path)
        return ResponseModel("", result).success_json()


    def stt(self, audio_file):
        try:
            client = AzureOpenAI(
              api_key=AZURE_API_KEY_WHISPER,  
              api_version="2024-08-01-preview",
              azure_endpoint=AZURE_API_KEY_WHISPER_ENDPOINT
            ) 
            with open(audio_file, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                return transcription.text
        except Exception as e:
            print(f"{e}")
            return ""


    def text_completion_test(self): 
        result = self.text_completion()
        return ResponseModel("", result).success_json()


    def text_completion(self, user_text):
        try:
            client = AzureOpenAI(
              api_key=AZURE_API_KEY_TEXT,  
              api_version="2024-08-01-preview",
              azure_endpoint=AZURE_API_KEY_TEXT_ENDPOINT
            )
            messages=[
                {"role": "system", "content": "Vous êtes un professeur de français natif avec un niveau C2 qui aide les gens à améliorer leur langue française, et vous vous appelez C2Copine. Notez que : Assurez-vous d’utiliser le mot 'te', 'tu' au lieu de 'vous', car il s’agit simplement d’une conversation agréable avec des pairs, et votre réponse ne doit pas être trop longue, rendez-la courte, tout comme discuter avec des amis."},
            ]
            if user_text is not None and len(user_text) > 2:
                messages.append(
                    {"role": "user", "content": user_text}
                )
            response = client.chat.completions.create(
                model="gpt-4o", 
                messages=messages
            ) 
            return response.choices[0].message.content
        except Exception as e:
            print(f"{e}")
            return ""
        

    def get_audio_filepath(self, is_gen = False):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        milliseconds = datetime.now().microsecond // 1000
        if is_gen:
            filename = f"gen_{timestamp}_{milliseconds}.wav"
        else:
            filename = f"user_{timestamp}_{milliseconds}.wav"
        return f"{self.get_audio_gen_folder()}/{filename}"


    def get_audio_gen_folder(self) -> str:
        root_path = current_app.root_path
        audio_gen_folder = os.path.join(root_path, 'audio_gen')
        if not os.path.exists(audio_gen_folder):
            os.makedirs(audio_gen_folder)
        datetime_foler = datetime.now().strftime("%Y-%m-%d")
        dt_gen_folder = os.path.join(audio_gen_folder, datetime_foler)
        if not os.path.exists(dt_gen_folder):
            os.makedirs(dt_gen_folder)
        return dt_gen_folder
    

    def get_root_audio_folder(self):
        root_path = current_app.root_path
        return os.path.join(root_path, 'audio_gen')
    

    def get_audio_filepath_only(self, audio_fullpath):
        return audio_fullpath.replace(self.get_root_audio_folder(), "")