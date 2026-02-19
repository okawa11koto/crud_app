from flask import Flask, request, jsonify
from models import db, User
from flask_caching import Cache

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'redis'
app.config['CACHE_REDIS_PORT'] = 6379

db.init_app(app)
cache = Cache(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(name=data['name'])
    db.session.add(user)
    db.session.commit()
    cache.clear()
    return jsonify({'id': user.id, 'name': user.name})

@app.route('/users', methods=['GET'])
@cache.cached(timeout=60)
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name} for u in users])

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    user.name = request.json['name']
    db.session.commit()
    cache.clear()
    return jsonify({'id': user.id, 'name': user.name})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    cache.clear()
    return '', 204
