import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class SentimentAnalyzer:
    def __init__(self, model_name="cardiffnlp/twitter-roberta-base-sentiment-latest"):
        """
        Initialize the sentiment analyzer with a pre-trained model
        
        Args:
            model_name (str): HuggingFace model name
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.labels = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']
        self.emojis = {
            'NEGATIVE': '😞',
            'NEUTRAL': '😐',
            'POSITIVE': '😊'
        }
        self.colors = {
            'NEGATIVE': '#ff4757',
            'NEUTRAL': '#ffa502',
            'POSITIVE': '#2ed573'
        }
        
        # Load model on initialization
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained model and tokenizer"""
        try:
            print(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to a different model
            try:
                print("Trying fallback model: nlptown/bert-base-multilingual-uncased-sentiment")
                self.model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
                self.model.to(self.device)
                self.model.eval()
                # This model has 5 classes (1-5 stars), we'll map them to 3 classes
                self.labels = ['VERY_NEGATIVE', 'NEGATIVE', 'NEUTRAL', 'POSITIVE', 'VERY_POSITIVE']
                print("Fallback model loaded successfully")
            except Exception as e2:
                print(f"Error loading fallback model: {e2}")
                raise Exception("Failed to load any sentiment analysis model")
    
    def _preprocess_text(self, text):
        """Preprocess text for sentiment analysis"""
        # Clean and normalize text
        text = text.strip()
        # Remove excessive whitespace
        text = ' '.join(text.split())
        return text
    
    def _map_sentiment(self, predicted_class, confidence):
        """Map model output to sentiment labels"""
        if self.model_name == "nlptown/bert-base-multilingual-uncased-sentiment":
            # Map 5-class sentiment to 3-class
            if predicted_class in [0, 1]:  # 1-2 stars
                return 'NEGATIVE'
            elif predicted_class == 2:  # 3 stars
                return 'NEUTRAL'
            else:  # 4-5 stars
                return 'POSITIVE'
        else:
            # Direct mapping for 3-class models
            return self.labels[predicted_class]
    
    def predict(self, text):
        """
        Predict sentiment for given text
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Prediction results with sentiment, confidence, emoji, and color
        """
        if not self.model or not self.tokenizer:
            raise Exception("Model not loaded properly")
        
        # Preprocess text
        processed_text = self._preprocess_text(text)
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                processed_text, 
                return_tensors="pt", 
                truncation=True, 
                padding=True, 
                max_length=512
            )
            
            # Move inputs to device
            inputs = {key: value.to(self.device) for key, value in inputs.items()}
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
                # Get predicted class and confidence
                predicted_class = torch.argmax(predictions, dim=-1).item()
                confidence = torch.max(predictions, dim=-1)[0].item()
                
                # Map to sentiment
                sentiment = self._map_sentiment(predicted_class, confidence)
                
                return {
                    'sentiment': sentiment,
                    'confidence': round(confidence * 100, 2),
                    'emoji': self.emojis.get(sentiment, '🤔'),
                    'color': self.colors.get(sentiment, '#74b9ff'),
                    'raw_scores': predictions.cpu().numpy().tolist()[0]
                }
        
        except Exception as e:
            print(f"Error during prediction: {e}")
            return {
                'sentiment': 'NEUTRAL',
                'confidence': 0.0,
                'emoji': '🤔',
                'color': '#74b9ff',
                'error': str(e)
            }
    
    def predict_batch(self, texts):
        """
        Predict sentiment for multiple texts
        
        Args:
            texts (list): List of texts to analyze
            
        Returns:
            list: List of prediction results
        """
        results = []
        for text in texts:
            result = self.predict(text)
            results.append(result)
        return results
    
    def is_loaded(self):
        """Check if model is loaded"""
        return self.model is not None and self.tokenizer is not None

# Example usage
if __name__ == "__main__":
    # Test the sentiment analyzer
    analyzer = SentimentAnalyzer()
    
    test_texts = [
        "I absolutely love this movie!",
        "This is terrible and I hate it.",
        "It's okay, nothing special.",
        "The weather is nice today.",
        "I'm so excited about the new project!"
    ]
    
    print("Testing Sentiment Analyzer:")
    print("-" * 50)
    
    for text in test_texts:
        result = analyzer.predict(text)
        print(f"Text: {text}")
        print(f"Sentiment: {result['sentiment']} {result['emoji']}")
        print(f"Confidence: {result['confidence']}%")
        print("-" * 50)