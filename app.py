from flask import Flask, jsonify, request
import datetime

UserData = [
    {
        "id_user": "admin",
        "user_name": "Daniel Cuque",
        "user_nickname": "danielcuque",
        "user_password": "danielcuque123",
        "user_rol": "Administrador",
        "available": True
    },
    {
        "id_user": "A1",
        "user_name": "Mario Lopez",
        "user_nickname": "mlopez",
        "user_password": "matecomputo",
        "user_rol": "Catedrático",
        "available": False
    }
]

BookData = [
    {
        "id_book": "1a",
        "book_author": "J.K. Rowling",
        "book_title": "Harry Potter y la piedra filosofal",
        "book_edition": 1,
        "book_editorial": "Editorial Potter",
        "book_year": 1997,
        "book_description": "La historia de Harry Potter y la piedra filosofal, la primera parte de la saga de libros de la autora.",
        "book_available_copies": 4,
        "book_unavailable_copies": 3,
        "book_copies": 5,
    },
    {
        "id_book": "2a",
        "book_author": "J.K. Rowling",
        "book_title": "Harry Potter y la cámara secreta",
        "book_edition": 1,
        "book_editorial": "Editorial Potter",
        "book_year": 1997,
        "book_description": "La historia de Harry Potter y la cámara secreta, la segunda parte de la saga de libros de la autora.",
        "book_available_copies": 2,
        "book_unavailable_copies": 3,
        "book_copies": 5,
    },
    {
        "id_book": "3a",
        "book_author": "Harry",
        "book_title": "Potter 2",
        "book_edition": 1,
        "book_editorial": "Editorial Potter",
        "book_year": 1997,
        "book_description": "La historia de Harry Potter y el prisionero de Azkaban, la tercera parte de la saga de libros de la autora.",
        "book_available_copies": 2,
        "book_unavailable_copies": 3,
        "book_copies": 5,
    }
]

BorrowData = []

app = Flask(__name__)

@app.route('/')
def home():
    initialMessage = {
        "msg": 'Servidor funcionando correctamente',
        "status": 200
    }
    
    return jsonify(initialMessage)

# Endpoints para usuarios
@app.route("/user", methods=["GET"])
def getUsuarios():
    return jsonify({'Usuarios': UserData, 'status': 200})


@app.route("/user/<string:id_user>", methods=["GET"])
def getUsuario(id_user):
    if not id_user or id_user == "":
        return jsonify({'message': 'No se recibió ningún dato', 'status': 404})
    else:
        for user in UserData:
            if user['id_user'] == id_user:
                return jsonify({'Usuario': user, 'status': 200})
        return jsonify({'message': 'No se encontró el usuario', 'status': 404})


