from flask import Flask, jsonify, render_template, request, redirect
from itsdangerous import encoding
import speech_recognition as sr
import html
import logging
from translate import Translator
from deep_translator import GoogleTranslator

app = Flask(__name__)

logging.basicConfig(filename='record.log', encoding='utf-8', level=logging.INFO, format=f'[%(asctime)s] %(levelname)s : %(message)s')

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")
        if "audio_data" not in request.files:
            return redirect(request.url)
        file = request.files["audio_data"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, language='bn-IN')
            # print(transcript)
            app.logger.info("Bengali text: {}".format(transcript))
            # translator = Translator(from_lang="bengali",to_lang="english")
            translator = GoogleTranslator(source='bn', target='en')
            translation = translator.translate(transcript)
            translation = html.unescape(translation)
            # print(translation)
            app.logger.info("English text: {}".format(translation))
            return jsonify({'ben_text': transcript, 'eng_text': translation})

    return render_template('index.html', transcript="transcript")

@app.route("/translate", methods=["POST"])
def translate():
    if request.method == "POST":
        text = request.form['text']
        # t = text.encode('utf-8')
        # t1 = text.encode('raw-unicode-escape').decode('utf-8')
        app.logger.info("Bengali text: {}".format(text))
        # translator= Translator(from_lang="bengali",to_lang="english")
        translator = GoogleTranslator(source='bn', target='en')
        translation = translator.translate(text)
        # print(translation)
        app.logger.info("English text: {}".format(html.unescape(translation)))
        return jsonify({'eng_text': html.unescape(translation)})

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
