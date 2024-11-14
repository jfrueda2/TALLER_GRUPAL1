# TALLER_GRUPAL1
Crear una API

Este proyecto es una API y una interfaz gráfica para la gestión de productos. Permite realizar operaciones CRUD sobre productos (Crear, Leer, Actualizar, Eliminar).

## Requisitos

- Python 
- Flask
- Flask-SQLAlchemy
- Postman 
- MySQL

## Instalación

Para ejecutar el programa debemos estar en la raiz de la carpeta y ejecutar el comando

 - docker-compose up --build 

Se deber tomar en cuenta que en primera instancia, se va a generar ciertos errores hasta
que la base de datos se active correctamente.

## Endpoints

Se crearon endpoints para ver, editar, guardar y eliminar

# VER TODOS LOS PRODUCTOS
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([{'id': p.id, 'nombre': p.nombre, 'precio': p.precio, 'descripcion': p.descripcion} for p in productos])

# AGREGAR
@app.route('/api/productos', methods=['POST'])
def api_agregar_producto():
    datos = request.get_json()
    nuevo_producto = Producto(nombre=datos['nombre'], precio=datos['precio'], descripcion=datos.get('descripcion'))
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({'id': nuevo_producto.id}), 201

# OBTENER POR ID
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify({'id': producto.id, 'nombre': producto.nombre, 'precio': producto.precio, 'descripcion': producto.descripcion})

# ACTUALIZAR
@app.route('/api/productos/<int:id>', methods=['PUT'])
def api_actualizar_producto(id):
    datos = request.get_json()
    producto = Producto.query.get_or_404(id)
    producto.nombre = datos['nombre']
    producto.precio = datos['precio']
    producto.descripcion = datos.get('descripcion')
    db.session.commit()
    return jsonify({'id': producto.id})

# ELIMINAR
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def api_eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return '', 204
