# BERT Sentiment Analysis App 🧠

A production-ready sentiment analysis application powered by BERT (Bidirectional Encoder Representations from Transformers) that provides real-time sentiment analysis through a modern web interface.

## Features ✨

- **Real-time Sentiment Analysis**: Analyze text sentiment using pre-trained BERT models
- **Batch Processing**: Analyze multiple texts simultaneously
- **CSV Upload**: Upload CSV files for bulk sentiment analysis
- **Interactive Web Interface**: Modern, responsive UI with real-time feedback
- **REST API**: JSON API endpoints for programmatic access
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **Kubernetes Ready**: Production-ready Kubernetes deployment configurations
- **Health Monitoring**: Built-in health checks and monitoring endpoints

## Technology Stack 🔧

- **Backend**: Python 3.10, Flask
- **ML Models**: HuggingFace Transformers (BERT, RoBERTa)
- **Frontend**: HTML5, JavaScript, Bootstrap 5
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes
- **Data Processing**: Pandas, NumPy
- **HTTP Client**: Requests

## Quick Start 🚀

### Prerequisites

1. **Docker Desktop** - Install from [docker.com](https://www.docker.com/products/docker-desktop/)
2. **Python 3.10+** (optional, for local development)
3. **Git** (optional, for version control)

### Option 1: Docker (Recommended)

1. **Start Docker Desktop** (ensure it's running)

2. **Clone or download the project**

3. **Build the Docker image**:
   ```bash
   # On Windows
   .\build.bat
   
   # On Linux/macOS
   ./build.sh
   
   # Manual build
   docker build -t bert-sentiment-app:latest .
   ```

4. **Run the container**:
   ```bash
   docker run -p 5000:5000 bert-sentiment-app:latest
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:5000`

### Option 2: Docker Compose

1. **Start the application**:
   ```bash
   docker-compose up
   ```

2. **Access the application**:
   Open your browser and go to `http://localhost:5000`

### Option 3: Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## Docker Commands 🐳

### Build Image
```bash
docker build -t bert-sentiment-app:latest .
```

### Run Container
```bash
# Basic run
docker run -p 5000:5000 bert-sentiment-app:latest

# Run with volume for model caching
docker run -p 5000:5000 -v model_cache:/app/model_cache bert-sentiment-app:latest

# Run in background
docker run -d -p 5000:5000 --name sentiment-app bert-sentiment-app:latest
```

### Docker Compose
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Useful Docker Commands
```bash
# List running containers
docker ps

# View container logs
docker logs <container_id>

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# Remove image
docker rmi bert-sentiment-app:latest
```

## Kubernetes Deployment ☸️

### Deploy to Kubernetes

1. **Apply the deployment**:
   ```bash
   kubectl apply -f deployment.yaml
   ```

2. **Check deployment status**:
   ```bash
   kubectl get pods
   kubectl get services
   ```

3. **Access the application**:
   ```bash
   # Port forward to local machine
   kubectl port-forward service/bert-sentiment-app-service 5000:80
   
   # Or access via NodePort (if available)
   # Application will be available at: http://<node-ip>:30007
   ```

### Kubernetes Management Commands
```bash
# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/bert-sentiment-app-deployment

# Scale deployment
kubectl scale deployment bert-sentiment-app-deployment --replicas=3

# Delete deployment
kubectl delete -f deployment.yaml
```

## API Endpoints 🔌

### Health Check
```bash
GET /health
```

### Single Text Analysis
```bash
POST /analyze
Content-Type: application/json

{
  "text": "I love this product!"
}
```

### Batch Analysis
```bash
POST /analyze_batch
Content-Type: application/json

{
  "texts": ["I love this!", "This is terrible", "It's okay"]
}
```

### CSV Upload
```bash
POST /upload_csv
Content-Type: multipart/form-data

file: <csv_file>
```

## Configuration ⚙️

### Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `FLASK_DEBUG`: Set to `false` for production
- `TRANSFORMERS_CACHE`: Directory for caching downloaded models

### Model Configuration

The application uses the following models by default:
- Primary: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- Fallback: `nlptown/bert-base-multilingual-uncased-sentiment`

To use a different model, modify the `model_name` parameter in `model_utils.py`.

## Troubleshooting 🔧

### Common Issues

1. **Docker not starting**:
   - Ensure Docker Desktop is installed and running
   - Check Docker service status: `docker --version`

2. **Port already in use**:
   - Use a different port: `docker run -p 5001:5000 bert-sentiment-app:latest`

3. **Model download issues**:
   - Ensure internet connectivity
   - Check firewall/proxy settings
   - Models are cached after first download

4. **Memory issues**:
   - Increase Docker memory limit in Docker Desktop settings
   - Reduce batch size for large datasets

### Docker Desktop Issues

1. **Start Docker Desktop**:
   - Windows: Start Docker Desktop from Start menu
   - macOS: Start Docker Desktop from Applications
   - Linux: Start Docker daemon

2. **Check Docker Status**:
   ```bash
   docker info
   ```

3. **Reset Docker** (if needed):
   - Go to Docker Desktop settings
   - Click "Reset to factory defaults"

## Development 👨‍💻

### Project Structure
```
├── app.py                 # Main Flask application
├── model_utils.py         # BERT model utilities
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── deployment.yaml       # Kubernetes deployment
├── service.yaml          # Kubernetes service
├── templates/
│   └── index.html        # Web interface
├── build.sh              # Linux/macOS build script
├── build.bat             # Windows build script
└── README.md             # This file
```

### Adding New Models

1. Modify `model_utils.py`
2. Update the `model_name` parameter
3. Test locally before building Docker image

### Custom Modifications

1. **UI Changes**: Edit `templates/index.html`
2. **API Changes**: Modify `app.py`
3. **Model Changes**: Update `model_utils.py`

## Performance Optimization 🚀

### Model Caching
- Models are cached after first download
- Use Docker volumes for persistent caching
- Pre-download models in Docker build (optional)

### Production Deployment
- Use multiple replicas in Kubernetes
- Configure resource limits
- Enable horizontal pod autoscaling
- Use load balancers for high availability

## Security Considerations 🔒

- Application runs as non-root user in container
- No sensitive data in environment variables
- Input validation for all user inputs
- HTTPS recommended for production deployment

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License 📝

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

For issues and questions:
1. Check the troubleshooting section
2. Review Docker and Kubernetes documentation
3. Check application logs for error details

---

**Happy analyzing! 🎉**

# Sentiment Analysis App with CSV Upload

This is a Flask-based sentiment analysis application that uses a pre-trained BERT model to analyze text sentiment. The app now supports three different modes of analysis:

## Features

1. **Single Text Analysis** - Analyze individual text snippets
2. **Batch Analysis** - Analyze multiple texts at once (up to 10 texts)
3. **CSV Upload** - Upload CSV files for bulk sentiment analysis

## CSV Upload Feature

The CSV upload feature allows you to:
- Upload CSV files containing text data
- Automatically analyze sentiment for all texts
- Download results as a CSV file with additional columns:
  - `text` - Original text
  - `sentiment` - Detected sentiment (POSITIVE, NEGATIVE, NEUTRAL)
  - `accuracy` - Confidence score (0-100%)
  - `emoji` - Emoji representation of sentiment
  - `color` - Color code for sentiment visualization

### CSV Format Requirements

Your CSV file must contain a column named `text` with the text data you want to analyze.

Example CSV format:
```csv
text
I love this product!
This service is terrible.
It's okay, nothing special.
```

### How to Use

1. Click on the "CSV Upload" tab
2. Select your CSV file using the file picker
3. Click "Upload and Analyze"
4. Wait for processing to complete
5. Your results will automatically download as a CSV file

### Sample File

A sample CSV file (`sample_texts.csv`) is included in the project directory for testing purposes.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and go to `http://localhost:5000`

## API Endpoints

- `POST /analyze` - Single text analysis
- `POST /analyze_batch` - Batch text analysis
- `POST /upload_csv` - CSV file upload and analysis
- `GET /health` - Health check

## Model Information

The app uses a pre-trained BERT model for sentiment analysis:
- Primary model: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- Fallback model: `nlptown/bert-base-multilingual-uncased-sentiment`

## Output Format

The CSV output includes:
- All original columns from your input CSV
- `sentiment` - POSITIVE, NEGATIVE, or NEUTRAL
- `accuracy` - Confidence percentage
- `emoji` - 😊 (positive), 😞 (negative), 😐 (neutral)
- `color` - Hex color code for visualization
