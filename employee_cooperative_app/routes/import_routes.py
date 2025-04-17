from flask import Blueprint, render_template, jsonify, flash
from ..database_import import handle_database_import

import_bp = Blueprint('import_bp', __name__)

@import_bp.route('/import-database', methods=['GET'])
def import_database_page():
    """Render the database import page"""
    return render_template('import_database.html')

@import_bp.route('/import-database/execute', methods=['POST'])
def execute_import():
    """Execute the database import process"""
    try:
        success, result = handle_database_import()
        
        if success:
            flash('Database imported successfully', 'success')
            return jsonify({
                'status': 'success',
                'message': result['message'],
                'details': result['details']
            })
        else:
            flash('Import failed: ' + str(result), 'error')
            return jsonify({
                'status': 'error',
                'message': str(result)
            }), 400
            
    except Exception as e:
        flash('Error during import: ' + str(e), 'error')
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
