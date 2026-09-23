
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Local LibreTranslate server
LIBRETRANSLATE_URL = "http://127.0.0.1:5000/translate"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.get_json()

        text = data.get("text", "").strip()
        source = data.get("source", "en")
        target = data.get("target", "hi")

        if not text:
            return jsonify({
                "error": "Please enter some text."
            }), 400

        # Same language: no API call needed
        if source == target:
            return jsonify({
                "translation": text
            })

        payload = {
            "q": text,
            "source": source,
            "target": target,
            "format": "text"
        }

        response = requests.post(
            LIBRETRANSLATE_URL,
            json=payload,
            timeout=60
        )

        print("LibreTranslate Status:", response.status_code)
        print("LibreTranslate Response:", response.text)

        if response.status_code != 200:
            return jsonify({
                "error": "Translation service returned an error."
            }), 500

        result = response.json()

        translation = result.get("translatedText")

        if not translation:
            return jsonify({
                "error": "No translation received."
            }), 500

        return jsonify({
            "translation": translation
        })

    except requests.exceptions.RequestException as e:
        print("Connection Error:", e)

        return jsonify({
            "error": "Unable to connect to LibreTranslate."
        }), 500

    except Exception as e:
        print("Translation Error:", e)

        return jsonify({
            "error": "Translation failed."
        }), 500


if __name__ == "__main__":
    # Flask website runs on 5001
    # LibreTranslate is already running on 5000
    app.run(port=5001, debug=True)
