# Quotes API

A modern REST API built with FastAPI that delivers inspirational quotes with intelligent recommendations powered by machine learning. Users can browse, like, and receive personalized quote suggestions based on collaborative filtering.

## ✨ Features

- **📚 Quote Management**: Full CRUD operations for quotes with pagination support
- **❤️ User Interactions**: Like/unlike quotes with real-time tracking
- **🤖 Smart Recommendations**: ML-powered quote suggestions using association rule mining (Apriori algorithm)
- **👥 Multi-user Support**: Personalized experiences for each user
- **🏷️ Categorization**: Quotes organized by tags (inspirational, philosophy, love, etc.)
- **🚀 Fast & Modern**: Built with FastAPI for high performance and automatic API documentation

## 🛠️ Tech Stack

- **FastAPI** - Modern, high-performance web framework
- **SQLite** - Lightweight, embedded database
- **Pandas** - Data manipulation and analysis
- **mlxtend** - Association rule mining for recommendations
- **scikit-learn** - Machine learning utilities
- **Pydantic** - Data validation using Python type hints

## 📊 Dataset

- **3,003** carefully curated quotes from renowned authors
- **302** users with existing interaction data for ML training
- Authors include: Oscar Wilde, Mahatma Gandhi, Albert Einstein, Marilyn Monroe, and many more
- Categories: inspirational, life, love, philosophy, wisdom, humor, and more

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd quotes-api
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**

   ```bash
   python db/scripts/init_db.py
   ```

   This will create the SQLite database and populate it with quotes and user data.

5. **Verify database setup** (optional)
   ```bash
   python db/scripts/read_db.py
   ```

## 🎯 Running the API

Start the development server:

```bash
uvicorn quotes-api:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### Quotes

| Method   | Endpoint             | Description                | Parameters                 |
| -------- | -------------------- | -------------------------- | -------------------------- |
| `GET`    | `/quotes`            | Get paginated quotes       | `user_id`, `limit`, `skip` |
| `GET`    | `/quotes/{id}`       | Get single quote by ID     | `id`, `user_id`            |
| `POST`   | `/quotes/`           | Create a new quote         | Request body               |
| `PATCH`  | `/quotes/{id}/likes` | Toggle like on a quote     | Request body               |
| `DELETE` | `/quotes/{id}`       | Delete a quote             | `id`                       |
| `POST`   | `/quotes/by_ids`     | Get multiple quotes by IDs | Request body               |

### Users

| Method | Endpoint                            | Description             | Parameters |
| ------ | ----------------------------------- | ----------------------- | ---------- |
| `GET`  | `/users/search`                     | Search user by username | `username` |
| `GET`  | `/recommendation_request/{user_id}` | Get user's liked quotes | `user_id`  |

### Recommendations

| Method | Endpoint     | Description                      | Parameters   |
| ------ | ------------ | -------------------------------- | ------------ |
| `POST` | `/recommend` | Get personalized recommendations | Request body |

## 💡 Usage Examples

### Get Quotes (with pagination)

```bash
curl "http://localhost:8000/quotes?user_id=1&limit=10&skip=0"
```

### Get a Single Quote

```bash
curl "http://localhost:8000/quotes/5?user_id=1"
```

### Create a New Quote

```bash
curl -X POST "http://localhost:8000/quotes/" \
  -H "Content-Type: application/json" \
  -d '{
    "quote": "The only way to do great work is to love what you do.",
    "author": "Steve Jobs",
    "tags": "inspirational;work;passion",
    "likes": 0
  }'
```

### Like/Unlike a Quote

```bash
curl -X PATCH "http://localhost:8000/quotes/5/likes" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 5,
    "user_id": 1
  }'
```

### Get Personalized Recommendations

```bash
curl -X POST "http://localhost:8000/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "User1",
    "liked_quotes": [1, 5, 10, 15, 20]
  }'
```

### Search for a User

```bash
curl "http://localhost:8000/users/search?username=User1"
```

## 🗂️ Project Structure

```
quotes-api/
├── quotes-api.py           # Main FastAPI application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── db/
    ├── quotes.db          # SQLite database (generated)
    ├── data/
    │   ├── quotes.csv     # Source data for quotes
    │   └── users.csv      # Source data for users
    └── scripts/
        ├── init_db.py     # Database initialization script
        └── read_db.py     # Database verification script
```

## 🤖 How the Recommendation Engine Works

The recommendation system uses **Association Rule Mining** with the Apriori algorithm:

1. **Data Collection**: Analyzes historical user-quote interactions (likes)
2. **Pattern Discovery**: Identifies frequent itemsets (quotes often liked together)
3. **Rule Generation**: Creates association rules (if user likes quotes A and B, they'll likely enjoy C)
4. **Personalization**: Recommends quotes based on user's current likes and discovered patterns

### Configurable Parameters

- `min_support`: Minimum frequency for itemsets (default: 0.01)
- `min_confidence`: Minimum confidence for rules (default: 0.5)

## 🔧 Database Schema

### Tables

**quotes**

- `id` (INTEGER, PRIMARY KEY)
- `quote` (TEXT)
- `author` (TEXT)
- `tags` (TEXT)
- `likes` (INTEGER)

**users**

- `id` (INTEGER, PRIMARY KEY)
- `name` (TEXT)

**likes**

- `user_id` (INTEGER, FOREIGN KEY)
- `quote_id` (INTEGER, FOREIGN KEY)
- PRIMARY KEY: (`user_id`, `quote_id`)

## 🌐 CORS Configuration

The API is configured to accept requests from all origins. For production use, update the CORS settings in `quotes-api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Testing

You can test the API using:

- **curl** (command line)
- **Postman** or **Insomnia** (GUI clients)
- **Swagger UI** at http://localhost:8000/docs (built-in)

## 📝 Response Format

All endpoints return JSON responses. Example quote object:

```json
{
  "id": 1,
  "quote": "Be yourself; everyone else is already taken.",
  "author": "Oscar Wilde",
  "tags": "attributed-no-source;be-yourself;honesty;inspirational",
  "likes": 149270,
  "isLiked": true
}
```

## 🚨 Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (e.g., duplicate quote)
- `404` - Not Found
- `500` - Internal Server Error

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Advanced search and filtering
- [ ] Quote categories/collections
- [ ] Social sharing features
- [ ] Rating system (beyond just likes)
- [ ] Admin panel
- [ ] Export quotes to various formats
- [ ] Multi-language support

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 👤 Author

Your Name

---

⭐ If you found this project helpful, please give it a star!
