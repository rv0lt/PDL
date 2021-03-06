import ply.lex as lex
from ply.lex import TOKEN
import sys
import re
from TablaSimbolos import TablaSimbolos
from TablaSimbolos import Fun
from gramatica import parser
import gramatica
lexema=""
tipo=None
comentario=False
tabla_simbolos = TablaSimbolos()
estoy_en_fun=False #sirve para indicar si voy a leer una funcion
flagFor = False
flagFor2 = False
contador=0
contReturn=0
contParentesis_1=0
flagIf = False
metaFlagIf = False
flagExpresion=False
anotherFlag = False
opEsp=False
checkParentesis=False
funPass=False
listaExpresion=[]
listaTokens=[] #Para pasarle al sintactico
funcion = Fun()
funcionAux = Fun()
tipos=(
        #palabras clave que hacen referencia a los tipos de datos
        'int',
        'boolean',
        'string'
)
palabras_clave = tipos +(
    #Definir las palabras clave
    'var',
    'for',
    'print',
    'return',
    'function',
    'if',
    'input'
)

tokens = palabras_clave + (
    'id',
    'cte_entera',
    'asignacion', # =
    'coma', # ,
    'cadena', #"hola"
    'opArt', #+
    'opRel', # >
    'opLog', # !
    'opEsp', # b1|=b2 -> b1 = b1 || b2
    'puntoComa', # ;
    'parAb', # ( 
    'parCerr', # )
    'corchAb', # {
    'corchCerr' # }    
)
def limpiar_expresion():
        global listaExpresion
        listaExpresionLimpiada=[]
        backup_listaExpresion=[]
        contParentesis_2=1
        #print(listaExpresion)
        while len(listaExpresion)>0:
                elem = listaExpresion.pop()
                if elem == ')':
                        contParentesis_2+=1
                if elem == '(':
                        contParentesis_2-=1

                if contParentesis_2 !=0:
                        listaExpresionLimpiada.append(elem)

                if contParentesis_2 == 0:
                        listaExpresionLimpiada.reverse()
                        backup_listaExpresion = listaExpresion
                        listaExpresion=listaExpresionLimpiada
                        #print("nueva expresion\n")
                        #print(listaExpresion)
                        tipo = evaluar_expresion()
                        listaExpresion=backup_listaExpresion
                        return tipo




def evaluar_expresion():
        check=False
        tipoRetorno=None
        simboloMayorQue = False
       #print("-----------------\n")
        #print(listaExpresion)
        while len(listaExpresion)>0:
                elem= listaExpresion.pop()

                if elem == ')':
                        elem=limpiar_expresion()


                if not check:
                        if elem == ">" or elem == "!" or elem == "+":
                                return "error"
                        else:
                                if tipoRetorno is not None:
                                        if tipoRetorno == "+" and elem != "int":
                                                return "error"
                                        elif tipoRetorno == ">" and elem != "int":
                                                return "error"
                                tipoRetorno=elem
                        check=True
                else:
                        if elem == "!" and (tipoRetorno != "boolean" and not simboloMayorQue):
                                return "error"
                        elif elem == ">":
                                if tipoRetorno != "int" or simboloMayorQue:
                                        return "error"
                                simboloMayorQue=True
                        elif elem == "+" and tipoRetorno != "int":
                                return "error"
                        check=False
                        tipoRetorno = elem
        if tipoRetorno == "!" or simboloMayorQue: tipoRetorno = "boolean"
        #print(tipoRetorno)
        return tipoRetorno
                                

# Reglas de expresiones regulares para los tokens
def t_opEsp(t):
    r'\|='
    global lexema
    global flagExpresion
    global opEsp
    if(not comentario):
        listaTokens.append(t.value)
        flagExpresion=True
        opEsp=True
        t.value=" "
        return t
def t_opRel(t):
    r'>'
    if(not comentario):
        listaTokens.append(t.value)
        if flagExpresion:
                listaExpresion.append(t.value)
        t.value=" "
        return t