@app.route("/user", methods=["PUT"])
def updateUsuario():

    # Validaciones de campos para la creación de usuarios
    if not request.json or not 'id_user' in request.json:
        return jsonify({'status': 400, 'message': 'No se recibió el id_user'})
    if not "user_name" in request.json:
        return jsonify({'message': 'No se recibio el nombre', 'status': 400})
    if not "user_nickname" in request.json:
        return jsonify({'message': 'No se recibio el nickname', 'status': 400})
    if not "user_password" in request.json:
        return jsonify({'message': 'No se recibio la contraseña', 'status': 400})
    if not "user_rol" in request.json:
        return jsonify({'message': 'No se recibio el rol', 'status': 400})
    if not "available" in request.json:
        return jsonify({'message': 'No se recibio el estado', 'status': 400})

    # Se verifica que el tipo de dato sea el que corresponde
    user = [user for user in UserData if user['id_user']
        == request.json['id_user']]
    if len(user) == 0:
        return jsonify({'message': 'Usuario no encontrado', 'status': 404})
    if not request.json:
        return jsonify({'message': 'No se recibieron datos', 'status': 400})
    if 'user_name' in request.json and type(request.json['user_name']) is not str:
        return jsonify({'message': 'El nombre debe ser un string', 'status': 400})
    if 'user_nickname' in request.json and type(request.json['user_nickname']) is not str:
        return jsonify({'message': 'El nickname debe ser un string', 'status': 400})
    if 'user_password' in request.json and type(request.json['user_password']) is not str:
        return jsonify({'message': 'La contraseña debe ser un string', 'status': 400})
    if 'user_rol' in request.json and type(request.json['user_rol']) is not str:
        return jsonify({'message': 'El rol debe ser un string', 'status': 400})
    if 'available' in request.json and type(request.json['available']) is not bool:
        return jsonify({'message': 'El estado debe ser un boolean', 'status': 400})

    # Se verifica que el dato no esté vacío
    if request.json['id_user'] == "":
        return jsonify({'message': 'El id no puede estar vacio', 'status': 400})
    if request.json['user_name'] == "":
        return jsonify({'message': 'El nombre no puede estar vacio', 'status': 400})
    if request.json['user_nickname'] == "":
        return jsonify({'message': 'El nickname no puede estar vacio', 'status': 400})
    if request.json['user_password'] == "":
        return jsonify({'message': 'La contraseña no puede estar vacia', 'status': 400})
    if request.json['user_rol'] == "":
        return jsonify({'message': 'El rol no puede estar vacio', 'status': 400})

    if request.json['user_rol'] != "Catedratico" and request.json['user_rol'] != "Estudiante":
        return jsonify({'message': 'El rol debe ser Estudiante o Catedratico', "Rol erróneo": request.json["user_rol"], 'status': 400})

    # Se actualiza el usuario
    user[0]['user_name'] = request.json.get('user_name', user[0]['user_name'])
    user[0]['user_nickname'] = request.json.get(
        'user_nickname', user[0]['user_nickname'])
    user[0]['user_password'] = request.json.get(
        'user_password', user[0]['user_password'])
    user[0]['user_rol'] = request.json.get('user_rol', user[0]['user_rol'])
    user[0]['available'] = request.json.get('available', user[0]['available'])
    return jsonify({'Usuario': user[0], "message": "Actualizado correctamente", 'status': 200})


@app.route("/user", methods=["POST"])
def createUsuario():

    # Validaciones de campos para la creación de usuarios
    if not request.json or not 'id_user' in request.json:
        return jsonify({'message': 'No se recibieron datos', 'status': 400})
    if not "user_name" in request.json:
        return jsonify({'message': 'No se recibio el nombre', 'status': 400})
    if not "user_nickname" in request.json:
        return jsonify({'message': 'No se recibio el nickname', 'status': 400})
    if not "user_password" in request.json:
        return jsonify({'message': 'No se recibio la contraseña', 'status': 400})
    if not "user_rol" in request.json:
        return jsonify({'message': 'No se recibio el rol', 'status': 400})
    if not "available" in request.json:
        return jsonify({'message': 'No se recibio el estado', 'status': 400})
    if request.json['id_user'] in [user['id_user'] for user in UserData]:
        return jsonify({'message': 'El usuario ya existe', 'status': 400})

    # Se verifica que el tipo de dato sea el que corresponde
    if type(request.json['id_user']) is not str:
        return jsonify({'message': 'El id debe ser un string', 'status': 400})
    if type(request.json['user_name']) is not str:
        return jsonify({'message': 'El nombre debe ser un string', 'status': 400})
    if type(request.json['user_nickname']) is not str:
        return jsonify({'message': 'El nickname debe ser un string', 'status': 400})
    if type(request.json['user_password']) is not str:
        return jsonify({'message': 'La contraseña debe ser un string', 'status': 400})
    if type(request.json['user_rol']) is not str:
        return jsonify({'message': 'El rol debe ser un string', 'status': 400})
    if type(request.json['available']) is not bool:
        return jsonify({'message': 'El estado debe ser un boolean', 'status': 400})

    # Se verifica que el dato no esté vacío
    if request.json['id_user'] == "":
        return jsonify({'message': 'El id no puede estar vacio', 'status': 400})
    if request.json['user_name'] == "":
        return jsonify({'message': 'El nombre no puede estar vacio', 'status': 400})
    if request.json['user_nickname'] == "":
        return jsonify({'message': 'El nickname no puede estar vacio', 'status': 400})
    if request.json['user_password'] == "":
        return jsonify({'message': 'La contraseña no puede estar vacia', 'status': 400})
    if request.json['user_rol'] == "":
        return jsonify({'message': 'El rol no puede estar vacio', 'status': 400})

    # Se verifica que el rol sea correcto
    if request.json['user_rol'] != "Catedratico" and request.json['user_rol'] != "Estudiante":
        return jsonify({'message': 'El rol debe ser Estudiante o Catedratico', "Rol erróneo": request.json["rol"], 'status': 400})

    # Se verifica dentro de la lista de usuarios que el id_user no esté repetido
    user = [user for user in UserData if user['id_user']
            == request.json['id_user']]

    # Si la lista devuelve 0, entonces signfiica que el usuairio no existe
    if len(user) == 0:
        # El usuario se inserta en la lista de usuarios
        UserData.append(request.json)
        return jsonify({'Usuario': request.json, 'message': 'Creado correctamente', 'status': 201})
    # Si la lista devuelve mayor a 0, entonces signfiica que el usuairio ya existe
    # Y devuelve un mensaje de error
    return jsonify({'message': 'El usuario ya existe', 'status': 400})

