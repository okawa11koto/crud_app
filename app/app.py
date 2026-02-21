import os, redis
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL', 'postgresql://user:pass@db/db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))

with app.app_context():
    try:
        db.create_all()
    except Exception:
        pass

@app.route('/item', methods=['POST'])
def add():
    data = request.json
    task = Task(text=data['text'])
    db.session.add(task)
    db.session.commit()
    return jsonify({"id": task.id}), 201

@app.route('/item/<int:id>', methods=['GET'])
def get(id):
    try:
        cached = cache.get(f"task:{id}")
        if cached:
            return jsonify({"data": cached, "source": "redis_cache"})
    except:
        pass

    task = Task.query.get_or_404(id)
    
    try:
        cache.setex(f"task:{id}", 30, task.text)
    except:
        pass

    return jsonify({"data": task.text, "source": "postgres_db"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
