from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.security import check_password_hash
from models import db, User, Item, Prestamo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# -------------------
# LOGIN
# -------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrecta", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------
# DASHBOARD
# -------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# -------------------
# INVENTARIO
# -------------------
@app.route('/items')
def items():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    items = Item.query.all()
    return render_template('items.html', items=items)

@app.route('/items/add', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        item = Item(
            nombre=request.form['nombre'],
            cantidad=request.form['cantidad'],
            descripcion=request.form['descripcion']
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('items'))
    return render_template('add_item.html')

# -------------------
# PRESTAMOS
# -------------------
@app.route('/prestamos')
def prestamos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    prestamos = Prestamo.query.all()
    return render_template('prestamos.html', prestamos=prestamos)

@app.route('/prestamos/add', methods=['GET', 'POST'])
def add_prestamo():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    items = Item.query.all()

    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        cantidad = int(request.form['cantidad'])
        local = request.form['local']

        item = Item.query.get(item_id)
        if cantidad > item.cantidad:
            return "Error: No hay suficiente inventario", 400

        prestamo = Prestamo(
            item_id=item_id,
            cantidad=cantidad,
            local=local,
            usuario_id=session['user_id']
        )

        # Reducir stock del inventario
        item.cantidad -= cantidad

        db.session.add(prestamo)
        db.session.commit()
        return redirect(url_for('prestamos'))

    return render_template('add_prestamo.html', items=items)

@app.route('/prestamos/devolver/<int:prestamo_id>')
def devolver_prestamo(prestamo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    prestamo = Prestamo.query.get_or_404(prestamo_id)

    if prestamo.devuelto:
        return "Este préstamo ya fue devuelto", 400

    # Marcar como devuelto
    prestamo.devuelto = True
    prestamo.fecha_devolucion = db.func.now()

    # Devolver stock al inventario
    prestamo.item.cantidad += prestamo.cantidad

    db.session.commit()
    return redirect(url_for('prestamos'))

# -------------------
# RUN APP
# -------------------
if __name__ == '__main__':
    app.run(debug=True)