# Endpoints para libros


@app.route("/book", methods=["GET"])
def getLibro():
   
    returnBooks = []
    args = request.args
    if args == {}:
        return jsonify({'Libros': BookData, 'status': 200})
    if not "book_title" in args and not "book_author" in args:
        return jsonify({'message': 'Debe enviar parámetros correctos', 'status': 400})
    
    if "book_title" in args:
        if type(args['book_title']) is not str:
            return jsonify({'message': 'El título debe ser un string', 'status': 400})
        if args['book_title'] == "":
            return jsonify({'message': 'El título no puede estar vacio', 'status': 400})
        for book in BookData:
            if book['book_title'] == args['book_title']:
                returnBooks.append(book)
    if "book_author" in args:
        if type(args['book_author']) is not str:
            return jsonify({'message': 'El autor debe ser un string', 'status': 400})
        if args['book_author'] == "":
            return jsonify({'message': 'El autor no puede estar vacio', 'status': 400})
        for book in BookData:
            if book['book_author'] == args['book_author']:
                returnBooks.append(book)
    return jsonify({'Libros': returnBooks, 'status': 200})
    


@app.route("/book", methods=["PUT"])
def updateLibro():
    # Verificación de datos
    if not request.json or not 'id_book' in request.json:
        return jsonify({'message': 'No se recibieron datos', 'status': 400})
    if not "book_author" in request.json:
        return jsonify({'message': 'No se recibio el autor', 'status': 400})
    if not "book_title" in request.json:
        return jsonify({'message': 'No se recibio el título', 'status': 400})
    if not "book_edition" in request.json:
        return jsonify({'message': 'No se recibio la edición', 'status': 400})
    if not "book_year" in request.json:
        return jsonify({'message': 'No se recibio el año', 'status': 400})
    if not "book_description" in request.json:
        return jsonify({'message': 'No se recibio la descripción', 'status': 400})
    if not "book_available_copies" in request.json:
        return jsonify({'message': 'No se recibio la cantidad de copias disponibles', 'status': 400})
    if not "book_unavailable_copies" in request.json:
        return jsonify({'message': 'No se recibio la cantidad de copias no disponibles', 'status': 400})
    if not "book_copies" in request.json:
        return jsonify({'message': 'No se recibio la cantidad de copias', 'status': 400})

    # Se verifica el tipo de dato de los campos
    book = [book for book in BookData if book['id_book'] == request.json['id_book']]
    if len(book) == 0:
        return jsonify({'message': 'Libro no encontrado', 'status': 404})
    if not request.json:
        return jsonify({'message': 'No se recibieron datos', 'status': 400})
    if 'book_author' in request.json and type(request.json['book_author']) is not str:
        return jsonify({'message': 'El autor debe ser un string', 'status': 400})
    if 'book_title' in request.json and type(request.json['book_title']) is not str:
        return jsonify({'message': 'El título debe ser un string', 'status': 400})
    if 'book_edition' in request.json and type(request.json['book_edition']) is not int:
        return jsonify({'message': 'La edición debe ser un entero', 'status': 400})
    if 'book_editorial' in request.json and type(request.json['book_editorial']) is not str:
        return jsonify({'message': 'La editorial debe ser un string', 'status': 400})
    if 'book_year' in request.json and type(request.json['book_year']) is not int:
        return jsonify({'message': 'El año debe ser un entero', 'status': 400})
    if 'book_description' in request.json and type(request.json['book_description']) is not str:
        return jsonify({'message': 'La descripción debe ser un string', 'status': 400})
    if 'book_available_copies' in request.json and type(request.json['book_available_copies']) is not int:
        return jsonify({'message': 'Las copias disponibles deben ser un entero', 'status': 400})
    if 'book_unavailable_copies' in request.json and type(request.json['book_unavailable_copies']) is not int:
        return jsonify({'message': 'Las copias no disponibles deben ser un entero', 'status': 400})
    if 'book_copies' in request.json and type(request.json['book_copies']) is not int:
        return jsonify({'message': 'El estado debe ser un entero', 'status': 400})

    # Se actualiza el libro
    book[0]['book_author'] = request.json.get(
        'book_author', book[0]['book_author'])
    book[0]['book_title'] = request.json.get(
        'book_title', book[0]['book_title'])
    book[0]['book_edition'] = request.json.get(
        'book_edition', book[0]['book_edition'])
    book[0]['book_editorial'] = request.json.get(
        'book_editorial', book[0]['book_editorial'])
    book[0]['book_year'] = request.json.get('book_year', book[0]['book_year'])
    book[0]['book_description'] = request.json.get(
        'book_description', book[0]['book_description'])
    book[0]['book_available_copies'] = request.json.get(
        'book_available_copies', book[0]['book_available_copies'])
    book[0]['book_unavailable_copies'] = request.json.get(
        'book_unavailable_copies', book[0]['book_unavailable_copies'])
    book[0]['book_copies'] = request.json.get(
        'book_copies', book[0]['book_copies'])

    # Se retorna un mensaje de éxito
    return jsonify({'Libro': book[0], "message": "Actualizado correctamente", 'status': 200})


