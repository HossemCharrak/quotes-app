import logging
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import ast
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


# FastAPI app instance
app = FastAPI()

# Allow requests from all origins (adjust as needed for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Data model for a quote (for response validation)
class Quote(BaseModel):
    id: int
    quote: str
    author: str
    tags: Optional[str] = None
    likes: int = 0
    isLiked: Optional[bool] = False
    
class newQuote(BaseModel):
    quote: str
    author: str
    tags: Optional[str] = None
    likes: int = 0

class updater(BaseModel):
    id: int
    user_id: int

class User(BaseModel):
    id: int
    name: str

class RecommendationRequest(BaseModel):
    username: str
    liked_quotes: list

class QuotesByIdsRequest(BaseModel):
    user_id: int
    quote_ids: List[int]

# Database utility functions
DATABASE_PATH = "db/quotes.db"

# Function to get a connection to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Allows access to rows as dictionaries
    return conn

# Create a quote (Insert into database)
@app.post("/quotes/", response_model=Quote)
def create_quote(quote: newQuote):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if quote already exists (based on 'quote' text)
    cursor.execute("SELECT * FROM quotes WHERE quote = ?", (quote.quote,))
    existing_quote = cursor.fetchone()
    
    if existing_quote:
        conn.close()  # Ensure the connection is closed
        raise HTTPException(status_code=400, detail="Quote already exists.")
    cursor.execute("SELECT MAX(id) AS last_id FROM quotes;")
    last_id = cursor.fetchone()
    last_id = last_id["last_id"]
    # Insert the new quote into the database with auto-generated id
    cursor.execute(
        "INSERT INTO quotes (id, quote, author, tags, likes) VALUES (?, ?, ?, ?, ?)",
        (last_id+1,quote.quote, quote.author, quote.tags, quote.likes),
    )
    conn.commit()
    
    # Retrieve the newly created quote with its auto-generated id
    cursor.execute("SELECT * FROM quotes WHERE id = last_insert_rowid()")
    new_quote = cursor.fetchone()
    conn.close()

    return dict(new_quote)

