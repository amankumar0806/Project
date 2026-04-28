from flask import Flask
import mysql.connector
import redis
import os

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME")
)
cursor = db.cursor()

# Redis connection
#cache = redis.Redis(host="redis", port=6379, decode_responses=True)

cache = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

@app.route("/api")
def api():
    # Check cache first
    cached_value = cache.get("visits")

    if cached_value:
        return f"(NEW VERSION) (From Cache) Visits: {cached_value}"

    # If not in cache → go to DB
    cursor.execute("UPDATE visits SET count = count + 1")
    db.commit()

    cursor.execute("SELECT count FROM visits")
    count = cursor.fetchone()[0]

    # Store in cache
    cache.setex("visits", 10, count)  # expires in 10 sec

    return f"(NEW VERSION) (From DB) Visits: {count}"

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)