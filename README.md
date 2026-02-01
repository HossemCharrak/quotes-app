# Quotes App 📚✨

A full-stack application for discovering and sharing inspirational quotes with intelligent, ML-powered recommendations. Built with FastAPI backend and React frontend, featuring a smart recommendation system based on collaborative filtering.

## 🌟 Overview

This application combines a robust RESTful API with a modern, responsive frontend to deliver a seamless quote-browsing experience. Users can explore thousands of curated quotes, like their favorites, and receive personalized recommendations powered by association rule mining algorithms.

## ✨ Key Features

- **🤖 Smart Recommendations**: ML-powered quote suggestions using Apriori algorithm
- **❤️ Interactive Like System**: Track favorites and improve recommendations
- **📚 Extensive Library**: 3,003+ carefully curated quotes from renowned authors
- **➕ Community Contributions**: Add your own quotes with author attribution
- **👥 Multi-user Support**: Personalized experiences for each user
- **🎨 Modern UI**: Beautiful, responsive design with Tailwind CSS
- **⚡ High Performance**: FastAPI backend with real-time updates
- **🏷️ Smart Categorization**: Organized by tags (inspirational, philosophy, love, etc.)

## 🏗️ Project Structure

```
quotes-app/
├── quotes-api/           # FastAPI backend
│   ├── quotes-api.py     # Main API application
│   ├── requirements.txt  # Python dependencies
│   └── db/
│       ├── data/         # CSV data files
│       └── scripts/      # Database utilities
│
└── quotes-frontend/      # React + Vite frontend
    ├── src/
    │   ├── components/   # React components
    │   ├── pages/        # Page components
    │   └── lib/          # Utilities
    ├── package.json      # Node dependencies
    └── vite.config.js    # Vite configuration
```

## 🛠️ Tech Stack

### Backend

- **FastAPI** - Modern, high-performance web framework
- **SQLite** - Lightweight embedded database
- **Pandas** - Data manipulation and analysis
- **mlxtend** - Association rule mining for recommendations
- **scikit-learn** - Machine learning utilities
- **Pydantic** - Data validation

### Frontend

- **React 18** - Modern React with hooks
- **Vite** - Next-generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality UI components
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Lucide React** - Icon library

## 📋 Prerequisites

- **Python 3.8+** and pip
- **Node.js 16+** and npm/yarn
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/HossemCharrak/quotes-app.git
cd quotes-app
```

### 2. Backend Setup

```bash
cd quotes-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python db/scripts/init_db.py

# Start the API server
uvicorn quotes-api:app --reload
```

The API will be available at `http://127.0.0.1:8000`

- API Documentation: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup

Open a new terminal:

```bash
cd quotes-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## 📡 API Endpoints

### Quotes

- `GET /quotes` - Get all quotes (with pagination)
- `GET /quotes/{id}` - Get specific quote
- `POST /quotes` - Add new quote
- `GET /quotes/random` - Get random quote

### Users

- `GET /users` - Get all users
- `GET /users/{id}` - Get specific user
- `POST /users` - Create new user

### Interactions

- `POST /like` - Like a quote
- `POST /unlike` - Unlike a quote
- `GET /liked/{user_id}` - Get user's liked quotes

### Recommendations

- `POST /recommendations` - Get personalized recommendations

## 🎯 Usage

1. **Login**: Enter your username or create a new account
2. **Browse Quotes**: Explore the quote library on the home page
3. **Like Quotes**: Click the heart icon to like quotes you enjoy
4. **Get Recommendations**: Visit the Quotes page for personalized suggestions
5. **Add Quotes**: Share your favorite quotes with the community

## 📊 Dataset

- **3,003 quotes** from renowned authors
- **302 users** with interaction data for ML training
- Authors include: Oscar Wilde, Mahatma Gandhi, Albert Einstein, Marilyn Monroe, and many more
- Categories: inspirational, life, love, philosophy, wisdom, humor, and more

## 🤖 Machine Learning

The recommendation system uses **Association Rule Mining (Apriori algorithm)** to:

- Identify patterns in user quote preferences
- Generate "users who liked this also liked..." suggestions
- Provide personalized recommendations based on collaborative filtering
- Continuously improve with user interactions

## 🔧 Development

### Backend Development

```bash
cd quotes-api
uvicorn quotes-api:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd quotes-frontend
npm run dev
```

### Build for Production

```bash
cd quotes-frontend
npm run build
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Hossem Charrak**

- GitHub: [@HossemCharrak](https://github.com/HossemCharrak)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Quote data sourced from various public datasets
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons from [Lucide](https://lucide.dev/)

---

⭐ If you find this project helpful, please consider giving it a star!
