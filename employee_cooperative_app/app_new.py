from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'cooperative.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize database
db = SQLAlchemy(app)

# Import models
from models import Employee, SavingsType, SavingsTransaction, LoanApplication, LoanRepayment, Item, Period

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/barang')
def barang():
    items = Item.query.all()
    return render_template('master_barang.html', items=items)

@app.route('/form-transaksi')
def form_transaksi():
    return render_template('form_transaksi.html')

@app.route('/simpanan')
def simpanan():
    return render_template('simpanan_penarikan.html')

@app.route('/permohonan-pinjaman')
def permohonan_pinjaman():
    return render_template('permohonan_pinjaman.html')

@app.route('/tagihan')
def tagihan():
    return render_template('tagihan_angsuran.html')

@app.route('/pembayaran-angsuran')
def pembayaran_angsuran():
    return render_template('angsuran_pinjaman.html')

@app.route('/perhitungan-shu')
def perhitungan_shu():
    return render_template('perhitungan_shu.html')

@app.route('/karyawan')
def karyawan():
    employees = Employee.query.all()
    return render_template('master_karyawan.html', employees=employees)

@app.route('/periode')
def periode():
    periods = Period.query.all()
    return render_template('master_periode.html', periods=periods)

@app.route('/jenis-simpanan')
def jenis_simpanan():
    types = SavingsType.query.all()
    return render_template('jenis_simpanan.html', types=types)

@app.route('/pembelian')
def pembelian():
    return render_template('form_pembelian.html')

@app.route('/laporan')
def laporan():
    return render_template('laporan.html')

@app.route('/import-database', methods=['GET', 'POST'])
def import_database():
    if request.method == 'POST':
        if 'database_file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['database_file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
            
        if not file.filename.endswith(('.mdb', '.accdb')):
            flash('Invalid file type. Please upload .mdb or .accdb file')
            return redirect(request.url)
            
        try:
            # For now, just return success message
            flash('Database import functionality will be implemented soon')
            return redirect(url_for('import_database'))
            
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(request.url)
            
    return render_template('import_database.html')

# API endpoints
@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = []
    for emp in employees:
        result.append({
            'id': emp.id,
            'nik': emp.nik,
            'nama': emp.nama,
            'bagian': emp.bagian,
            'jabatan': emp.jabatan,
            'jk': emp.jk,
            'tmk': emp.tmk.strftime('%Y-%m-%d') if emp.tmk else None,
            'iuran_wajib': emp.iuran_wajib,
            'tgl_keluar': emp.tgl_keluar.strftime('%Y-%m-%d') if emp.tgl_keluar else None,
            'status': emp.status,
            'max_plafon': emp.max_plafon,
            'max_plafon_sembako': emp.max_plafon_sembako
        })
    return jsonify(result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)
