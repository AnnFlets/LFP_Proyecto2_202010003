class EscritorTraduccion():

    def __init__(self, lista_funciones):
        self.lista_funciones = lista_funciones

    def escribir_funcion(self):
        archivo = open("resultados\TRADUCCION_202010003.txt", "w+")
        texto = ""
        for funcion in self.lista_funciones:
            if funcion.parametros != None:
                funcion.set_id()
                funcion.set_json()
            if funcion.tipo == "CrearBD":
                texto += "use(\'" + str(funcion.nombre) + "\');\n"
            elif funcion.tipo == "EliminarBD":
                texto += "db.dropDatabase();\n"
            elif funcion.tipo == "CrearColeccion":
                texto += "db.createCollection(\'" + str(funcion.id) + "\');\n"
            elif funcion.tipo == "EliminarColeccion":
                texto += "db." + str(funcion.id) + ".drop();\n"
            elif funcion.tipo == "InsertarUnico":
                texto += "db." + str(funcion.id) + ".insertOne(" + str(funcion.json) + ");\n"
            elif funcion.tipo == "ActualizarUnico":
                texto += "db." + str(funcion.id) + ".updateOne(" + str(funcion.json) + ");\n"
            elif funcion.tipo == "EliminarUnico":
                texto += "db." + str(funcion.id) + ".deleteOne(" + str(funcion.json) + ");\n"
            elif funcion.tipo == "BuscarTodo":
                texto += "db." + str(funcion.id) + ".find();\n"
            elif funcion.tipo == "BuscarUnico":
                texto += "db." + str(funcion.id) + ".findOne();\n"
        archivo.write(texto)
        archivo.close()