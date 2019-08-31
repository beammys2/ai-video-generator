# AI Video Generator

A full-stack web application that converts text prompts or image uploads into AI-generated videos. Built with React, FastAPI, and MongoDB.

## 🚀 Features

- **Text-to-Video**: Generate videos from text prompts with multiple style options
- **Image-to-Video**: Upload images and transform them with animation styles
- **Video Gallery**: View and manage all generated videos
- **Mobile-First Design**: Responsive dark mode interface
- **Video Styles**: Realistic, Anime, Cartoon, Surreal, Talking Image, Character Animation, Movement Overlay, Talking Face
- **Duration Control**: Adjustable video length (5-10 seconds)
- **NSFW Content**: Premium feature with payment integration ready
- **Admin Override**: Full access for creators/admins

## 🏗️ Architecture

- **Frontend**: React 19 + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: MongoDB
- **File Storage**: Local uploads directory
- **Authentication**: JWT-based (ready for implementation)
- **Payments**: Stripe integration ready

## 📁 Project Structure

```
ai-video-generator/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── App.js           # Main application component
│   │   ├── App.css          # Tailwind + custom styles
│   │   └── index.js         # React entry point
│   ├── public/              # Static assets
│   ├── package.json         # Frontend dependencies
│   ├── tailwind.config.js   # Tailwind configuration
│   └── .env                 # Frontend environment variables
├── backend/                 # FastAPI backend
│   ├── server.py           # Main FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── uploads/            # File upload directory
│   └── .env               # Backend environment variables
├── tests/                  # Test files
└── README.md              # This file
```

## 🛠️ Local Development Setup

### Prerequisites

- Node.js 16+ and npm/yarn
- Python 3.8+
- MongoDB (local or cloud)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-video-generator.git
cd ai-video-generator
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration:
# MONGO_URL=mongodb://localhost:27017
# DB_NAME=ai_video_generator
# JWT_SECRET=your-secret-key
# STRIPE_SECRET_KEY=sk_test_...
# RUNWAYML_API_KEY=your-key
# STABILITY_API_KEY=your-key

# Start the backend server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in new terminal)
cd frontend

# Install dependencies
yarn install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration:
# REACT_APP_BACKEND_URL=http://localhost:8001
# REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_...

# Start the frontend server
yarn start
```

### 4. Database Setup

The application will automatically create the required MongoDB collections:
- `videos` - Stores video generation data
- `users` - User authentication data (when implemented)
- `status_checks` - System health checks

## 🔧 Hosting Options

### Option 1: Replit

1. Create a new Replit project
2. Upload all project files
3. Set up the following environment variables in Replit:
   - `MONGO_URL`: Your MongoDB connection string
   - `DB_NAME`: Your database name
   - `REACT_APP_BACKEND_URL`: Your Replit backend URL
4. Install dependencies:
   ```bash
   # Backend
   cd backend && pip install -r requirements.txt
   
   # Frontend
   cd frontend && yarn install
   ```
5. Start both servers (Replit can run multiple processes)

### Option 2: Glitch

1. Import GitHub repo to Glitch
2. Set up environment variables in `.env` files
3. Glitch will automatically install dependencies and start the servers

### Option 3: Vercel (Frontend) + Railway/Heroku (Backend)

**Frontend (Vercel):**
1. Connect your GitHub repo to Vercel
2. Set build command: `cd frontend && yarn build`
3. Set build directory: `frontend/build`
4. Add environment variables in Vercel dashboard

**Backend (Railway/Heroku):**
1. Connect your GitHub repo
2. Set root directory to `backend`
3. Add environment variables
4. Deploy with auto-scaling

### Option 4: Docker

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🎯 API Endpoints

### Video Generation
- `POST /api/generate-text-to-video` - Generate video from text
- `POST /api/generate-image-to-video` - Generate video from image
- `GET /api/video/{id}` - Get video by ID
- `GET /api/videos` - Get user's video gallery
- `GET /api/styles` - Get available video styles

### System
- `GET /api/` - Health check
- `POST /api/status` - Create status check
- `GET /api/status` - Get status checks

## 🔐 Environment Variables

### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=ai_video_generator
JWT_SECRET=your-super-secret-jwt-key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
RUNWAYML_API_KEY=your_runwayml_api_key
STABILITY_API_KEY=your_stability_api_key
PIKA_API_KEY=your_pika_api_key
ADMIN_EMAILS=admin@example.com,creator@example.com
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

## 🔮 Future Integrations (Ready to Implement)

### Video Generation APIs
- **RunwayML**: Text-to-video and image-to-video generation
- **Pika Labs**: High-quality video generation
- **Stability AI**: Video diffusion models

### Authentication & Payments
- **JWT Authentication**: User signup, login, logout
- **Stripe Integration**: Premium subscriptions for NSFW content
- **Admin Controls**: Creator whitelist for unlimited access

### Additional Features
- **Video History**: Enhanced gallery with filters
- **Download System**: High-quality video exports
- **Social Sharing**: Direct sharing to social platforms
- **Batch Processing**: Multiple video generation
- **Custom Styles**: User-defined video styles

## 🧪 Testing

Run the test suite:
```bash
# Backend API tests
python backend_test.py

# Frontend tests (when implemented)
cd frontend && yarn test
```

## 📱 Mobile Support

The application is fully responsive and works on:
- Mobile phones (iOS/Android)
- Tablets
- Desktop browsers
- Progressive Web App (PWA) ready

## 🔒 Security Features

- CORS properly configured
- File upload validation
- Input sanitization
- Rate limiting ready
- HTTPS deployment ready

## 🎨 Customization

### Adding New Video Styles
1. Update `SAMPLE_VIDEOS` in `backend/server.py`
2. Add style definitions in `/api/styles` endpoint
3. Update frontend style selectors

### Modifying UI
- Tailwind classes in `frontend/src/App.js`
- Custom styles in `frontend/src/App.css`
- Responsive breakpoints in Tailwind config

## 📊 Monitoring

- Built-in health checks
- Error logging configured
- Performance monitoring ready
- Database connection monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
1. Check the GitHub issues
2. Review the setup documentation
3. Test with the provided examples
4. Contact the development team

## 🔄 Version History

- v1.0.0 - Initial release with stubbed video generation
- v1.1.0 - Real API integration (coming soon)
- v1.2.0 - Authentication & payments (coming soon)

---

**Ready to generate amazing AI videos!** 🎬✨