@app.route("/book", methods=["POST"])
def createLibro():
    allDataBooksRequest = {}
    countBook = 1
    stateDataBook = []
    listBooksNotCreated = {}
    listBooksCreated = {}

    bookNotCreated = {}
    bookCreated = {}
    causa = ""

    for book in request.json:
        # Verificación de datos
        if not "id_book" in book:
            causa = "No se recibio el id del libro"
        if not 'book_author' in book:
            causa = "No se recibió al autor"
        if not "book_title" in book:
            causa = "No se recibio el título"
        if not "book_edition" in book:
            causa = "No se recibio la edición"
        if not "book_year" in book:
            causa = "No se recibio el año"
        if not "book_description" in book:
            causa = "No se recibio la descripción"
        if not "book_available_copies" in book:
            causa = "No se recibio la cantidad de copias disponibles"
        if not "book_unavailable_copies" in book:
            causa = "No se recibio la cantidad de copias no disponibles"
        if not "book_copies" in book:
            causa = "No se recibio la cantidad de copias"

        if causa != "":
            print("la causa es "+causa)
            bookNotCreated = {
                "book": book,
                "causa": causa
            }
            listBooksNotCreated["book"+str(countBook)] = bookNotCreated

        # Se verifica el tipo de dato de los campos
        if "id_book" in book and type(book['id_book']) is not str:
            causa = "El id debe ser un string"
        if 'book_author' in book and type(book['book_author']) is not str:
            causa = "El autor debe ser un string"
        if 'book_title' in book and type(book['book_title']) is not str:
            causa = "El título debe ser un string"
        if 'book_edition' in book and type(book['book_edition']) is not int:
            causa = "La edición debe ser un entero"
        if 'book_editorial' in book and type(book['book_editorial']) is not str:
            causa = "La editorial debe ser un string"
        if 'book_year' in book and type(book['book_year']) is not int:
            causa = "El año debe ser un entero"
        if 'book_description' in book and type(book['book_description']) is not str:
            causa = "La descripción debe ser un string"
        if 'book_available_copies' in book and type(book['book_available_copies']) is not int:
            causa = "Las copias disponibles deben ser un entero"
        if 'book_unavailable_copies' in book and type(book['book_unavailable_copies']) is not int:
            causa = "Las copias no disponibles deben ser un entero"
        if 'book_copies' in book and type(book['book_copies']) is not int:
            return jsonify({'message': 'El estado debe ser un entero', 'status': 400})
        if causa != "":
            print("la causa es "+causa)
            bookNotCreated = {
                "book": book,
                "causa": causa
            }
            listBooksNotCreated["book"+str(countBook)] = bookNotCreated

        # Se verifica que el libro no exista
        if causa == "":
            bookVerified = [bookVerified for bookVerified in BookData if bookVerified['id_book']
                            == book['id_book']]
            if len(bookVerified) == 0:
                bookCreated = {
                    "book": book,
                    "status": 200
                }
                listBooksCreated["book"+str(countBook)] = bookCreated
                BookData.append(book)
            else:
                bookNotCreated = {
                    "book": book,
                    "causa": "El libro ya existe"
                }
                listBooksNotCreated["book"+str(countBook)] = bookNotCreated

        countBook += 1

    allDataBooksRequest["Libros creados"] = listBooksCreated
    allDataBooksRequest["Libros no creados"] = listBooksNotCreated
    stateDataBook.append(allDataBooksRequest)

    return jsonify(stateDataBook)


