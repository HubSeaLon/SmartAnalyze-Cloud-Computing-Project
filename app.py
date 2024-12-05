from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PIL import Image
import time 
load_dotenv()

app = Flask(__name__)
app.secret_key = "projet_cloud"

# Configuration Azure Text Analytics
key = os.environ.get('TEXT_ANALYTICS_KEY')
endpoint = os.environ.get('TEXT_ANALYTICS_ENDPOINT')

credential = AzureKeyCredential(key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

# Configuration Azure Computer Vision
VISION_KEY = os.environ.get("VISION_KEY")
VISION_ENDPOINT = os.environ.get("VISION_ENDPOINT")

# Utiliser CognitiveServicesCredentials pour l'authentification
credentials = CognitiveServicesCredentials(VISION_KEY)
vision_client = ComputerVisionClient(endpoint=VISION_ENDPOINT, credentials=credentials)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text-analysis', methods=['GET', 'POST'])
def text_analysis():
    sentiment = None
    score = None
    avis = None
    language = None
    key_phrases = []
    entities = []
    summary = None

    if 'historique' not in session:
        session['historique'] = []

    if request.method == 'POST':
        avis = request.form['avis']
        if avis:  # Vérifier que l'avis n'est pas vide
            documents = [avis]

            # Analyse de sentiments
            sentiment_response = text_analytics_client.analyze_sentiment(documents=documents)[0]
            sentiment = sentiment_response.sentiment

            if sentiment == "positive":
                score = float(sentiment_response.confidence_scores.positive)
            elif sentiment == "neutral":
                score = float(sentiment_response.confidence_scores.neutral)
            elif sentiment == "negative":
                score = float(sentiment_response.confidence_scores.negative)
            else:
                score = 0.0

            score = round(score * 100, 2)

            # Détection de la langue
            language_response = text_analytics_client.detect_language(documents=documents)[0]
            language = language_response.primary_language.name

            # Extraction de phrases clés
            key_phrases_response = text_analytics_client.extract_key_phrases(documents=documents)[0]
            key_phrases = key_phrases_response.key_phrases

            # Reconnaissance d'entités nommées
            entity_response = text_analytics_client.recognize_entities(documents=documents)[0]
            entities = [(entity.text, entity.category) for entity in entity_response.entities]

            # Résumé automatique
            if len(avis.split()) > 10:  # Vérifier que l'avis est suffisamment long
                poller = text_analytics_client.begin_extract_summary(documents=documents, max_sentence_count=2)
                summary_results = poller.result()

                for result in summary_results:
                    if not result.is_error:
                        summary = " ".join([sentence.text for sentence in result.sentences])
                    else:
                        summary = "Résumé non disponible en raison d'une erreur."
                
                # Vérifier si le résumé est identique à l'avis
                if summary.strip() == avis.strip():
                    summary = "Le résumé est identique à l'avis, car le texte est déjà concis."
            else:
                summary = "L'avis est trop court pour générer un résumé."

            # Ajouter le nouvel avis à l'historique
            session['historique'].append({
                'avis': avis,
                'sentiment': sentiment,
                'score': score,
                'language': language,
                'key_phrases': key_phrases,
                'entities': entities,
                'summary': summary
            })
            session.modified = True

        return redirect(url_for('text_analysis'))

    return render_template('texte_analyse.html', historique=session['historique'])





UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Fonction pour redimensionner les images
def resize_image(input_path, output_path, max_size=4096):
    with Image.open(input_path) as img:
        img.thumbnail((max_size, max_size))
        img.save(output_path)


@app.route('/image-analysis', methods=['GET', 'POST'])
def image_analysis():
    descriptions = []
    objects = []
    ocr_text = None
    error_message = None
    uploaded_image_url = None

    if request.method == 'POST':
        if 'image' not in request.files:
            error_message = "Aucune image sélectionnée."
            return render_template('image_analyse.html', error_message=error_message)

        image_file = request.files['image']
        if image_file.filename == '':
            error_message = "Aucune image sélectionnée."
            return render_template('image_analyse.html', error_message=error_message)

        # Sauvegarder l'image temporairement
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)

        # URL pour afficher l'image
        uploaded_image_url = f"/uploads/{filename}"

        try:
            # Redimensionner si nécessaire
            resized_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"resized_{filename}")
            resize_image(filepath, resized_filepath)

            # Analyse avec Azure Computer Vision
            with open(resized_filepath, "rb") as image_stream:
                # 1. Génération de description
                description_results = vision_client.describe_image_in_stream(image_stream)
                descriptions = [caption.text for caption in description_results.captions]

            with open(resized_filepath, "rb") as image_stream:
                # 2. Détection d'objets
                object_results = vision_client.detect_objects_in_stream(image_stream)
                objects = [(obj.object_property, obj.confidence) for obj in object_results.objects]

            with open(resized_filepath, "rb") as image_stream:
                # 3. Extraction de texte (OCR)
                ocr_results = vision_client.read_in_stream(image_stream, raw=True)
                ocr_operation_location = ocr_results.headers["Operation-Location"]
                operation_id = ocr_operation_location.split("/")[-1]

                while True:
                    result = vision_client.get_read_result(operation_id)
                    if result.status.lower() in ["notstarted", "running"]:
                        time.sleep(1)  # Attendre que l'OCR soit terminé
                    elif result.status.lower() == "succeeded":
                        ocr_text = " ".join(
                            [line.text for page in result.analyze_result.read_results for line in page.lines]
                        )
                        break
                    else:
                        error_message = "Une erreur est survenue lors de l'analyse OCR."
                        break

        except Exception as e:
            error_message = f"Une erreur est survenue : {e}"        

    return render_template(
        'image_analyse.html',
        descriptions=descriptions,
        objects=objects,
        ocr_text=ocr_text,
        error_message=error_message,
        uploaded_image_url=uploaded_image_url
    )

# Route pour servir les images uploadées
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
