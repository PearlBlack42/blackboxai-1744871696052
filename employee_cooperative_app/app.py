from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cooperative.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    bagian = db.Column(db.String(100))
    jabatan = db.Column(db.String(100))
    jk = db.Column(db.String(1))  # L or P
    tmk = db.Column(db.Date)
    iuran_wajib = db.Column(db.Float, default=0)
    tgl_keluar = db.Column(db.Date, nullable=True)
    status = db.Column(db.Boolean, default=True)
    max_plafon = db.Column(db.Float, default=0)
    max_plafon_sembako = db.Column(db.Float, default=0)

class SavingsType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jenis_id = db.Column(db.String(10), unique=True, nullable=False)
    keterangan = db.Column(db.String(100))
    operator = db.Column(db.String(1))  # + or -

class SavingsTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    periode = db.Column(db.String(20), nullable=False)
    jenis_id = db.Column(db.String(10), db.ForeignKey('savings_type.jenis_id'), nullable=False)
    jumlah = db.Column(db.Float, nullable=False)
    tanggal = db.Column(db.Date, default=datetime.utcnow)

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    periode_pengajuan = db.Column(db.String(20), nullable=False)
    total_simpanan = db.Column(db.Float, default=0)
    sisa_angsuran = db.Column(db.Float, default=0)
    n_akhir = db.Column(db.Integer, default=0)
    jumlah = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Approved, Rejected

class LoanRepayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan_application.id'), nullable=False)
    periode = db.Column(db.String(20), nullable=False)
    ang_ke = db.Column(db.Integer, nullable=False)
    ang_pokok = db.Column(db.Float, nullable=False)
    bunga = db.Column(db.Float, nullable=False)
    jumlah = db.Column(db.Float, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode_barang = db.Column(db.String(50), unique=True, nullable=False)
    nama_barang = db.Column(db.String(100), nullable=False)
    satuan = db.Column(db.String(20))
    stok_awal = db.Column(db.Integer, default=0)
    harga_beli = db.Column(db.Float, default=0)
    margin = db.Column(db.Float, default=0)
    harga_jual = db.Column(db.Float, default=0)

class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    periode_id = db.Column(db.String(10), unique=True, nullable=False)
    periode = db.Column(db.String(50), nullable=False)
    awal = db.Column(db.Date, nullable=True)
    akhir = db.Column(db.Date, nullable=True)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/barang')
def master_barang():
    # For now, just render the form page
    return render_template('master_barang.html')

# API example: Get all employees
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
    app.run(debug=True)
