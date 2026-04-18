# FINNY Finance App - Backend
# Flask server for managing student purchases

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import transversal module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transversal.constants import CATEGORIES

# Initialize Flask app
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing) to allow frontend to communicate
CORS(app)

# In-memory storage for purchases
# Each purchase will be a dictionary with name, amount, and category
purchases = []

# POST route to add a new purchase
@app.route('/compras', methods=['POST'])
def add_purchase():
    """
    Add a new purchase to the list.
    Expects JSON data with: name, amount
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data or 'amount' not in data:
            return jsonify({'error': 'Missing required fields: name, amount'}), 400
        
        # Validate that amount is a number
        try:
            amount = float(data['amount'])
        except ValueError:
            return jsonify({'error': 'Amount must be a number'}), 400
        
        # Create purchase object
        purchase = {
            'id': len(purchases) + 1,  # Simple ID based on list length
            'name': data['name'],
            'amount': amount,
            'category': data.get('category', 'Other')  # Optional category field
        }
        
        # Add to purchases list
        purchases.append(purchase)
        
        # Return success response with the new purchase
        return jsonify({
            'message': 'Purchase added successfully',
            'purchase': purchase,
            'total_purchases': len(purchases)
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET route to retrieve all purchases
@app.route('/compras', methods=['GET'])
def get_purchases():
    """
    Retrieve all purchases stored in memory.
    Returns a list of all purchases and total spent.
    """
    try:
        # Calculate total amount spent
        total_spent = sum(p['amount'] for p in purchases)
        
        return jsonify({
            'purchases': purchases,
            'total': total_spent,
            'count': len(purchases),
            'categories': CATEGORIES
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'OK', 'message': 'FINNY Backend is running'}), 200

# Root route
@app.route('/', methods=['GET'])
def home():
    """Root endpoint"""
    return jsonify({'message': 'Welcome to FINNY Finance App API'}), 200

# Run the app
if __name__ == '__main__':
    print("Starting FINNY Finance App Backend...")
    print("Server running on http://localhost:5000")
    print("Available routes:")
    print("  GET  /compras - Retrieve all purchases")
    print("  POST /compras - Add a new purchase")
    print("  GET  /health - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)
