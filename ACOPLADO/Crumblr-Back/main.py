from flask import Flask, request, jsonify
from pydantic import ValidationError
import psycopg2
from models.crumb import Crumb
from db.factory import DatabaseFactory

app = Flask(__name__)

# Inicializar base de datos
try:
    db = DatabaseFactory.create()
except ValueError as e:
    raise RuntimeError(f"Error initializing DB: {e}") from e


# Middleware CORS
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response


# Crear un nuevo crumb
@app.route('/crumbs', methods=['POST'])
def create_crumb():
    try:
        data = request.get_json()
        crumb = Crumb(**data)
        created = db.create_crumb(crumb)
        return jsonify(created.__dict__), 201
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.errors()}), 400
    except psycopg2.IntegrityError as e:
        return jsonify({'error': 'Database integrity error', 'details': str(e)}), 409
    except psycopg2.OperationalError as e:
        return jsonify({'error': 'Database connection error', 'details': str(e)}), 503
    except psycopg2.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500


# Obtener un crumb por ID
@app.route('/crumbs/<crumb_id>', methods=['GET'])
def get_crumb(crumb_id):
    try:
        crumb = db.get_crumb(crumb_id)
        if crumb:
            return jsonify(crumb.__dict__), 200
        return jsonify({'error': 'Crumb not found'}), 404
    except psycopg2.OperationalError as e:
        return jsonify({'error': 'Database connection error', 'details': str(e)}), 503
    except psycopg2.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500


# Obtener todos los crumbs
@app.route('/crumbs', methods=['GET'])
def get_all_crumbs():
    try:
        crumbs = db.get_all_crumbs()
        return jsonify([c.__dict__ for c in crumbs]), 200
    except psycopg2.OperationalError as e:
        return jsonify({'error': 'Database connection error', 'details': str(e)}), 503
    except psycopg2.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500


# Actualizar un crumb
@app.route('/crumbs/<crumb_id>', methods=['PUT'])
def update_crumb(crumb_id):
    try:
        data = request.get_json()
        data.pop('crumb_id', None)
        data.pop('created_at', None)
        crumb = Crumb(**data)
        updated = db.update_crumb(crumb_id, crumb)
        if updated:
            return jsonify(updated.__dict__), 200
        return jsonify({'error': 'Crumb not found'}), 404
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.errors()}), 400
    except psycopg2.IntegrityError as e:
        return jsonify({'error': 'Database integrity error', 'details': str(e)}), 409
    except psycopg2.OperationalError as e:
        return jsonify({'error': 'Database connection error', 'details': str(e)}), 503
    except psycopg2.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500


# Eliminar un crumb
@app.route('/crumbs/<crumb_id>', methods=['DELETE'])
def delete_crumb(crumb_id):
    try:
        if db.delete_crumb(crumb_id):
            return '', 204
        return jsonify({'error': 'Crumb not found'}), 404
    except psycopg2.OperationalError as e:
        return jsonify({'error': 'Database connection error', 'details': str(e)}), 503
    except psycopg2.Error as e:
        return jsonify({'error': 'Database error', 'details': str(e)}), 500


# Healthcheck
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
