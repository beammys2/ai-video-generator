# Deployment Guide

This document provides detailed instructions for deploying the AI Video Generator to various platforms.

## 🚀 Quick Deploy Options

### Vercel (Frontend) + Railway (Backend)

**1. Deploy Backend to Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add
railway deploy
```

**2. Deploy Frontend to Vercel:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

### Heroku (Full Stack)

**1. Prepare for Heroku:**
```bash
# Create Procfile
echo "web: cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT" > Procfile
echo "worker: cd frontend && npm start" >> Procfile
```

**2. Deploy:**
```bash
heroku create your-app-name
heroku addons:create mongolab:sandbox
heroku config:set MONGO_URL=your-mongodb-url
git push heroku main
```

### Docker Deployment

**1. Create Docker Compose:**
```yaml
version: '3.8'
services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://mongo:27017
      - DB_NAME=ai_video_generator
    depends_on:
      - mongo
    
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8001
    depends_on:
      - backend
    
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

**2. Deploy:**
```bash
docker-compose up --build -d
```

## 🛠️ Platform-Specific Instructions

### Replit

1. **Create New Replit:**
   - Import from GitHub
   - Select "Full Stack" template

2. **Configuration:**
   ```bash
   # In .replit file
   run = "cd backend && python server.py & cd frontend && npm start"
   
   # Install dependencies
   cd backend && pip install -r requirements.txt
   cd frontend && npm install
   ```

3. **Environment Variables:**
   - Add all required variables in Replit Secrets
   - Use Replit's database if needed

### Glitch

1. **Import Project:**
   - Go to glitch.com
   - Select "Import from GitHub"
   - Enter your repository URL

2. **Setup Scripts:**
   ```json
   // In package.json
   {
     "scripts": {
       "start": "cd backend && python server.py & cd frontend && npm start"
     }
   }
   ```

### DigitalOcean App Platform

1. **App Spec Configuration:**
```yaml
name: ai-video-generator
services:
- name: backend
  github:
    repo: your-username/ai-video-generator
    branch: main
  source_dir: /backend
  run_command: uvicorn server:app --host 0.0.0.0 --port $PORT
  
- name: frontend
  github:
    repo: your-username/ai-video-generator
    branch: main
  source_dir: /frontend
  build_command: npm run build
  run_command: npm start
```

### AWS Deployment

**1. Elastic Beanstalk:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init
eb create production
eb deploy
```

**2. Lambda + API Gateway (Serverless):**
```bash
# Install Serverless Framework
npm install -g serverless

# Deploy
serverless deploy
```

## 🔧 Environment Configuration

### Production Environment Variables

**Backend:**
```env
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/
DB_NAME=ai_video_generator_prod
JWT_SECRET=super-secure-production-secret
STRIPE_SECRET_KEY=sk_live_...
RUNWAYML_API_KEY=prod_api_key
STABILITY_API_KEY=prod_api_key
ADMIN_EMAILS=admin@yourdomain.com
ALLOWED_ORIGINS=https://yourdomain.com
NODE_ENV=production
DEBUG=false
```

**Frontend:**
```env
REACT_APP_BACKEND_URL=https://api.yourdomain.com
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_live_...
REACT_APP_ENV=production
REACT_APP_DEBUG=false
```

## 🔒 Security Checklist

- [ ] Change all default passwords and secrets
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable database authentication
- [ ] Use environment variables for sensitive data
- [ ] Set up monitoring and logging
- [ ] Configure firewall rules
- [ ] Enable backup systems
- [ ] Set up error tracking (Sentry)

## 📊 Monitoring Setup

### Health Checks
```bash
# Backend health check
curl https://api.yourdomain.com/api/

# Frontend health check
curl https://yourdomain.com/
```

### Logging Configuration
```python
# In server.py
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 🚨 Troubleshooting

### Common Issues

**1. CORS Errors:**
```python
# In server.py - Update CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**2. MongoDB Connection Issues:**
```python
# Check connection string format
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/database
```

**3. File Upload Problems:**
```python
# Ensure uploads directory exists
os.makedirs('uploads', exist_ok=True)
```

**4. Environment Variables Not Loading:**
```bash
# Check .env file location and format
# Ensure no spaces around = signs
# Wrap values with quotes if they contain spaces
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v20
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.ORG_ID }}
        vercel-project-id: ${{ secrets.PROJECT_ID }}
        working-directory: ./frontend
```

## 📱 Mobile App Deployment

### PWA Configuration
```json
// In public/manifest.json
{
  "name": "AI Video Generator",
  "short_name": "VideoGen",
  "start_url": "/",
  "background_color": "#111827",
  "theme_color": "#8b5cf6",
  "display": "standalone"
}
```

### App Store Deployment
- Use Capacitor to build native apps
- Follow platform-specific guidelines
- Implement in-app purchases for premium features

## 🔧 Performance Optimization

### Backend Optimization
```python
# Add caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Add database indexing
await db.videos.create_index("user_id")
await db.videos.create_index("created_at")
```

### Frontend Optimization
```javascript
// Code splitting
const VideoGallery = lazy(() => import('./VideoGallery'));

// Image optimization
const optimizedImage = `${imageUrl}?w=400&h=300&fit=crop`;
```

---

**Need help with deployment? Check the GitHub issues or contact support!** 🚀