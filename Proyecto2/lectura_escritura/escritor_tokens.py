class EscritorTokens():

    def __init__(self, lista_funciones):
        self.lista_funciones = lista_funciones

    def escribir_tokens(self):
        archivo = open("resultados\TOKENS_202010003.html", "w+")
        texto_escribir = "<!DOCTYPE html>\n"
        texto_escribir += "<html lang=\"es\">\n"
        texto_escribir += "<head>\n"
        texto_escribir += "\t<title>Tokens</title>\n"
        texto_escribir += "\t<meta charset=\"utf-8\">\n"
        texto_escribir += "</head>\n"
        texto_escribir += "<body>\n"
        texto_escribir += "\t<h1>TABLA DE TOKENS</h1>\n"
        texto_escribir += "\t<br>\n"
        texto_escribir += "\t<table border=\"1\">\n"
        texto_escribir += "\t<tr>\n"
        texto_escribir += "\t\t<td>No.</td>\n"
        texto_escribir += "\t\t<td>Token</td>\n"
        texto_escribir += "\t\t<td>Lexema</td>\n"
        texto_escribir += "\t</tr>\n"
        for funcion in self.lista_funciones:
            if funcion.parametros != None:
                funcion.set_id()
                funcion.set_json()
            numero, token = self.comprobar_tokens(funcion.tipo)
            texto_escribir += "\t<tr>\n"
            texto_escribir += "\t\t<td>" + str(numero) + "</td>\n"
            texto_escribir += "\t\t<td>" + str(token) + "</td>\n"
            texto_escribir += "\t\t<td>" + str(funcion.tipo) + "</td>\n"
            texto_escribir += "\t</tr>\n"
            texto_escribir += self.agregar_tokens(funcion)
        texto_escribir += "</table>\n"
        texto_escribir += "</body>\n"
        texto_escribir += "</html>\n"
        archivo.write(texto_escribir)
        archivo.close()

    def agregar_json(self, funcion):
        texto_datos = ""
        texto_id = []
        texto = ""
        texto_escribir = ""
        if funcion.json != None:
            texto = funcion.json.replace("{", "")
            texto = texto.replace("}", "")
            texto_datos += texto
            texto_id = texto_datos.split("\"")
            texto_id.remove("")
            if len(texto_id) > 1:
                texto_id.pop()
            try:
                posicion = texto_id.index(",$set:")
            except:
                posicion = -1
            if posicion != -1:
                texto_id.pop(posicion + 3)
                texto_id.pop(posicion + 2)
                texto_id.pop(posicion + 1)
                texto_id.pop(posicion)
        for valor in texto_id:
            if valor != ":" and valor != ",":
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>17</td>\n"
                texto_escribir += "\t\t<td>Tk_ComillaD</td>\n"
                texto_escribir += "\t\t<td>\"</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>11</td>\n"
                texto_escribir += "\t\t<td>Tk_ID</td>\n"
                texto_escribir += "\t\t<td>" + str(valor) + "</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>17</td>\n"
                texto_escribir += "\t\t<td>Tk_ComillaD</td>\n"
                texto_escribir += "\t\t<td>\"</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
            elif valor == ",":
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>18</td>\n"
                texto_escribir += "\t\t<td>Tk_Coma</td>\n"
                texto_escribir += "\t\t<td>,</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
            elif valor == ":":
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>21</td>\n"
                texto_escribir += "\t\t<td>Tk_DosPts</td>\n"
                texto_escribir += "\t\t<td>:</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
        return texto_escribir

    def agregar_set(self, funcion):
        texto_datos = ""
        texto_id = []
        arreglo = []
        texto = ""
        texto_escribir = ""
        if funcion.json != None:
            texto = funcion.json.replace("{", "")
            texto = texto.replace("}", "")
            texto_datos += texto
            texto_id = texto_datos.split("\"")
            texto_id.remove("")
            if len(texto_id) > 1:
                texto_id.pop()
            try:
                posicion = texto_id.index(",$set:")
            except:
                posicion = -1
            if posicion != -1:
                arreglo.append(texto_id[posicion + 1])
                arreglo.append(texto_id[posicion + 2])
                arreglo.append(texto_id[posicion + 3])
        for valor in arreglo:
            if valor != ":":
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>17</td>\n"
                texto_escribir += "\t\t<td>Tk_ComillaD</td>\n"
                texto_escribir += "\t\t<td>\"</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>11</td>\n"
                texto_escribir += "\t\t<td>Tk_ID</td>\n"
                texto_escribir += "\t\t<td>" + str(valor) + "</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>17</td>\n"
                texto_escribir += "\t\t<td>Tk_ComillaD</td>\n"
                texto_escribir += "\t\t<td>\"</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
            elif valor == ":":
                texto_escribir += "\t<tr>\n"
                texto_escribir += "\t\t<td>21</td>\n"
                texto_escribir += "\t\t<td>Tk_DosPts</td>\n"
                texto_escribir += "\t\t<td>:</td>\n"
                texto_escribir += "\t</tr>\n"
                texto_escribir += "\t<tr>\n"
        return texto_escribir

    def agregar_tokens(self, funcion):
        texto = ""
        texto += "\t<tr>\n"
        texto += "\t\t<td>11</td>\n"
        texto += "\t\t<td>Tk_ID</td>\n"
        texto += "\t\t<td>" + str(funcion.nombre) + "</td>\n"
        texto += "\t</tr>\n"
        texto += "\t<tr>\n"
        texto += "\t\t<td>12</td>\n"
        texto += "\t\t<td>Tk_Igual</td>\n"
        texto += "\t\t<td>=</td>\n"
        texto += "\t</tr>\n"
        texto += "\t<tr>\n"
        texto += "\t\t<td>13</td>\n"
        texto += "\t\t<td>Tk_Nueva</td>\n"
        texto += "\t\t<td>nueva</td>\n"
        texto += "\t</tr>\n"
        texto += "\t<tr>\n"
        texto += "\t\t<td>14</td>\n"
        texto += "\t\t<td>Tk_ParA</td>\n"
        texto += "\t\t<td>(</td>\n"
        texto += "\t</tr>\n"
        if funcion.id != None:
            texto += "\t<tr>\n"
            texto += "\t\t<td>17</td>\n"
            texto += "\t\t<td>Tk_ComillaD</td>\n"
            texto += "\t\t<td>\"</td>\n"
            texto += "\t</tr>\n"
            texto += "\t<tr>\n"
            texto += "\t\t<td>11</td>\n"
            texto += "\t\t<td>Tk_ID</td>\n"
            texto += "\t\t<td>" + str(funcion.id) + "</td>\n"
            texto += "\t</tr>\n"
            texto += "\t<tr>\n"
            texto += "\t\t<td>17</td>\n"
            texto += "\t\t<td>Tk_ComillaD</td>\n"
            texto += "\t\t<td>\"</td>\n"
            texto += "\t</tr>\n"
        if funcion.tipo == "InsertarUnico" or \
                funcion.tipo == "ActualizarUnico" or \
                funcion.tipo == "EliminarUnico":
            texto += "\t<tr>\n"
            texto += "\t\t<td>18</td>\n"
            texto += "\t\t<td>Tk_Coma</td>\n"
            texto += "\t\t<td>,</td>\n"
            texto += "\t</tr>\n"
            texto += "\t<tr>\n"
            texto += "\t\t<td>17</td>\n"
            texto += "\t\t<td>Tk_ComillaD</td>\n"
            texto += "\t\t<td>\"</td>\n"
            texto += "\t</tr>\n"
            texto += "\t<tr>\n"
            texto += "\t<tr>\n"
            texto += "\t\t<td>19</td>\n"
            texto += "\t\t<td>Tk_LlaveA</td>\n"
            texto += "\t\t<td>{</td>\n"
            texto += "\t</tr>\n"
            texto += self.agregar_json(funcion)
            texto += "\t<tr>\n"
            texto += "\t\t<td>20</td>\n"
            texto += "\t\t<td>Tk_LlaveC</td>\n"
            texto += "\t\t<td>}</td>\n"
            texto += "\t</tr>\n"
            if funcion.tipo == "ActualizarUnico":
                texto += "\t<tr>\n"
                texto += "\t\t<td>18</td>\n"
                texto += "\t\t<td>Tk_Coma</td>\n"
                texto += "\t\t<td>,</td>\n"
                texto += "\t</tr>\n"
                texto += "\t<tr>\n"
                texto += "\t\t<td>19</td>\n"
                texto += "\t\t<td>Tk_LlaveA</td>\n"
                texto += "\t\t<td>{</td>\n"
                texto += "\t</tr>\n"
                texto += "\t<tr>\n"
                texto += "\t\t<td>22</td>\n"
                texto += "\t\t<td>Tk_Set</td>\n"
                texto += "\t\t<td>$set</td>\n"
                texto += "\t</tr>\n"
                texto += "\t<tr>\n"
                texto += "\t\t<td>21</td>\n"
                texto += "\t\t<td>Tk_DosPts</td>\n"
                texto += "\t\t<td>:</td>\n"
                texto += "\t</tr>\n"
                texto += "\t<tr>\n"
                texto += "\t\t<td>19</td>\n"
                texto += "\t\t<td>Tk_LlaveA</td>\n"
                texto += "\t\t<td>{</td>\n"
                texto += "\t</tr>\n"
                texto += self.agregar_set(funcion)
                texto += "\t<tr>\n"
                texto += "\t\t<td>20</td>\n"
                texto += "\t\t<td>Tk_LlaveC</td>\n"
                texto += "\t\t<td>}</td>\n"
                texto += "\t</tr>\n"
                texto += "\t<tr>\n"
                texto += "\t\t<td>20</td>\n"
                texto += "\t\t<td>Tk_LlaveC</td>\n"
                texto += "\t\t<td>}</td>\n"
                texto += "\t</tr>\n"
            texto += "\t<tr>\n"
            texto += "\t\t<td>17</td>\n"
            texto += "\t\t<td>Tk_ComillaD</td>\n"
            texto += "\t\t<td>\"</td>\n"
            texto += "\t</tr>\n"
            texto += "\t<tr>\n"
        texto += "\t<tr>\n"
        texto += "\t\t<td>15</td>\n"
        texto += "\t\t<td>Tk_ParC</td>\n"
        texto += "\t\t<td>)</td>\n"
        texto += "\t</tr>\n"
        texto += "\t<tr>\n"
        texto += "\t\t<td>16</td>\n"
        texto += "\t\t<td>Tk_PtoComa</td>\n"
        texto += "\t\t<td>;</td>\n"
        texto += "\t</tr>\n"
        return texto

    def comprobar_tokens(self, lexema):
        numero = None
        nombre_token = ""
        if lexema == "CrearBD":
            numero = 2
            nombre_token = "Tk_CrearBD"
        elif lexema == "EliminarBD":
            numero = 3
            nombre_token = "Tk_EliminarBD"
        elif lexema == "CrearColeccion":
            numero = 4
            nombre_token = "Tk_CrearC"
        elif lexema == "EliminarColeccion":
            numero = 5
            nombre_token = "Tk_EliminarC"
        elif lexema == "InsertarUnico":
            numero = 6
            nombre_token = "Tk_InsertarU"
        elif lexema == "ActualizarUnico":
            numero = 7
            nombre_token = "Tk_ActualizarU"
        elif lexema == "EliminarUnico":
            numero = 8
            nombre_token = "Tk_EliminarU"
        elif lexema == "BuscarTodo":
            numero = 9
            nombre_token = "Tk_BuscarT"
        elif lexema == "BuscarUnico":
            numero = 10
            nombre_token = "Tk_BuscarU"
        return numero, nombre_token