# Setup Instructions

Complete guide to set up the AI Video Generator locally or on cloud platforms.

## 🎯 Quick Start (5 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-video-generator.git
cd ai-video-generator

# 2. Backend setup
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
uvicorn server:app --host 0.0.0.0 --port 8001 --reload &

# 3. Frontend setup
cd ../frontend
yarn install
cp .env.example .env
# Edit .env with your settings
yarn start

# 4. Open http://localhost:3000
```

## 🔧 Detailed Setup

### Prerequisites

**Required:**
- Python 3.8+ (`python --version`)
- Node.js 16+ (`node --version`)
- MongoDB (local or cloud)

**Optional:**
- Git (`git --version`)
- Docker (`docker --version`)
- Yarn (`yarn --version`)

### Step 1: Environment Setup

**Option A: Local MongoDB**
```bash
# Install MongoDB locally
# macOS
brew install mongodb/brew/mongodb-community
brew services start mongodb/brew/mongodb-community

# Ubuntu
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb

# Windows
# Download from https://www.mongodb.com/try/download/community
```

**Option B: MongoDB Atlas (Cloud)**
```bash
# Create account at https://cloud.mongodb.com
# Create cluster and get connection string
# Format: mongodb+srv://username:password@cluster.mongodb.net/database
```

### Step 2: Backend Configuration

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env file with your settings:
nano .env  # or vim .env or code .env
```

**Backend .env Configuration:**
```env
# Required
MONGO_URL=mongodb://localhost:27017
DB_NAME=ai_video_generator

# Optional (for future features)
JWT_SECRET=your-secret-key-here
STRIPE_SECRET_KEY=sk_test_...
RUNWAYML_API_KEY=your-key-here
```

### Step 3: Frontend Configuration

```bash
cd ../frontend

# Install dependencies
yarn install
# or: npm install

# Create environment file
cp .env.example .env

# Edit .env file:
nano .env
```

**Frontend .env Configuration:**
```env
# Required
REACT_APP_BACKEND_URL=http://localhost:8001

# Optional (for future features)
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### Step 4: Start the Application

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # Skip if already activated
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
yarn start
```

**Access the Application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

## 🔍 Verification

### 1. Backend Health Check
```bash
curl http://localhost:8001/api/
# Expected: {"message": "Hello World"}
```

### 2. Database Connection
```bash
curl http://localhost:8001/api/styles
# Expected: JSON with video styles
```

### 3. Frontend Loading
- Open http://localhost:3000
- Should see the AI Video Generator interface
- Try switching between Text-to-Video and Image-to-Video tabs

### 4. Full Flow Test
1. Enter a text prompt: "A cat playing with a ball"
2. Select style: "Realistic"
3. Click "Generate Video"
4. Wait 3 seconds for completion
5. Video should appear in preview panel
6. Click "Show Gallery" to see the generated video

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill process on port 8001
lsof -ti:8001 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different ports
uvicorn server:app --host 0.0.0.0 --port 8002 --reload
```

**2. MongoDB Connection Error**
```bash
# Check MongoDB is running
mongosh  # Should connect successfully

# Check connection string in .env
MONGO_URL=mongodb://localhost:27017  # No trailing slash
```

**3. Python Dependencies Error**
```bash
# Upgrade pip
pip install --upgrade pip

# Install specific versions
pip install -r requirements.txt --no-cache-dir

# Check Python version
python --version  # Should be 3.8+
```

**4. Node Dependencies Error**
```bash
# Clear cache
yarn cache clean

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
yarn install

# Check Node version
node --version  # Should be 16+
```

**5. CORS Errors**
```bash
# Check backend .env
ALLOWED_ORIGINS=http://localhost:3000

# Or allow all origins (development only)
ALLOWED_ORIGINS=*
```

**6. File Upload Issues**
```bash
# Check uploads directory exists
mkdir -p backend/uploads
chmod 755 backend/uploads
```

### Debug Mode

**Enable Backend Debug:**
```bash
# In backend/.env
DEBUG=true

# Run with debug
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