def t_opLog(t):
    r'!'
    global flagExpresion
    if(not comentario):
        listaTokens.append(t.value)
        if flagExpresion:
                listaExpresion.append(t.value)
        t.value=" "
        return t
def t_asignacion(t):
    r'='
    global flagExpresion
    if(not comentario):
        flagExpresion=True
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_coma(t):
    r','
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_puntoComa(t):
    r';'
    global listaExpresion
    global flagExpresion
    global lexema
    global opEsp
    global flagFor,contador
    global metaFlagIf
    if(not comentario):
        listaTokens.append(t.value)
        if metaFlagIf: metaFlagIf=False
        if flagFor:
                contador -=1
                if contador == 0:
                        #flagExpresion=False
                       #print(listaExpresion)
                        exp=evaluar_expresion()
                        if exp!='boolean':
                                raise Exception ("Error en la condicion del for")
        
        if flagExpresion and not flagIf:
                flagExpresion = False
                exp = evaluar_expresion()
                if exp == "error":
                        raise Exception ("La expresion escrita no tiene los tipos correctos")

                elif lexema == "return":  
                        if exp!=funcionAux.retorno:
                                raise Exception("Tipo no valido para el return")
                elif lexema=="print":
                        if exp == 'boolean': 
                                raise Exception ("Tipo logico en print o input")
                elif opEsp:
                        opEsp=False
                        if ( (tabla_simbolos.buscarTipo(lexema) != 'boolean') or (exp!='boolean') ):
                                raise Exception ("Tipo no logico en asignacion con or logico")
                elif tabla_simbolos.buscarTipo(lexema) != exp:
                        '''print("------\n")
                        print(tabla_simbolos.buscarTipo(lexema))
                        print(lexema)
                        print(exp)
                        print("-------\n") '''
                        #print(exp)
                        if flagFor and exp!=None:
                                raise Exception("Asignacion de tipos distintos en la iniciacion del for")
                        elif not flagFor and lexema!="": raise Exception("Tipo incorrecto en asignacion")

        if contador ==1 and flagFor:
                flagExpresion=True
        lexema=""#Es posible que falle por esto
        t.value=" "
        return t
def t_parAb(t):
    r'\('
    global checkParentesis, flagExpresion,contParentesis_1
    if(not comentario):
        listaTokens.append(t.value)
        if flagIf and not checkParentesis:
                checkParentesis=True
        if flagExpresion and flagIf:
                contParentesis_1+=1
                if contParentesis_1 !=0:
                        listaExpresion.append(t.value)

        t.value=" "
        return t
def t_parCerr(t):
    r'\)'
    global anotherFlag,flagFor, flagIf, opEsp, checkParentesis,funPass, contParentesis_1
    if(not comentario):
        listaTokens.append(t.value)
        if flagExpresion and flagIf:
                contParentesis_1-=1
                if contParentesis_1 !=0:
                        listaExpresion.append(t.value)   
                        t.value=" "
                        return t
                #print(listaExpresion)
                listaExpresion.append(t.value)

        if flagIf:
                flagIf=False
                exp=evaluar_expresion()

                if exp != "boolean":
                        raise Exception("Asignacion de tipos distintos en el if")
                        

        if flagFor:
                flagFor=False
                exp=evaluar_expresion()
                if exp == "error" or tabla_simbolos.buscarTipo(lexema) !=exp:
                        if exp !=None:
                                raise Exception("Asignacion de tipos distintos en la actualizacion del for")
                elif opEsp:
                        opEsp=False
                        if ( (tabla_simbolos.buscarTipo(lexema) != 'boolean') or (exp!='boolean') ):
                                raise Exception ("Tipo incorrecto en actualizacion del for")
       # print(anotherFlag)
       # print(flagExpresion)
        if anotherFlag and flagExpresion:
                anotherFlag=False
                if funcionAux.nParam > 1:
                        #print(funcionAux.nParam-1)
                        #print(funcionAux.nombre)
                        #print(tabla_simbolos.buscarnParamFuncion(funcionAux.nombre))


                        if funcionAux.nParam-1 != tabla_simbolos.buscarnParamFuncion(funcionAux.nombre):
                                funPass=False
                                raise Exception ("Numero de parametros equivocado")
                        funcionAux.tipoParam.reverse()
                        funcionAux.tipoParam.pop()
                        funcionAux.tipoParam.reverse()

                        if funcionAux.tipoParam != tabla_simbolos.buscarTipoParamFuncion(funcionAux.nombre):
                                funPass=False
                                raise Exception ("Tipos de los atributos equivocado")
                else:
                        if tabla_simbolos.buscarnParamFuncion(funcionAux.nombre) > 0:
                                raise Exception ("Numero de argumentos erroneo")
                funcionAux.reinicio()
        if checkParentesis:
                checkParentesis=False
        t.value=" "
        return t
