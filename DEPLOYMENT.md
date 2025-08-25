# 🚀 Deployment Guide

This guide covers deploying your Stock/ETF Dashboard to various platforms.

## 📋 **Prerequisites**

- ✅ **GitHub repository** with your code
- ✅ **Environment variables** configured
- ✅ **Dependencies** working locally
- ✅ **Streamlit app** running without errors

## 🌐 **Streamlit Cloud (Recommended)**

### **Step 1: Prepare Your Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### **Step 2: Deploy to Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app/main.py`
6. Click "Deploy!"

### **Step 3: Configure Environment Variables**
1. In your app settings, go to "Secrets"
2. Add your environment variables:
```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_ANON_KEY = "your-supabase-anon-key"
ALPHA_VANTAGE_API_KEY = "your-key"
IEX_CLOUD_API_KEY = "your-key"
YAHOO_FINANCE_CACHE_TTL = "300"
MAX_CACHE_SIZE = "1000"
CACHE_EXPIRY = "3600"
```

### **Step 4: Access Your App**
- **Public URL**: `https://your-app-name.streamlit.app`
- **Custom Domain**: Available on paid plans

## 🐳 **Docker Deployment**

### **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### **Build and Run**
```bash
# Build image
docker build -t stock-dashboard .

# Run container
docker run -p 8501:8501 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_ANON_KEY=your-key \
  stock-dashboard
```

### **Docker Compose**
```yaml
version: '3.8'
services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
    restart: unless-stopped
```

## ☁️ **Cloud Platforms**

### **Heroku**
```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set SUPABASE_URL=your-url
heroku config:set SUPABASE_ANON_KEY=your-key
git push heroku main
```

### **Railway**
1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

### **Render**
1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0`

## 🖥️ **VPS/Server Deployment**

### **System Requirements**
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: 2GB+ (4GB recommended)
- **Storage**: 10GB+ available space
- **Python**: 3.9+

### **Installation Steps**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/stock-dashboard.service
```

### **Systemd Service File**
```ini
[Unit]
Description=Stock Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/stock-dashboard
Environment=PATH=/home/ubuntu/stock-dashboard/venv/bin
ExecStart=/home/ubuntu/stock-dashboard/venv/bin/streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

### **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 **Security Considerations**

### **Environment Variables**
- ✅ **Never commit** `.env` files
- ✅ **Use secrets management** in production
- ✅ **Rotate API keys** regularly
- ✅ **Limit API access** to necessary endpoints

### **Network Security**
- 🔒 **HTTPS only** in production
- 🔒 **Firewall rules** to limit access
- 🔒 **Rate limiting** to prevent abuse
- 🔒 **CORS configuration** if needed

### **Monitoring**
- 📊 **Health checks** for uptime monitoring
- 📊 **Log aggregation** for debugging
- 📊 **Performance metrics** for optimization
- 📊 **Error tracking** for issue resolution

## 📊 **Performance Optimization**

### **Caching Strategy**
```python
# In config.py
YAHOO_FINANCE_CACHE_TTL = 300  # 5 minutes
MAX_CACHE_SIZE = 1000
CACHE_EXPIRY = 3600  # 1 hour
```

### **Database Optimization**
- **Indexes** on frequently queried fields
- **Connection pooling** for database connections
- **Query optimization** for complex operations

### **CDN Configuration**
- **Static assets** served from CDN
- **Image optimization** for charts
- **Compression** enabled

## 🚨 **Troubleshooting**

### **Common Issues**

#### **App Won't Start**
```bash
# Check logs
streamlit run app/main.py --server.port=8501 --logger.level=debug

# Check dependencies
pip list | grep streamlit
```

#### **Environment Variables Not Loading**
```bash
# Verify .env file exists
ls -la .env

# Check variable loading
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('SUPABASE_URL'))"
```

#### **Port Already in Use**
```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>
```

### **Support Resources**
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub Issues**: Create issue in your repository
- **Community**: [discuss.streamlit.io](https://discuss.streamlit.io)

## 📈 **Scaling Considerations**

### **Horizontal Scaling**
- **Load balancer** for multiple instances
- **Session management** across instances
- **Database clustering** for high availability

### **Vertical Scaling**
- **Resource monitoring** and alerts
- **Auto-scaling** based on demand
- **Performance profiling** and optimization

---

**Happy Deploying! 🚀**