**Enable Frontend Debug:**
```bash
# In frontend/.env
REACT_APP_DEBUG=true

# Check browser console for logs
```

### Log Files

**Backend Logs:**
```bash
# View real-time logs
tail -f backend/app.log

# View error logs
grep ERROR backend/app.log
```

**Frontend Logs:**
- Open browser developer tools (F12)
- Check Console tab for errors
- Check Network tab for API calls

## 🚀 Platform-Specific Setup

### Replit Setup

1. **Import Project:**
   - Go to replit.com
   - Click "Import from GitHub"
   - Enter repository URL

2. **Configuration:**
   ```bash
   # Create .replit file
   echo 'run = "cd backend && python server.py & cd frontend && npm start"' > .replit
   
   # Set up environment
   # Use Replit's Secret Environment Variables for sensitive data
   ```

3. **Install Dependencies:**
   ```bash
   cd backend && pip install -r requirements.txt
   cd frontend && npm install
   ```

### Glitch Setup

1. **Import Project:**
   - Go to glitch.com
   - Click "Import from GitHub"
   - Enter repository URL

2. **Configuration:**
   ```json
   // In package.json (root)
   {
     "scripts": {
       "start": "cd backend && python server.py & cd frontend && npm start"
     }
   }
   ```

### CodeSandbox Setup

1. **Import Project:**
   - Go to codesandbox.io
   - Click "Import from GitHub"
   - Enter repository URL

2. **Configuration:**
   - CodeSandbox will auto-detect the setup
   - Set environment variables in Settings

### Gitpod Setup

1. **Open in Gitpod:**
   - Prefix GitHub URL with `gitpod.io/#/`
   - Example: `gitpod.io/#/https://github.com/username/ai-video-generator`

2. **Automatic Setup:**
   - Create `.gitpod.yml`:
   ```yaml
   tasks:
     - name: Backend
       command: cd backend && pip install -r requirements.txt && uvicorn server:app --host 0.0.0.0 --port 8001
     - name: Frontend
       command: cd frontend && yarn install && yarn start
   
   ports:
     - port: 8001
       onOpen: ignore
     - port: 3000
       onOpen: open-preview
   ```

## 🔒 Security Setup

### Development Security

```bash
# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set secure permissions on .env files
chmod 600 backend/.env frontend/.env

# Never commit .env files
echo ".env" >> .gitignore
```

### Production Security

```bash
# Use strong secrets
JWT_SECRET=$(openssl rand -base64 32)
STRIPE_WEBHOOK_SECRET=whsec_...

# Enable HTTPS
HTTPS=true

# Restrict CORS
ALLOWED_ORIGINS=https://yourdomain.com
```

## 📊 Performance Tuning

### Backend Optimization

```python
# In server.py
# Add connection pooling
client = AsyncIOMotorClient(mongo_url, maxPoolSize=20)

# Add response caching
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
```

### Frontend Optimization

```javascript
// In App.js
// Lazy loading
const VideoGallery = React.lazy(() => import('./VideoGallery'));

// Memoization
const VideoCard = React.memo(({ video }) => {
  // Component code
});
```

### Database Optimization

```javascript
// Create indexes for better performance
db.videos.createIndex({ "user_id": 1 })
db.videos.createIndex({ "created_at": -1 })
db.videos.createIndex({ "status": 1 })
```

## 📱 Mobile Testing

### Local Mobile Testing

```bash
# Find your local IP
ipconfig getifaddr en0  # macOS
hostname -I  # Linux
ipconfig  # Windows

# Update frontend .env
REACT_APP_BACKEND_URL=http://YOUR_LOCAL_IP:8001

# Access from mobile
# Open http://YOUR_LOCAL_IP:3000 on mobile browser
```

### Mobile Debugging

```javascript
// Enable mobile debugging
// Add to App.js for development
if (process.env.REACT_APP_DEBUG) {
  console.log('Mobile debugging enabled');
}
```

---

**Still having issues? Check our [GitHub Issues](https://github.com/yourusername/ai-video-generator/issues) or create a new one!** 🆘