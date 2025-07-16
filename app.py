from flask import Flask, render_template, request, jsonify, send_file
import re
import pandas as pd
import io
import os
from datetime import datetime
from model_utils import SentimentAnalyzer

app = Flask(__name__)

# Initialize the sentiment analyzer
sentiment_analyzer = SentimentAnalyzer()

def validate_input(text):
    """Validate input text"""
    if not text or not text.strip():
        return False, "Please enter some text to analyze."
    
    if len(text.strip()) < 3:
        return False, "Text is too short. Please enter at least 3 characters."
    
    if len(text.strip()) > 500:
        return False, "Text is too long. Please enter less than 500 characters."
    
    # Check if text contains only special characters or numbers
    if not re.search(r'[a-zA-Z]', text):
        return False, "Please enter text that contains letters."
    
    return True, ""

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment of input text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        # Validate input
        is_valid, error_message = validate_input(text)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            })
        
        # Perform sentiment analysis
        result = sentiment_analyzer.predict(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'emoji': result['emoji'],
            'color': result['color']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/analyze_batch', methods=['POST'])
def analyze_batch():
    """Analyze sentiment for multiple texts"""
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({
                'success': False,
                'error': 'Please provide texts to analyze.'
            })
        
        if len(texts) > 10:
            return jsonify({
                'success': False,
                'error': 'Maximum 10 texts allowed for batch analysis.'
            })
        
        results = []
        for i, text in enumerate(texts):
            text = text.strip()
            is_valid, error_message = validate_input(text)
            
            if not is_valid:
                results.append({
                    'index': i,
                    'text': text,
                    'error': error_message
                })
            else:
                result = sentiment_analyzer.predict(text)
                results.append({
                    'index': i,
                    'text': text,
                    'sentiment': result['sentiment'],
                    'confidence': result['confidence'],
                    'emoji': result['emoji'],
                    'color': result['color']
                })
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        })

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """Handle CSV file upload and sentiment analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'Invalid file type, only CSV allowed'}), 400

        # Read the CSV file with better error handling
        try:
            # Try different parsing approaches
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            try:
                file.seek(0)  # Reset file pointer
                df = pd.read_csv(file, encoding='latin-1')
            except Exception as e2:
                return jsonify({'success': False, 'error': f'Error reading CSV file: {str(e2)}. Please ensure your CSV uses UTF-8 or Latin-1 encoding.'}), 400
        except pd.errors.ParserError as e:
            try:
                file.seek(0)  # Reset file pointer
                df = pd.read_csv(file, encoding='utf-8', quoting=3, escapechar='\\')
            except Exception as e2:
                return jsonify({'success': False, 'error': f'CSV parsing error: {str(e)}. Please ensure your CSV is properly formatted with quoted text fields.'}), 400
        except Exception as e:
            return jsonify({'success': False, 'error': f'Error reading CSV file: {str(e)}. Please check your file format.'}), 400
        
        if 'text' not in df.columns:
            return jsonify({'success': False, 'error': 'CSV must contain a "text" column'}), 400

        # Perform sentiment analysis
        results = []
        for text in df['text']:
            if pd.isna(text) or text.strip() == '':
                results.append({
                    'sentiment': 'UNKNOWN',
                    'confidence': 0.0,
                    'emoji': '❓',
                    'color': '#cccccc'
                })
            else:
                result = sentiment_analyzer.predict(str(text))
                results.append(result)

        # Add results to DataFrame
        df['sentiment'] = [r['sentiment'] for r in results]
        df['accuracy'] = [r['confidence'] for r in results]  # Using confidence as accuracy
        df['emoji'] = [r['emoji'] for r in results]
        df['color'] = [r['color'] for r in results]

        # Save to downloadable CSV in-memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)

        # Prepare response
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'sentiment_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': sentiment_analyzer.is_loaded()})

if __name__ == '__main__':
    print("Starting BERT Sentiment Analysis Application...")
    print("Loading BERT model (this may take a moment)...")
    
    # Check if model is loaded successfully
    if sentiment_analyzer.is_loaded():
        print("✓ Model loaded successfully!")
    else:
        print("✗ Failed to load model. Please check your setup.")
    
    # Run the application
    app.run(
        host="0.0.0.0", 
        port=8080, 
        debug=False,  # Set to False for production
        threaded=True
    )
