# TALLER_GRUPAL1

## Crear una API

Este proyecto consiste en el desarrollo de una API junto con una interfaz gráfica para la gestión de productos. La API permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre productos, facilitando la interacción con una base de datos MySQL a través de Flask y Flask-SQLAlchemy.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalados los siguientes requisitos:

- Python
- Flask
- Flask-SQLAlchemy
- Postman
- MySQL

## Instalación

Para ejecutar el programa, primero debes estar en la raíz de la carpeta y ejecutar el siguiente comando:

```bash
docker-compose up --build 
```

Se deber tomar en cuenta que en primera instancia, se va a generar ciertos errores hasta
que la base de datos se active correctamente.

# Endpoints 

Se han creado varios endpoints para interactuar con los productos. A continuación, se detallan los métodos disponibles, junto con una breve descripción de su funcionamiento.

## VER TODOS LOS PRODUCTOS
Este endpoint permite obtener todos los productos almacenados en la base de datos. Devuelve una lista con los productos disponibles, incluyendo su id, nombre, precio y descripción.
```bash
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([{'id': p.id, 'nombre': p.nombre, 'precio': p.precio, 'descripcion': p.descripcion} for p in productos])
```

 --POSTMAN 
```bash
 (get) http://localhost:5000/api/productos
```

 --PRUEBAS POSTMAN
```bash
 pm.test("Response status code is 200", function () {
    pm.expect(pm.response.code).to.equal(200);
});


pm.test("Response time is less than 200ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(200);
});


pm.test("Response has the required fields", function () {
    const responseData = pm.response.json();
    
    pm.expect(responseData).to.be.an('array');
    responseData.forEach(function(product) {
        pm.expect(product).to.have.property('id');
        pm.expect(product).to.have.property('nombre');
        pm.expect(product).to.have.property('descripcion');
        pm.expect(product).to.have.property('precio');
    });
});


pm.test("Id is a non-negative integer", function () {
    const responseData = pm.response.json();
    
    responseData.forEach(function (producto) {
        pm.expect(producto.id).to.be.a('number').and.to.be.at.least(0, "Id must be a non-negative integer");
    });
});


pm.test("Precio is a non-negative number", function () {
  const responseData = pm.response.json();
  
  responseData.forEach(function(item) {
    pm.expect(item.precio).to.be.a('number').and.to.be.at.least(0);
  });
});
```

## AGREGAR
Este endpoint permite agregar un nuevo producto a la base de datos. Se espera que el cliente envíe los datos del producto en formato JSON (nombre, precio, descripción). Al agregar un producto exitosamente, el servidor devolverá el id del producto creado.
```bash
@app.route('/api/productos', methods=['POST'])
def api_agregar_producto():
    datos = request.get_json()
    nuevo_producto = Producto(nombre=datos['nombre'], precio=datos['precio'], descripcion=datos.get('descripcion'))
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({'id': nuevo_producto.id}), 201
```
 --POSTMAN
```bash
(post) http://localhost:5000/api/productos
```
```bash
 {
  "nombre": "Product B",
  "precio": 9.99,
  "descripcion": "Holi amigos"
}
```
--PRUEBAS POSTMAN
```bash
pm.test("Response status code is 201", function () {
    pm.expect(pm.response.code).to.equal(201);
});


pm.test("Response time is less than 300ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(300);
});


pm.test("Response has the required fields", function () {
    const responseData = pm.response.json();
    
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData.id).to.exist;
});


pm.test("Id is a non-negative integer", function () {
  const responseData = pm.response.json();
  
  pm.expect(responseData.id).to.exist;
  pm.expect(responseData.id).to.be.a('number');
  pm.expect(responseData.id).to.be.at.least(0);
});


pm.test("Content-Type is application/json", function () {
  pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});
```
## OBTENER POR ID
Este endpoint permite obtener un producto específico utilizando su id. Si el producto no existe, devolverá un error 404. Si el producto existe, se devolverán los datos del producto solicitado.
```bash
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify({'id': producto.id, 'nombre': producto.nombre, 'precio': producto.precio, 'descripcion': producto.descripcion})
```
--POSTMAN
```bash
(get) http://localhost:5000/api/productos/1
```
--PRUEBAS POSTMAN
```bash
// Updated test script to handle the TypeError
pm.test("Response status code is 200", function () {
    pm.expect(pm.response.code).to.equal(200);
});


pm.test("Response time is less than 200ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(200);
});


pm.test("Response has the required fields", function () {
    const responseData = pm.response.json();
    
    pm.expect(responseData).to.be.an('object').and.to.have.property('id');
    pm.expect(responseData).to.have.property('nombre');
    pm.expect(responseData).to.have.property('descripcion');
    pm.expect(responseData).to.have.property('precio');
});


pm.test("Id is a non-negative integer", function () {
    const responseData = pm.response.json();
    
    pm.expect(responseData.id).to.be.a('number').and.to.be.at.least(0, "Id must be a non-negative integer");
});


pm.test("Precio is a non-negative number", function () {
    const responseData = pm.response.json();
  
    pm.expect(responseData.precio).to.be.a('number').and.to.be.at.least(0);
});
```
## ACTUALIZAR
Este endpoint permite actualizar los detalles de un producto específico. Se requiere enviar los nuevos valores del producto en el cuerpo de la solicitud en formato JSON. El id del producto debe ser proporcionado en la URL. Si la actualización es exitosa, se devolverá el id del producto actualizado.
```bash
@app.route('/api/productos/<int:id>', methods=['PUT'])
def api_actualizar_producto(id):
    datos = request.get_json()
    producto = Producto.query.get_or_404(id)
    producto.nombre = datos['nombre']
    producto.precio = datos['precio']
    producto.descripcion = datos.get('descripcion')
    db.session.commit()
    return jsonify({'id': producto.id})
```
--POSTMAN
```bash
(put) http://localhost:5000/api/productos/1

--PRUEBAS POSTMAN

pm.test("Response status code is 200", function () {
    pm.response.to.have.status(200);
});


pm.test("Response has the required fields", function () {
    const responseData = pm.response.json();
    
    pm.expect(responseData).to.be.an('object');
    pm.expect(responseData.id).to.exist;
});


pm.test("Response Content-Type is application/json", function () {
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});


pm.test("Response time is less than 200ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(200);
});
```

## ELIMINAR
Este endpoint permite eliminar un producto específico de la base de datos utilizando su id. Si el producto es eliminado correctamente, el servidor devolverá un código de estado 204 sin contenido.
```bash
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def api_eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return '', 204
```
--POSTMAN
```bash
(delete) http://localhost:5000/api/productos/4
```
--PRUEBAS POSTMAN
```bash
pm.test("Response status code is 204", function () { 
    pm.expect(pm.response.code).to.equal(204); 
});

pm.test("Response time is less than 300ms", function () {  
    pm.expect(pm.response.responseTime).to.be.below(300); 
});

pm.test("Response body is empty after successful deletion", function () { 
    pm.expect(pm.response.text()).to.be.empty; 
});
```