def t_corchAb(t):
    r'\{'
    global estoy_en_fun
    if(not comentario):
        if estoy_en_fun:
                #si estoy leyendo una funcion y veo las llaves abiertas signigica que ya he dejado de declararla
                estoy_en_fun=False
                tabla_simbolos.declaracion=False
                tabla_simbolos.crearFuncion(funcion)
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_corchCerr(t):
    r'\}'
    global flagFor2,contReturn
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        if not flagFor2:
                if contReturn <=0 and funcionAux.retorno is not None:
                        raise Exception("Error en el cuerpo de la funcion")
                tabla_simbolos.destuirTSL()
                funcion.reinicio()
                funcionAux.reinicio()
        else:
                flagFor2=False
        return t
def t_opArt(t):
    r'\+'
    global flagExpresion
    if(not comentario):
        if flagExpresion:
                listaExpresion.append(t.value)
        listaTokens.append(t.value)
        t.value = " "
        return t        
 
def t_id(t):
    r'[a-zA-z_]\w*'
    if(not comentario):
        global tipo
        global estoy_en_fun
        global flagFor, flagFor2
        global flagIf,metaFlagIf
        global flagExpresion
        global anotherFlag
        global lexema
        global contador, contReturn
        if t.value in palabras_clave:
            listaTokens.append(t.value)
            t.type = t.value
            t.value = " "
            if t.type == 'var': #cada vez que leo var entro en zona de declaraciom
                    tabla_simbolos.declaracion=True
            elif t.type in tipos and (tabla_simbolos.declaracion or estoy_en_fun):
                    #si estoy en zona de declaracion o acabo de leer un function me quiero guardar el tipo
                    tipo= t.type
            elif t.type == 'function': #voy a leer una funcion
                    estoy_en_fun=True
                    contReturn=0
            elif t.type == 'for':
                    flagFor=True
                    flagFor2=True
                    contador=2
            elif t.type == 'if':
                    flagIf=True
                    metaFlagIf=True
                    flagExpresion=True
            elif t.type == 'print' or t.type == 'input':
                    flagExpresion=True
                    lexema="print"
            elif t.type == 'return':
                    flagExpresion=True
                    lexema="return"
                    contReturn+=1
                    if metaFlagIf:
                            contReturn-=1
        else:
            t.type = "id"
            if tabla_simbolos.buscarTipo(t.value) == "funcion":
                    flagExpresion=True
                    if anotherFlag:
                            funPass=True
            if not flagExpresion: lexema=t.value
            if flagExpresion and not anotherFlag:
                    if tabla_simbolos.buscarTipo(t.value) == "funcion":
                        listaExpresion.append(tabla_simbolos.buscarTipoRetorno(t.value))
                        funcionAux.nombre=t.value
                        anotherFlag = True
                    else:
                        listaExpresion.append(tabla_simbolos.buscarTipo(t.value))
            listaTokens.append(t.type)
            #if flagIf:
            #        flagIf=False
            #        if tabla_simbolos.buscarTipo(t.value) != "boolean":
            #                raise Exception("error en el if")
            if anotherFlag:
                if flagExpresion:
                        funcionAux.nParam+=1
                        funcionAux.tipoParam.append(tabla_simbolos.buscarTipo(t.value))
            if estoy_en_fun:
                    if not funcion.flag:
                            funcion.retorno=tipo
                            funcion.nombre=t.value
                            funcionAux.retorno=tipo
                            funcion.flag=True
                            q=tabla_simbolos.insertarTS(t.value, "funcion")
                    else:
                            funcion.nParam+=1
                            funcion.tipoParam.append(tipo)
                            funcion.nombreParam.append(t.value)
                            q = tabla_simbolos.insertarTSL()

            elif tabla_simbolos.declaracion: #zona declaracion
                    q=tabla_simbolos.buscarTS(t.value)
                    if q is not None:
                            #print(t.value)
                            raise Exception("id ya declarada")
                    else:
                            q= tabla_simbolos.insertarTS(t.value,tipo)
                            #una vez que he leido el ID paso a zona de uso 
                            tabla_simbolos.declaracion=False
            
            else: #zona de uso
                    q= tabla_simbolos.buscarTS(t.value)
                    if q is None:
                        raise Exception("id no declarado")
            t.value=q
            tipo=None
        return t
