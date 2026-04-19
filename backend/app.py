# FINNY Finance App - Backend v2
# Flask REST API with gamification, budget, streaks, missions, achievements

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transversal.constants import CATEGORIES, MAX_NAME_LENGTH, MAX_AMOUNT
from backend.database import (
    init_db,
    # Purchases
    create_purchase, get_all_purchases, get_purchase_by_id,
    delete_purchase, get_stats,
    # Budget
    get_budget, set_budget,
    # Profile
    get_profile, update_profile, increment_tips_read,
    # Streak
    get_streak,
    # Missions / Achievements
    get_missions, get_achievements,
    # Dashboard & analytics
    get_dashboard_data, get_spending_trend, get_tips,
)

app = Flask(__name__)
CORS(app)
init_db()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _validate_purchase(data: dict):
    """Returns error string or None if valid."""
    if not data:
        return 'El cuerpo de la solicitud debe ser JSON válido.'
    name = str(data.get('name', '')).strip()
    if not name:
        return 'El campo "name" es requerido.'
    if len(name) > MAX_NAME_LENGTH:
        return f'El nombre no puede superar {MAX_NAME_LENGTH} caracteres.'
    raw = data.get('amount')
    if raw is None:
        return 'El campo "amount" es requerido.'
    try:
        amount = float(raw)
    except (TypeError, ValueError):
        return 'El campo "amount" debe ser un número.'
    if amount <= 0:
        return 'El monto debe ser mayor que 0.'
    if amount > MAX_AMOUNT:
        return f'El monto no puede superar {MAX_AMOUNT:,.2f}.'
    cat = data.get('category', '')
    valid = CATEGORIES + ['Other']
    if cat and cat not in valid:
        return f'Categoría inválida. Use: {", ".join(valid)}'
    return None


