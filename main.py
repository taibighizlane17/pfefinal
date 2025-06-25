from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import openai
import io

app = Flask(__name__)
CORS(app)

# Configuration de l'API OpenRouter avec DeepSeek
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

# Stockage temporaire du contenu extrait du PDF
pdf_content = ""

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global pdf_content

    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400

    file = request.files['file']

    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Le fichier doit être un PDF'}), 400

    try:
        reader = PyPDF2.PdfReader(file)
        pdf_content = ""
        for page in reader.pages:
            pdf_content += page.extract_text()
        return jsonify({'message': 'Fichier analysé avec succès'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ask', methods=['POST'])
def ask_question():
    global pdf_content

    data = request.get_json()
    question = data.get('question', '')

    if not pdf_content:
        return jsonify({'error': 'Aucun document analysé'}), 400

    prompt = f"Voici le contenu du document PDF :\n\n{pdf_content}\n\nQuestion : {question}\nRépondez en français de manière claire et concise."

    try:
        response = openai.ChatCompletion.create(
            model="deepseek-ai/deepseek-chat",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert dans l'analyse de documents PDF."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response['choices'][0]['message']['content']
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
