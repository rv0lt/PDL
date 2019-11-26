import ply.lex as lex
from ply.lex import TOKEN
import sys
import re
from TablaSimbolos import TablaSimbolos
from TablaSimbolos import Fun
from gramatica import parser
tipo=None
comentario=False
tabla_simbolos = TablaSimbolos()
estoy_en_fun=False #sirve para indicar si voy a leer una funcion
listaTokens=[] #Para pasarle al sintactico
funcion = Fun()
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
# Reglas de expresiones regulares para los tokens
def t_opEsp(t):
    r'\|='
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_opRel(t):
    r'>'
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_opLog(t):
    r'!'
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_asignacion(t):
    r'='
    if(not comentario):
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
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_parAb(t):
    r'\('
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_parCerr(t):
    r'\)'
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_corchAb(t):
    r'\{'
    global estoy_en_fun
    if(not comentario):
        if estoy_en_fun:
                #si estoy leyendo una funcion y veo las llaves abiertas signigica que ya he dejado de declararla
                estoy_en_fun=False
                tabla_simbolos.crearFuncion(funcion)
        listaTokens.append(t.value)
        t.value=" "
        return t
def t_corchCerr(t):
    r'\}'
    if(not comentario):
        listaTokens.append(t.value)
        t.value=" "
        tabla_simbolos.destuirTSL()
        funcion.reinicio()
        return t
def t_opArt(t):
    r'\+'
    if(not comentario):
        listaTokens.append(t.value)
        t.value = " "
        return t        
 
def t_id(t):
    r'[a-zA-z_]\w*'
    if(not comentario):
        global tipo
        global estoy_en_fun
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
        else:
            t.type = "id"
            listaTokens.append(t.type)
            if estoy_en_fun:
                    if not funcion.flag:
                            funcion.retorno=tipo
                            funcion.nombre=t.value
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
    if(not comentario):
        if eval(t.value) > 32767 or '.' in t.value:
            raise Exception ("Lexical: illegal character '%s' in line '%d' position" % (t.value, t.lineno))
            t.lexer.skip(1)
        else:
            t.value = eval(t.value)
            listaTokens.append(t.type)
            return t
def t_cadena(t) :  
    r'"([^"\\]|(\\.))*"'
    if(not comentario):
        if len(t.value)-2>64 : 
                raise Exception("Cadena demasiado larga")
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
    print("Comentario de multiple linea")
def t_commentcer(t):
    r'\*/'
    global comentario
    comentario = False



def t_error(t):
    if(not comentario):
        print("Illegal character %s" % t.value[0])
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
    output = open("tokens.txt", 'w')
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
            print(tokens)
    tabla_simbolos.volcar()
    #Ahora he generado un fichero con los tokens y he creado la tabla de Simbolos
    #El siguiente paso es pasar la lista de Tokens identificados al parser
    print(listaTokens) 
    if parser.match(listaTokens):
            print("ACEPT")
    else:
            print("REJEC")
    parser.verbose_match(listaTokens, True)


    data.close()
    output.close()
    #lex.input("a+b")
    #for tok in iter(lex.token, None):
    #    print repr(tok.type), repr(tok.value)

     #lex.runmain(lexer)
