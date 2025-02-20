
from flask import Flask, request, jsonify
import joblib
from sentence_transformers import SentenceTransformer
import logging


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)



app = Flask(__name__)


try:
    clf = joblib.load('svm.joblib')  # Ensure svm.joblib is available
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logging.info("Model and classifier loaded successfully.")
except Exception as e:
    logging.critical(f"Failed to load model or classifier: {e}")
    raise



@app.get('/status')
def status():
    logging.info("Received status check request.")
    return jsonify({'status': 'OK'})




@app.route('/score_headlines', methods=['POST'])
def score_headlines():
    logging.info("Received request for scoring headlines.")
    
    try:
        data = request.get_json()
        if not data or 'headlines' not in data:
            logging.warning("Invalid request: Missing 'headlines' key in JSON.")
            return jsonify({'error': 'Invalid request, expected JSON with key "headlines"'}), 400

        headlines = data['headlines']
        logging.debug(f"Received Headlines: {headlines}")
        
        embeddings = model.encode(headlines)
        predicted_labels = clf.predict(embeddings).tolist()
        logging.debug(f"Predicted Labels: {predicted_labels}")

        return jsonify({'labels': predicted_labels})
    except Exception as e:
        logging.error(f"Error during headline scoring: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logging.info("Starting the Flask application on port 8088.")
    app.run(debug=True, host='0.0.0.0', port=8088)