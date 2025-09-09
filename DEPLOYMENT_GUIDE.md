# Enhanced Business Card Editor - Deployment Guide

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd enhanced_business_card_editor

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run enhanced_main_app.py
```

### 2. Access the Application

Once running, open your browser to:
- **Local**: http://localhost:8501
- **Network**: Available on your local network

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

### Recommended Requirements
- **Python**: 3.11+
- **RAM**: 16GB for optimal performance
- **Storage**: 10GB for image library
- **GPU**: Optional, for faster image processing

## 🔧 Dependencies

### Core Dependencies
```
streamlit>=1.28.0          # Web framework
Pillow>=10.0.0            # Image processing
numpy>=1.24.0             # Numerical computing
opencv-python>=4.8.0      # Computer vision
scikit-learn>=1.3.0       # Machine learning
scipy>=1.11.0             # Scientific computing
```

### Optional Dependencies
```
pandas>=2.0.0             # Data manipulation
matplotlib>=3.7.0         # Plotting
plotly>=5.15.0           # Interactive plots
requests>=2.31.0          # HTTP requests
```

## 🏗️ Project Structure

```
enhanced_business_card_editor/
├── enhanced_main_app.py          # Main application
├── test_app.py                   # Test version
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── DEPLOYMENT_GUIDE.md          # This file
├── components/                   # Core components
│   ├── __init__.py
│   ├── ui_components.py         # UI components
│   ├── image_library.py         # Image management
│   └── magic_eraser.py          # Advanced editing
├── utils/                       # Utilities
│   ├── __init__.py
│   ├── canvas_sizes.py          # Canvas management
│   └── image_processing.py      # Image processing
├── static/                      # Static assets
│   └── css/
│       └── photoshop_theme.css  # Styling
└── assets/                      # Runtime assets
    ├── images/                  # Image library
    └── projects/                # Saved projects
```

## 🐳 Docker Deployment

### Build Docker Image

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p assets/images assets/projects

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "enhanced_main_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t enhanced-business-card-editor .

# Run container
docker run -p 8501:8501 -v $(pwd)/assets:/app/assets enhanced-business-card-editor

# Run with docker-compose
docker-compose up -d
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./assets:/app/assets
      - ./projects:/app/projects
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_ENABLE_CORS=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## ☁️ Cloud Deployment

### Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Enhanced Business Card Editor"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `enhanced_main_app.py` as main file
   - Deploy automatically

### Heroku Deployment

1. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

2. **Add Buildpacks**
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt
   ```

3. **Create Aptfile**
   ```
   libgl1-mesa-glx
   libglib2.0-0
   ```

4. **Create Procfile**
   ```
   web: streamlit run enhanced_main_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t3.medium or larger
   - Security group: Allow port 8501

2. **Setup Application**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and dependencies
   sudo apt install python3-pip python3-venv -y
   
   # Clone application
   git clone <your-repo-url>
   cd enhanced_business_card_editor
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run application
   streamlit run enhanced_main_app.py --server.port=8501 --server.address=0.0.0.0
   ```

3. **Setup as Service**
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/business-card-editor.service
   ```

   ```ini
   [Unit]
   Description=Enhanced Business Card Editor
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/enhanced_business_card_editor
   Environment=PATH=/home/ubuntu/enhanced_business_card_editor/venv/bin
   ExecStart=/home/ubuntu/enhanced_business_card_editor/venv/bin/streamlit run enhanced_main_app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   # Enable and start service
   sudo systemctl enable business-card-editor
   sudo systemctl start business-card-editor
   ```

## 🔒 Security Configuration

### Production Settings

```python
# .streamlit/config.toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
base = "dark"
```

### Environment Variables

```bash
# .env
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 📊 Performance Optimization

### Memory Management

```python
# Optimize Streamlit caching
@st.cache_data(max_entries=100)
def load_image(path):
    return Image.open(path)

@st.cache_resource
def get_image_processor():
    return ImageProcessor()
```

### Image Processing

```python
# Optimize image sizes
MAX_IMAGE_SIZE = (2048, 2048)
THUMBNAIL_SIZE = (256, 256)

# Use efficient formats
PREFERRED_FORMAT = "WEBP"
QUALITY_SETTINGS = {"PNG": 9, "JPEG": 85, "WEBP": 80}
```

## 🔍 Monitoring & Logging

### Application Monitoring

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks

```python
# Health check endpoint
def health_check():
    try:
        # Test database connection
        library = ImageLibrary()
        
        # Test image processing
        processor = ImageProcessor()
        
        return {"status": "healthy", "timestamp": datetime.now()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install --force-reinstall -r requirements.txt
   ```

2. **Memory Issues**
   ```bash
   # Increase swap space
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

3. **Port Issues**
   ```bash
   # Check port usage
   netstat -tlnp | grep :8501
   
   # Kill process
   sudo kill -9 <PID>
   ```

4. **Permission Issues**
   ```bash
   # Fix permissions
   chmod +x enhanced_main_app.py
   chown -R $USER:$USER .
   ```

### Debug Mode

```bash
# Run in debug mode
streamlit run enhanced_main_app.py --logger.level=debug
```

### Performance Profiling

```python
# Add profiling
import cProfile
import pstats

def profile_function(func):
    pr = cProfile.Profile()
    pr.enable()
    result = func()
    pr.disable()
    
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    return result
```

## 📈 Scaling

### Horizontal Scaling

```yaml
# kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: business-card-editor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: business-card-editor
  template:
    metadata:
      labels:
        app: business-card-editor
    spec:
      containers:
      - name: app
        image: enhanced-business-card-editor:latest
        ports:
        - containerPort: 8501
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

### Load Balancing

```nginx
# nginx.conf
upstream streamlit_backend {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://streamlit_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔄 Updates & Maintenance

### Update Process

```bash
# Backup current version
cp -r enhanced_business_card_editor enhanced_business_card_editor_backup

# Pull updates
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart application
sudo systemctl restart business-card-editor
```

### Database Maintenance

```python
# Image library maintenance
def cleanup_library():
    library = ImageLibrary()
    library.cleanup_orphaned_files()
    library.optimize_database()
    library.generate_missing_thumbnails()
```

## 📞 Support

### Getting Help

- **Documentation**: Check README.md and inline comments
- **Issues**: Create GitHub issues for bugs
- **Community**: Join discussions for feature requests
- **Email**: Contact support for enterprise needs

### Reporting Issues

When reporting issues, include:
1. Python version
2. Operating system
3. Error messages
4. Steps to reproduce
5. Expected vs actual behavior

---

**Enhanced Business Card Editor v2.0**  
*Professional Design Tool with Advanced Features*

