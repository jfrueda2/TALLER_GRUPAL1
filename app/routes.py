from flask import jsonify, request, render_template, redirect, url_for
from app import app, db
from app.models import Producto

# Rutas para la Interfaz Gráfica
@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        
        nuevo_producto = Producto(nombre=nombre, precio=precio, descripcion=descripcion)
        db.session.add(nuevo_producto)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('agregar.html')

@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.descripcion = request.form['descripcion']
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('actualizar.html', producto=producto)

@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('index'))

# API
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([{'id': p.id, 'nombre': p.nombre, 'precio': p.precio, 'descripcion': p.descripcion} for p in productos])

@app.route('/api/productos', methods=['POST'])
def api_agregar_producto():
    datos = request.get_json()
    nuevo_producto = Producto(nombre=datos['nombre'], precio=datos['precio'], descripcion=datos.get('descripcion'))
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({'id': nuevo_producto.id}), 201

@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify({'id': producto.id, 'nombre': producto.nombre, 'precio': producto.precio, 'descripcion': producto.descripcion})

@app.route('/api/productos/<int:id>', methods=['PUT'])
def api_actualizar_producto(id):
    datos = request.get_json()
    producto = Producto.query.get_or_404(id)
    producto.nombre = datos['nombre']
    producto.precio = datos['precio']
    producto.descripcion = datos.get('descripcion')
    db.session.commit()
    return jsonify({'id': producto.id})

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def api_eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return '', 204