def t_cte_entera(t):
    r'\d+\.?(\d+)?'
    global flagExpresion
    global anotherFlag
    if(not comentario):
        if eval(t.value) > 32767 or '.' in t.value:
            raise Exception ("Lexical: illegal character '%s' in line '%d' position" % (t.value, t.lineno))
            t.lexer.skip(1)
        else:
            t.value = eval(t.value)
            if flagExpresion:
                    if anotherFlag:
                            funcionAux.nParam+=1
                            funcionAux.tipoParam.append("int")
                    else:
                            listaExpresion.append("int")
            listaTokens.append(t.type)
            return t
def t_cadena(t) :  
    r'"([^"\\]|(\\.))*"'
    global flagExpresion
    if(not comentario):
        if len(t.value)-2>64 : 
                raise Exception("Cadena demasiado larga")
        if flagExpresion:
                if anotherFlag:
                        funcionAux.nParam+=1
                        funcionAux.tipoParam.append("string")
                else:
                        listaExpresion.append("string")
        listaTokens.append(t.type)
        return t
def t_newline(t):
    r'\n'
    t.lexer.lineno+=1  
#t_ignore_COMMENT = r'/\*(.|\n)*?\*/'
#@TOKEN(regex)
def t_commentab(t):
    r'/\*'
    global comentario
    comentario = True
def t_commentcer(t):
    r'\*/'
    global comentario
    comentario = False



def t_error(t):
    if(not comentario):
        print("")
    t.lexer.skip(1)
t_ignore = ' \t' #Contiene espacios y tabuladores

        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("ERROR parametros incorrectos")
        sys.exit(1)
    lexer=lex.lex(reflags=re.DOTALL)
    tabla_simbolos =TablaSimbolos()
    data = open(sys.argv[1], 'r')
    linea = data.readline()
    output = open("output/tokens.txt", 'w')
    lex.lex(reflags=re.DOTALL)
    while linea != "":
        lexer.input(linea)
        linea = data.readline()
        while True:
            tok = lexer.token()
            if not tok: break
            tokens  = ("<" + tok.type + ","  + str(tok.value) +">" ) 
            #print(tokens)
            output.write(tokens+"\n") 
            tokens+= " token number "+ str(tok.lexpos +1) + " in line " + str(tok.lineno)  +"\n"
            #print(tokens)
    tabla_simbolos.volcar()
    #Ahora he generado un fichero con los tokens y he creado la tabla de Simbolos
    #El siguiente paso es pasar la lista de Tokens identificados al parser
    #print(listaTokens) 
    if parser.match(listaTokens):
            print("ACEPT")
    else:
            print("REJEC")
    parser.verbose_match(listaTokens, False)
    #parser.print_table()
    #gramatica.res
   # print(gramatica.res)


    data.close()
    output.close()
    #lex.input("a+b")
    #for tok in iter(lex.token, None):
    #    print repr(tok.type), repr(tok.value)

     #lex.runmain(lexer)