# Read all quotes from the database
@app.get("/quotes", response_model=List[Quote])
def read_quotes(user_id: int,limit: int = 10, skip: int = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    cursor.execute("SELECT * FROM likes WHERE user_id = ?", (user_id,))
    likes = cursor.fetchall()
    rows = [dict(row) for row in rows]  # Convert rows to list of dictionaries
    for row in rows:
        row["isLiked"] = False
        for like in likes:
            if like["quote_id"] == row["id"]:
                row["isLiked"] = True
                break
    conn.close()

    return rows

# Read a single quote by id
@app.get("/quotes/{id}", response_model=Quote)
def read_quote(id: int, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        cursor.execute("SELECT * FROM likes WHERE user_id = ? and quote_id = ?", (user_id, id,))
        like = cursor.fetchone()
        row = dict(row)
        if like:
            row["isLiked"] = True
        conn.close()
        return row
    else:
        conn.close()
        raise HTTPException(status_code=404, detail="Quote not found.")

# Update likes for a quote
@app.patch("/quotes/{id}/likes", response_model=Quote)
def update_likes(updater: updater):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the user already liked the quote
        cursor.execute(
            "SELECT * FROM likes WHERE user_id = ? AND quote_id = ?", (updater.user_id, updater.id)
        )
        like = cursor.fetchone()

        if like:
            # Unlike the quote
            cursor.execute("UPDATE quotes SET likes = likes - 1 WHERE id = ?", (updater.id,))
            cursor.execute(
                "DELETE FROM likes WHERE user_id = ? AND quote_id = ?", (updater.user_id, updater.id)
            )
            isLiked = False
        else:
            # Like the quote
            cursor.execute("UPDATE quotes SET likes = likes + 1 WHERE id = ?", (updater.id,))
            cursor.execute(
                "INSERT INTO likes (user_id, quote_id) VALUES (?, ?)", (updater.user_id, updater.id)
            )
            isLiked = True

        conn.commit()

        # Fetch the updated quote directly
        cursor.execute("SELECT * FROM quotes WHERE id = ?", (updater.id,))
        updated_quote = cursor.fetchone()

        if not updated_quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found"
            )

        # Convert to dictionary and include `isLiked`
        updated_quote = dict(updated_quote)
        updated_quote["isLiked"] = isLiked

        return updated_quote

    except sqlite3.Error as e:
        logging.error("SQLite error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating likes.",
        )
    finally:
        conn.close()


# Delete a quote by id
@app.delete("/quotes/{id}", response_model=Quote)
def delete_quote(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes WHERE id = ?", (id,))
    row = cursor.fetchone()

    if row:
        cursor.execute("DELETE FROM quotes WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return dict(row)
    else:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found.")

# Search for a user by username
@app.get("/users/search", response_model=User)
def search_user(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE name = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    else:
        raise HTTPException(status_code=404, detail="User not found.")


@app.get("/recommendation_request/{user_id}", response_model=RecommendationRequest)
def get_recommendation_request(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch the user by user_id
    cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Fetch liked quotes by user_id
    cursor.execute("SELECT quote_id FROM likes WHERE user_id = ?", (user_id,))
    liked_quotes = cursor.fetchall()
    
    conn.close()
    
    liked_quotes = [quote["quote_id"] for quote in liked_quotes]
    
    return RecommendationRequest(username=user["name"], liked_quotes=liked_quotes)

# Get a list of quotes by their IDs and set isLiked based on the user
@app.post("/quotes/by_ids", response_model=List[Quote])
def get_quotes_by_ids(request: QuotesByIdsRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    user_id = request.user_id
    quote_ids_tuple = tuple(request.quote_ids)
    cursor.execute(f"SELECT * FROM quotes WHERE id IN ({','.join(['?']*len(quote_ids_tuple))})", quote_ids_tuple)
    rows = cursor.fetchall()
    
    cursor.execute("SELECT * FROM likes WHERE user_id = ?", (user_id,))
    likes = cursor.fetchall()
    likes_set = {like["quote_id"] for like in likes}
    
    quotes = []
    for row in rows:
        quote = dict(row)
        quote["isLiked"] = quote["id"] in likes_set
        quotes.append(quote)
    
    conn.close()
    return quotes

# Load and process data (sample size and confidence threshold can be modified)
def load_data():
    """Load the data."""
    users_df = pd.read_csv('db/data/users.csv')
    users_df['likes'] = users_df['likes'].apply(ast.literal_eval)
    return users_df

def process_transactions(users_df):
    """Transform transactions into a one-hot encoded DataFrame."""
    transactions = users_df['likes'].tolist()
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    return pd.DataFrame(te_ary, columns=te.columns_)

def generate_association_rules(df_onehot, min_support=0.01, min_confidence=0.5):
    """Generate association rules."""
    frequent_itemsets = apriori(df_onehot, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets,frequent_itemsets.shape[0], metric="confidence", min_threshold=min_confidence)
    return rules

def recommend_quotes_association(user_likes, rules):
    """Recommend quotes based on association rules."""
    recommendations = []
    for _, rule in rules.iterrows():
        if set(rule['antecedents']).issubset(user_likes):
            recommendations.extend(rule['consequents'])
    recommendations = set(recommendations) - set(user_likes)
    return list(recommendations)

# Load and process data at startup
users_df = load_data()
df_onehot = process_transactions(users_df)
rules = generate_association_rules(df_onehot)

@app.post("/recommend")
def recommend(request: RecommendationRequest):
    """
    API endpoint to recommend quotes.
    - username: str
    - liked_quotes: list[int]
    """
    username = request.username
    user_likes = request.liked_quotes

    # Check if the user exists
    if username not in users_df['name'].values:
        raise HTTPException(status_code=404, detail=f"User {username} not found.")

    # Generate recommendations
    recommendations = recommend_quotes_association(user_likes, rules)

    # Return recommendations
    return {"username": username, "recommendations": recommendations}