# ── Root ──────────────────────────────────────────────────────────────────────

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'app': 'FINNY Finance API',
        'version': '2.0.0',
        'endpoints': {
            'GET  /dashboard':         'Resumen completo del dashboard',
            'GET  /compras':           'Listar compras (opcional ?category=)',
            'POST /compras':           'Crear una compra',
            'GET  /compras/<id>':      'Obtener una compra por ID',
            'DELETE /compras/<id>':    'Eliminar una compra',
            'GET  /estadisticas':      'Estadísticas por categoría',
            'GET  /tendencia':         'Tendencia de gasto (últimos días, ?days=7)',
            'GET  /presupuesto':       'Obtener presupuesto actual',
            'POST /presupuesto':       'Guardar presupuesto mensual',
            'GET  /racha':             'Estado de la racha diaria',
            'GET  /misiones':          'Lista de misiones con progreso',
            'GET  /logros':            'Lista de logros (bloqueados/desbloqueados)',
            'GET  /consejos':          'Consejos personalizados (?limit=3)',
            'POST /consejos/leer':     'Marcar un consejo como leído (+XP)',
            'GET  /perfil':            'Perfil del usuario',
            'PUT  /perfil':            'Actualizar nombre o avatar',
            'GET  /categorias':        'Categorías disponibles',
            'GET  /health':            'Health check',
        }
    }), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK', 'message': 'FINNY Backend running'}), 200


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Single endpoint that returns everything needed for the main view."""
    try:
        data = get_dashboard_data()
        data['streak']  = get_streak()
        data['profile'] = get_profile()
        data['trend']   = get_spending_trend(7)
        data['tips']    = get_tips(3)
        data['missions_active'] = [m for m in get_missions() if not m['completed']][:3]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Compras ───────────────────────────────────────────────────────────────────

@app.route('/compras', methods=['GET'])
def list_purchases():
    try:
        cat = request.args.get('category', '').strip() or None
        if cat and cat not in (CATEGORIES + ['Other']):
            return jsonify({'error': f'Categoría inválida: "{cat}"'}), 400
        purchases = get_all_purchases(category=cat)
        total = sum(p['amount'] for p in purchases)
        return jsonify({
            'purchases':   purchases,
            'total':       round(total, 2),
            'count':       len(purchases),
            'categories':  CATEGORIES + ['Other'],
            'filtered_by': cat,
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compras', methods=['POST'])
def add_purchase():
    try:
        data = request.get_json(silent=True)
        err = _validate_purchase(data)
        if err:
            return jsonify({'error': err}), 400
        name     = data['name'].strip()
        amount   = round(float(data['amount']), 2)
        category = data.get('category', 'Other').strip() or 'Other'
        purchase = create_purchase(name, amount, category)
        return jsonify({'message': 'Compra agregada correctamente.', 'purchase': purchase}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compras/<int:pid>', methods=['GET'])
def get_purchase(pid):
    try:
        p = get_purchase_by_id(pid)
        if not p:
            return jsonify({'error': f'Compra {pid} no encontrada.'}), 404
        return jsonify({'purchase': p}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compras/<int:pid>', methods=['DELETE'])
def remove_purchase(pid):
    try:
        if not delete_purchase(pid):
            return jsonify({'error': f'Compra {pid} no encontrada.'}), 404
        return jsonify({'message': f'Compra {pid} eliminada.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Estadísticas & tendencia ──────────────────────────────────────────────────

@app.route('/estadisticas', methods=['GET'])
def stats():
    try:
        return jsonify(get_stats()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tendencia', methods=['GET'])
def trend():
    try:
        days = int(request.args.get('days', 7))
        days = max(3, min(days, 90))
        return jsonify({'trend': get_spending_trend(days), 'days': days}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Presupuesto ───────────────────────────────────────────────────────────────

@app.route('/presupuesto', methods=['GET'])
def get_presupuesto():
    try:
        return jsonify(get_budget()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/presupuesto', methods=['POST'])
def set_presupuesto():
    try:
        data = request.get_json(silent=True)
        if not data or 'amount' not in data:
            return jsonify({'error': 'Se requiere el campo "amount".'}), 400
        amount = float(data['amount'])
        if amount < 0:
            return jsonify({'error': 'El presupuesto no puede ser negativo.'}), 400
        budget = set_budget(amount)
        return jsonify({'message': 'Presupuesto guardado.', 'budget': budget}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Racha ─────────────────────────────────────────────────────────────────────

@app.route('/racha', methods=['GET'])
def racha():
    try:
        return jsonify(get_streak()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Misiones ──────────────────────────────────────────────────────────────────

@app.route('/misiones', methods=['GET'])
def misiones():
    try:
        return jsonify({'missions': get_missions()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Logros ────────────────────────────────────────────────────────────────────

@app.route('/logros', methods=['GET'])
def logros():
    try:
        return jsonify({'achievements': get_achievements()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Consejos ──────────────────────────────────────────────────────────────────

@app.route('/consejos', methods=['GET'])
def consejos():
    try:
        limit = int(request.args.get('limit', 3))
        return jsonify({'tips': get_tips(limit)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/consejos/leer', methods=['POST'])
def marcar_consejo_leido():
    """Mark a tip as read to update tips_read counter and trigger mission checks."""
    try:
        profile = increment_tips_read()
        return jsonify({'message': 'Consejo marcado como leído. +5 XP', 'profile': profile}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Perfil ────────────────────────────────────────────────────────────────────

@app.route('/perfil', methods=['GET'])
def perfil():
    try:
        return jsonify(get_profile()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/perfil', methods=['PUT'])
def update_perfil():
    try:
        data = request.get_json(silent=True) or {}
        profile = update_profile(
            name=data.get('name', '').strip() or None,
            avatar=data.get('avatar', '').strip() or None,
        )
        return jsonify({'message': 'Perfil actualizado.', 'profile': profile}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Categorías ────────────────────────────────────────────────────────────────

@app.route('/categorias', methods=['GET'])
def categorias():
    return jsonify({'categories': CATEGORIES + ['Other']}), 200


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('=' * 55)
    print('  FINNY Finance App Backend v2.0')
    print('  Server -> http://localhost:5000')
    print('=' * 55)
    app.run(debug=True, host='0.0.0.0', port=5000)
