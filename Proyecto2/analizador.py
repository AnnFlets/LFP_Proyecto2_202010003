from lectura_escritura.funcion import Funcion
from lectura_escritura.escritor_traduccion import EscritorTraduccion
from lectura_escritura.escritor_errores import EscritorErrores
from lectura_escritura.escritor_tokens import EscritorTokens
from lectura_escritura.error import Error

class Analizador():

    def __init__(self, lineas):
        self.lineas = lineas
        self.fila = 0
        self.columna = 0
        self.index = 0
        self.funciones = ["CrearBD", "EliminarBD", "CrearColeccion", "EliminarColeccion",
                          "InsertarUnico", "ActualizarUnico", "EliminarUnico",
                          "BuscarTodo", "BuscarUnico"]
        self.funcion = ""
        self.funcion_leida = None
        self.lista_funciones = []
        self.lista_errores = []

    """
    Método que recibirá el token a buscar, y los estados actual y siguiente.
    Ignora los espacios y cuando encuentre el primer caracter, texto tomará
    el valor retornado por juntar_caracteres. Luego condiciona el valor retornado
    por el método analizar_coincidencia, si es verdadero, se pasa al estado
    siguiente; en el caso contrario, se devuelve la palabra "ERROR" por no 
    coincidir el token con la palabra encontrada en el archivo.
    """
    def verificar_token(self, token, estado_actual, estado_siguiente):
        if self.lineas[self.index] != " ":
            # Palabra encontrada en el archivo
            texto = self.juntar_caracteres(self.index, len(token))
            # Si la palabra coincide con el token esperado
            if self.analizar_coincidencia(token, texto):
                self.index += len(token) - 1
                self.columna += len(token) - 1
                return estado_siguiente
            else:
                self.guardar_error("Lexico", token, texto)
                return "ERROR"
        else:
            return estado_actual

    """
    Método que recibe un inicio y fin para concatenar los caracteres del archivo leído
    posicionados dentro de ese rango. Se retorna la palabra unificada.
    """
    def juntar_caracteres(self, inicio, fin):
        try:
            token_unificado = ""
            for caracter in range(inicio, inicio + fin):
                token_unificado += self.lineas[caracter]
            return token_unificado
        except:
            return None

    """
    Método que recibe el token y el texto a comparar. Comprueba, caracter a caracter,
    que el texto sea igual al token esperado; si no coincide en algún caracter, se
    retorna False; y si todos los caracteres coinciden, se devuelve True.
    """
    def analizar_coincidencia(self, token, texto):
        try:
            posicion = 0
            token_temporal = ""
            for caracter in texto:
                if str(caracter) == str(token[posicion]):
                    token_temporal += caracter
                    posicion += 1
                else:
                    return False
            print(f'********** ENCONTRE - {token_temporal} ***************')
            return True
        except:
            return False

    def verificar_id(self, estado_siguiente):
        estado_actual = "I0"
        estado_siguiente = estado_siguiente
        id = ""
        while self.lineas[self.index] != "":
            # Casos en los cuales se debe salir de la verificación de id
            if str(self.lineas[self.index]) == " " and id != "":
                self.index -= 1
                return [estado_siguiente, id]

            # Casos en los cuales se debe salir de la verificación de id
            elif str(self.lineas[self.index]) == "\n" and id != "":
                self.fila += 1
                self.columna = 0
                self.index -= 1
                return [estado_siguiente, id]

            # Casos en los cuales se debe salir de la verificación de id
            elif str(self.lineas[self.index]) == "\"":
                self.index -= 1
                return [estado_siguiente, id]

            # I0 -> CARACTER I1
            elif estado_actual == "I0":
                if self.lineas[self.index] != " ":
                    id += self.lineas[self.index]
                    estado_actual = "I1"

            # I1 -> CARACTER I1
            elif estado_actual == "I1":
                if self.lineas[self.index] != " ":
                    id += self.lineas[self.index]
                    estado_actual = "I1"
                else:
                    estado_actual = "ERROR"

            if estado_actual == "ERROR":
                return ["ERROR", None]

            if self.index < len(self.lineas) - 1:
                self.index += 1
                self.columna += 1
            else:
                break

    def verificar_cadena(self, estado_siguiente):
        estado_actual = "K0"
        estado_siguiente = estado_siguiente
        cadena = ""
        while self.lineas[self.index] != "":
            # Caso de salida de la verificación de cadena
            if str(self.lineas[self.index]) == "\"":
                self.index -= 1
                return [estado_siguiente, cadena]

            # K0 -> CARACTER K1
            elif estado_actual == "K0":
                cadena += self.lineas[self.index]
                estado_actual = "K1"

            # K1 -> CARACTER K1
            elif estado_actual == "K1":
                if self.lineas[self.index] != "\n":
                    cadena += self.lineas[self.index]
                    estado_actual = "K1"
                else:
                    self.fila += 1
                    self.columna = 0
                    estado_actual = "ERROR"

            if estado_actual == "ERROR":
                return ["ERROR", None]

            if self.index < len(self.lineas) - 1:
                self.index += 1
                self.columna += 1
            else:
                break

    """
    ESTRUCTURA:
    COMENTARIO DE UNA LINEA -> - . - . - . (CARACTER)*
    """
    def comentario_linea(self, estado_siguiente):
        estado_actual = "C0"
        estado_siguiente = estado_siguiente
        comentario = ""
        while self.lineas[self.index] != "":
            # Casos en los cuales se debe salir del comentario de línea
            if str(self.lineas[self.index]) == "\n":
                self.fila += 1
                self.columna = 0
                self.index -= 1
                return [estado_siguiente, comentario]

            # C0 -> - C1
            elif estado_actual == "C0":
                estado_actual = self.verificar_token("-", "C0", "C1")

            # C1 -> - C2
            elif estado_actual == "C1":
                estado_actual = self.verificar_token("-", "C1", "C2")

            # C2 -> - C3
            elif estado_actual == "C2":
                estado_actual = self.verificar_token("-", "C2", "C3")

            # C3 -> CARACTER C3
            # C3 -> C4
            elif estado_actual == "C3":
                if self.lineas[self.index + 1] != "\n":
                    comentario += self.lineas[self.index]
                    estado_actual = "C3"
                else:
                    comentario += self.lineas[self.index]
                    print(f'********** ENCONTRE - {comentario} ***************')
                    estado_actual = "C4"

            # C4 -> ESTADO DE ACEPTACIÓN
            elif estado_actual == "C4":
                return [estado_siguiente, comentario]

            if estado_actual == "ERROR":
                return ["ERROR", None]

            if self.index < len(self.lineas) - 1:
                self.index += 1
                self.columna += 1
            else:
                break

    """
    ESTRUCTURA:
    COMENTARIO DE VARIAS LINEAS -> / . * . (CARACTER)* . * . /
    """
    def comentario_varias_lineas(self, estado_siguiente):
        estado_actual = "Q0"
        estado_siguiente = estado_siguiente
        comentario = ""
        while self.lineas[self.index] != "":
            if str(self.lineas[self.index]) == "\n":
                self.fila += 1
                self.columna = 0

            # Q0 -> / Q1
            if estado_actual == "Q0":
                estado_actual = self.verificar_token("/", "Q0", "Q1")

            # Q1 -> * Q2
            elif estado_actual == "Q1":
                estado_actual = self.verificar_token("*", "Q1", "Q2")

            # Q2 -> CARACTER Q2
            # Q2 -> * Q3
            elif estado_actual == "Q2":
                if self.lineas[self.index] != "*" and self.lineas[self.index + 1] != "/":
                    comentario += self.lineas[self.index]
                    estado_actual = "Q2"
                else:
                    print(f'********** ENCONTRE - {comentario} ***************')
                    estado_actual = self.verificar_token("*", "Q2", "Q3")

            # Q3 -> / Q4
            elif estado_actual == "Q3":
                estado_actual = self.verificar_token("/", "Q3", "Q4")

            # Q4 -> ESTADO DE ACEPTACIÓN
            elif estado_actual == "Q4":
                return [estado_siguiente, comentario]

            if estado_actual == "ERROR":
                return ["ERROR", None]

            if self.index < len(self.lineas) - 1:
                self.index += 1
                self.columna += 1
            else:
                break

    """
    ESTRUCTURA:
    JSON -> { . DATOS . (, . DATOS  )*  . } . ( , . { . $set . : . { . DATOS . } . } )?
    """
    def json(self, estado_siguiente):
        estado_actual = "J0"
        estado_siguiente = estado_siguiente
        json = []
        set = ""
        datos = ""
        while self.lineas[self.index] != "":
            if str(self.lineas[self.index]) == "\n":
                self.fila += 1
                self.columna = 0

            # J0 -> { J1
            elif estado_actual == "J0":
                estado_actual = self.verificar_token("{", "J0", "J1")

            # J1 -> DATOS J2
            elif estado_actual == "J1":
                arreglo = self.datos("J2")
                if arreglo[0] == "ERROR":
                    estado_actual = "ERROR"
                elif arreglo[0] == "J2":
                    print(f'********** ENCONTRE - {arreglo[1]} ***************')
                    json.append(str(arreglo[1]))
                    estado_actual = "J2"

            # J2 -> , J3
            # J2 -> } J4
            elif estado_actual == "J2":
                if self.lineas[self.index] != " " or self.lineas[self.index] != "\n":
                    if self.lineas[self.index] == ",":
                        estado_actual = self.verificar_token(",", "J2", "J3")
                    else:
                        estado_actual = self.verificar_token("}", "J2", "J4")

            # J3 -> DATOS J2
            elif estado_actual == "J3":
                arreglo = self.datos("J2")
                if arreglo[0] == "ERROR":
                    estado_actual = "ERROR"
                elif arreglo[0] == "J2":
                    print(f'********** ENCONTRE - {arreglo[1]} ***************')
                    json.append(str(arreglo[1]))
                    estado_actual = "J2"

            # J4 -> , J5
            # J4 -> J12
            elif estado_actual == "J4":
                if self.lineas[self.index] != " " or self.lineas[self.index] != "\n":
                    if self.lineas[self.index] == ",":
                        estado_actual = self.verificar_token(",", "J4", "J5")
                    else:
                        estado_actual = "J12"

            # J5 -> { J6
            elif estado_actual == "J5":
                estado_actual = self.verificar_token("{", "J5", "J6")

            # J6 -> $set J7
            elif estado_actual == "J6":
                estado_actual = self.verificar_token("$set", "J6", "J7")

            # J7 -> : J8
            elif estado_actual == "J7":
                estado_actual = self.verificar_token(":", "J7", "J8")

            # J8 -> { J9
            elif estado_actual == "J8":
                estado_actual = self.verificar_token("{", "J8", "J9")

            # J9 -> DATOS J10
            elif estado_actual == "J9":
                arreglo = self.datos("J10")
                if arreglo[0] == "ERROR":
                    estado_actual = "ERROR"
                elif arreglo[0] == "J10":
                    print(f'********** ENCONTRE - {arreglo[1]} ***************')
                    set += arreglo[1]
                    estado_actual = "J10"

            # J10 -> } J11
            elif estado_actual == "J10":
                estado_actual = self.verificar_token("}", "J10", "J11")

            # J11 -> } J12
            elif estado_actual == "J11":
                estado_actual = self.verificar_token("}", "J11", "J12")

            # J12 -> ESTADO DE ACEPTACION
            if estado_actual == "J12":
                datos += "{"
                contador = 1
                for dato in json:
                    if contador != len(json):
                        datos += dato + ","
                    else:
                        datos += dato
                    contador += 1
                datos += "}"
                if set != "":
                    datos += ",{$set:{"+ set + "}}"
                return [estado_siguiente, datos]

            if estado_actual == "ERROR":
                return ["ERROR", None]

            if self.index < len(self.lineas) - 1:
                self.index += 1
                self.columna += 1
            else:
                break

    """
    ESTRUCTURA:
    DATOS -> " . ID . " . : . " . CADENA . "
    """
    def datos(self, estado_siguiente):
        estado_actual = "D0"
        estado_siguiente = estado_siguiente
        id = ""
        valor = ""
        dato = ""
        while self.lineas[self.index] != "":
            # D0 -> " D1
            if estado_actual == "D0":
                estado_actual = self.verificar_token("\"", "D0", "D1")

            # D1 -> ID D2
            elif estado_actual == "D1":
                arreglo = self.verificar_id("D2")
                if arreglo[0] == "ERROR":
                    estado_actual = "ERROR"
                elif arreglo[0] == "D2":
                    print(f'********** ENCONTRE - {arreglo[1]} ***************')
                    id = arreglo[1]
                    estado_actual = "D2"

            # D2 -> " D3
            elif estado_actual == "D2":
                estado_actual = self.verificar_token("\"", "D2", "D3")

            # D3 -> : D4
            elif estado_actual == "D3":
                estado_actual = self.verificar_token(":", "D3", "D4")

            # D4 -> " D5
            elif estado_actual == "D4":
                estado_actual = self.verificar_token("\"", "D4", "D5")

            # D5 -> CADENA D6
            elif estado_actual == "D5":
                arreglo = self.verificar_cadena("D6")
                if arreglo[0] == "ERROR":
                    estado_actual = "ERROR"
                elif arreglo[0] == "D6":
                    print(f'********** ENCONTRE - {arreglo[1]} ***************')
                    valor = arreglo[1]
                    estado_actual = "D6"

            # D6 -> " D7
            elif estado_actual == "D6":
                estado_actual = self.verificar_token("\"", "D6", "D7")

            # D7 -> ESTADO DE ACEPTACION
            if estado_actual == "D7":
                dato += "\"" + id + "\":\"" + valor + "\""
                return [estado_siguiente, dato]

            if estado_actual == "ERROR":
                return ["ERROR", None]

            if self.index < len(self.lineas) - 1:
                self.index += 1
                self.columna += 1
            else:
                break

    """
    ESTRUCTURA:
    PARAMETROS -> " . (ID)? . " . (, . ". JSON . ")?
    """
    def parametros(self, estado_siguiente):
        estado_actual = "P0"
        estado_siguiente = estado_siguiente
        id = ""
        json = ""
        while self.lineas[self.index] != "":
            if str(self.lineas[self.index]) == "\n":
                self.fila += 1
                self.columna = 0

            # P0 -> " P1
            elif estado_actual == "P0":
                estado_actual = self.verificar_token("\"", "P0", "P1")

            # P1 -> ID P2
            # P1 -> " P3
            elif estado_actual == "P1":
                if self.lineas[self.index] == "\"":
                    estado_actual = self.verificar_token("\"", "P1", "P3")
                else:
                    arreglo = self.verificar_id("P2")
                    if arreglo[0] == "ERROR":
                        estado_actual = "ERROR"
                    elif arreglo[0] == "P2":
                        id = arreglo[1]
                        print(f'********** ENCONTRE - {arreglo[1]} ***************')
                        estado_actual = "P2"

            # P2 -> " P3
            elif estado_actual == "P2":
                estado_actual = self.verificar_token("\"", "P2", "P3")

            # P3 -> , P4
            # P3 -> P7
            elif estado_actual == "P3":
                if self.funcion == "CrearColeccion" or self.funcion == "EliminarColeccion"\
                        or self.funcion == "BuscarTodo" or self.funcion == "BuscarUnico":
                    self.index -= 1
                    estado_actual = "P7"
                elif self.lineas[self.index] == ",":
                    estado_actual = self.verificar_token(",", "P3", "P4")

            # P4 -> " P5
            elif estado_actual == "P4":
                estado_actual = self.verificar_token("\"", "P4", "P5")

            # P5 -> JSON P6
            elif estado_actual == "P5":
                arreglo = self.json("P6")
                if arreglo[0] == "ERROR":
                    estado_actual = "ERROR"
                elif arreglo[0] == "P6":
                    json = str(arreglo[1])
                    print(f'********** ENCONTRE - {arreglo[1]} ***************')
                    if self.funcion == "EliminarUnico" or self.funcion == "InsertarUnico":
                        self.index -= 1
                    estado_actual = "P6"

            # P6 -> " P7
            elif estado_actual == "P6":
                estado_actual = self.verificar_token("\"", "P6", "P7")

            # P7 -> ESTADO DE ACEPTACION
            if estado_actual == "P7":
                return [estado_siguiente, [id, json]]

            if estado_actual == "ERROR":
                return ["ERROR", None]

            if self.index < len(self.lineas) - 1:
                self.index += 1
                self.columna += 1
            else:
                break

    """
    ESTRUCTURA:
    FUNCIONES -> FUNCION . ID . = . nueva . FUNCION . ( . (PARAMETROS)? . ) . ;
    """
    def compilar(self):
        estado_actual = "S0"
        while self.lineas[self.index] != "":
            # Si el caracter leído es un salto de línea,
            # entonces se aumenta 1 a fila y se reinicia la columna a 0
            if self.lineas[self.index] == "\n":
                self.fila += 1
                self.columna = 0

            # S0 -> FUNCION S1
            elif estado_actual == "S0":
                if self.lineas[self.index] == "-":
                    arreglo = self.comentario_linea("S0")
                    estado_actual = arreglo[0]
                elif self.lineas[self.index] == "/" and self.lineas[self.index + 1] == "*":
                    arreglo = self.comentario_varias_lineas("S0")
                    estado_actual = arreglo[0]
                else:
                    estado_actual = "ERROR"
                    for funcion in self.funciones:
                        estado_actual = self.verificar_token(funcion, "S0", "S1")
                        if estado_actual != "ERROR":
                            self.funcion = funcion
                            break

            # S1 -> ID S2
            elif estado_actual == "S1":
                arreglo = self.verificar_id("S2")
                if arreglo[0] == "ERROR":
                    estado_actual = "ERROR"
                elif arreglo[0] == "S2":
                    print(f'********** ENCONTRE - {arreglo[1]} ***************')
                    self.funcion_leida = Funcion(self.funcion, arreglo[1])
                    estado_actual = "S2"

            # S2 -> = S3
            elif estado_actual == "S2":
                estado_actual = self.verificar_token("=", "S2", "S3")

            # S3 -> nueva S4
            elif estado_actual == "S3":
                estado_actual = self.verificar_token("nueva", "S3", "S4")

            # S4 -> FUNCION S5
            elif estado_actual == "S4":
                estado_actual = "ERROR"
                for funcion in self.funciones:
                    estado_actual = self.verificar_token(funcion, "S4", "S5")
                    if estado_actual != "ERROR" and self.funcion == funcion:
                        break

            # S5 -> ( S6
            elif estado_actual == "S5":
                estado_actual = self.verificar_token("(", "S5", "S6")

            # S6 -> PARAMETROS S7
            # S6 -> ) S8
            elif estado_actual == "S6":
                if self.funcion == "CrearBD" or self.funcion == "EliminarBD":
                    estado_actual = self.verificar_token(")", "S6", "S8")
                else:
                    arreglo = self.parametros("S7")
                    if arreglo[0] == "ERROR":
                        estado_actual = "ERROR"
                    elif arreglo[0] == "S7":
                        self.funcion_leida.set_parametros(arreglo[1])
                        estado_actual = "S7"

            # S7 -> ) S8
            elif estado_actual == "S7":
                estado_actual = self.verificar_token(")", "S7", "S8")

            #S8 -> ; S9
            elif estado_actual == "S8":
                estado_actual = self.verificar_token(";", "S8", "S9")

            #S9 -> ESTADO DE ACEPTACIÓN
            if estado_actual == "S9":
                print("Cadena leída")
                self.lista_funciones.append(self.funcion_leida)
                estado_actual = "S0"

            if estado_actual == "ERROR":
                estado_actual = "S0"

            if self.index < len(self.lineas) - 1:
                self.index += 1
                self.columna += 1
            else:
                print(self.lista_funciones)
                escribir_funciones = EscritorTraduccion(self.lista_funciones)
                escribir_funciones.escribir_funcion()
                escribir_errores = EscritorErrores(self.lista_errores)
                escribir_errores.escribir_errores()
                escribir_tokens = EscritorTokens(self.lista_funciones)
                escribir_tokens.escribir_tokens()
                break

    def guardar_error(self, tipo, token, texto):
        tipo = tipo
        token_esperado = token
        descripcion = texto.replace("\n", "")
        error = Error(tipo, token_esperado, descripcion, self.fila, self.columna)
        self.lista_errores.append(error)