@app.route("/book/<string:id>", methods=["DELETE"])
def deleteLibro(id):
    book = [book for book in BookData if book['id_book'] == id]
    if len(book) == 0:
        return jsonify({'message': 'Libro no encontrado', 'status': 404})
    BookData.remove(book[0])
    return jsonify({'message': 'Libro eliminado correctamente', 'status': 200})

# Rutas para prestamos


@app.route("/borrow", methods=["POST"])
def createBorrow():
    borrow = request.json

    # Se verifica que exista el campo de usuario y el libro
    if not "id_book" in borrow:
        return jsonify({'message': 'No se recibió el id del libro', 'status': 400})
    if not "id_user" in borrow:
        return jsonify({'message': 'No se recibió el id del usuario', 'status': 400})

    # Se verifica que el libro exista
    book = [book for book in BookData if book['id_book'] == borrow['id_book']]
    if len(book) == 0:
        return jsonify({'message': 'Libro no encontrado', 'status': 404})

    # Se verifica que el usuario exista
    user = [user for user in UserData if user['id_user'] == borrow["id_user"]]
    if len(user) == 0:
        return jsonify({'message': 'El usuario no existe', 'status': 404})

    if user[0]["available"] != True:
        return jsonify({'message': 'El usuario no esta disponible', 'status': 400})

    if book[0]["book_available_copies"] == 0:
        return jsonify({'message': 'No hay copias disponibles', 'status': 400})

    # Se actualizan los valores de la cantidad disponibles del prestamo
    book[0]["book_available_copies"] -= 1
    book[0]["book_unavailable_copies"] += 1

    # Se crea el prestamo
    borrow = {
        "id_borrow": len((BorrowData))+1,
        "borrow_date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "returned": False,
        "id_book": borrow['id_book'],
        "borrow_book": book[0],
    }
    BorrowData.append(borrow)
    return jsonify(borrow)


@app.route("/borrow/<string:id>", methods=["GET"])
def getPrestamo(id):
    borrow = [borrow for borrow in BorrowData if borrow['id_borrow'] == int(id)]
    if len(borrow) == 0:
        return jsonify({'message': 'Prestamo no encontrado', 'status': 404})
    return jsonify(borrow[0])


@app.route("/borrow/<string:id_borrow>", methods=["PUT"])
def returnPrestamo(id_borrow):

    if id_borrow == "":
        return jsonify({'message': 'No se recibió el id del prestamo', 'status': 400})
    print(id_borrow)

    # Se verifica que el prestamo exista
    borrow = [borrow for borrow in BorrowData if borrow['id_borrow'] == int(id_borrow)]
    if len(borrow) == 0:
        return jsonify({'message': 'Prestamo no encontrado', 'status': 404})
    
    if borrow[0]["returned"] == True:
        return jsonify({'message': 'El prestamo ya fue devuelto', 'status': 400})

    book = [book for book in BookData if book['id_book'] == borrow[0]["id_book"]]
    
    book[0]["book_available_copies"] += 1
    book[0]["book_unavailable_copies"] -= 1

    borrow[0]["returned"] = True

    return jsonify({'message': 'Prestamo devuelto correctamente', "Borrow": borrow[0], 'status': 200})

# Reporte
@app.route("/report", methods=["GET"])
def report():
    if not request:
        return jsonify({'message': 'No se recibió ningún reporte', 'status': 400})
    report = {
        "Cantidad de Libros": len(BookData),
        "Cantidad de Usuarios": len(UserData),
        "Cantidad de Préstamos no devueltos": len([borrow for borrow in BorrowData if borrow['returned'] == False]),
        "Cantidad de Préstamos devueltos": len([borrow for borrow in BorrowData if borrow['returned'] == True]),
    }
    return jsonify(report)

if __name__ == "__main__":
    app.run(debug=True)