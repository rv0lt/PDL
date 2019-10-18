import ply.lex as lex
from ply.lex import TOKEN
import sys
import re
posTs=1
comentario=False
regex = re.compile('/\*(.|[\r\n])*\*/', re.DOTALL)

palabras_clave = (
    #Definir las palabras clave
    'var',
    'int',
    'for',
    'boolean',
    'string',
    'print',
    'return',
    'function',
    'if',
    'input'
)
tokens = palabras_clave + (
    'id',
    'entero',
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
    'corchAb', # [
    'corchCerr' # ]    
)
# Reglas de expresiones regulares para los tokens
def t_opEsp(t):
    r'\|='
    global comentario
    if(not comentario):
        t.value="-"
        return t
def t_opRel(t):
    r'>'
    global comentario
    if(not comentario):
        t.value=1
        return t
def t_opLog(t):
    r'!'
    global comentario
    if(not comentario):
        t.value=1
        return t
def t_asignacion(t):
    r'='
    global comentario
    if(not comentario):
        t.value="-"
        return t
def t_coma(t):
    r','
    global comentario
    if(not comentario):
        t.value="-"
        return t
def t_puntoComa(t):
    r';'
    global comentario
    if(not comentario):
        t.value="-"
        return t
def t_parAb(t):
    r'\('
    global comentario
    if(not comentario):
        t.value="-"
        return t
def t_parCerr(t):
    r'\)'
    global comentario
    if(not comentario):
        t.value="-"
        return t
def t_corchAb(t):
    r'\['
    global comentario
    if(not comentario):
        t.value="-"
        return t
def t_corchCerr(t):
    r'\]'
    global comentario
    if(not comentario):
        t.value="-"
        return t
def t_opArt(t):
    r'\+'
    global comentario
    if(not comentario):
        t.value = 1
        return t        
 
def t_id(t):
    r'[a-zA-z_][a-zA-Z_0-9]*'
    global comentario
    if(not comentario):
        global posTs
        if t.value in palabras_clave:
            t.type = t.value
            t.value = "-"
        else:
            t.type = "id"
            t.value=posTs
            posTs+=1
        return t
def t_entero(t):
    r'\d+\.?(\d+)?'
    global comentario
    if(not comentario):
        if eval(t.value) > 32767 or '.' in t.value:
            print ("Lexical: illegal character '%s' in line '%d' position" % (t.value, t.lineno))
            t.lexer.skip(1)
        else:
            t.value = eval(t.value)
            return t
def t_cadena(t) :  
    r'"([^"\\]|(\\.))*"'
    global comentario
    if(not comentario):
        return t
    # keep multiline comments
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
    global comentario
    if(not comentario):
        print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)
t_ignore = ' \t' #Contiene espacios y tabuladores
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("ERROR parametros incorrectos")
        sys.exit(1)
    lexer=lex.lex(reflags=re.DOTALL)
    data = open(sys.argv[1], 'r')
    linea = data.readline()
    output = open("output.txt", 'w')
    lex.lex(reflags=re.DOTALL)
    while linea != "":
        lexer.input(linea)
        linea = data.readline()
        while True:
            tok = lexer.token()
            if not tok: break
            tokens  = ("(" + tok.type + ","  + str(tok.value) +")" ) 
            print(tokens) 
            tokens+= " token number "+ str(tok.lexpos +1) + " in line " + str(tok.lineno)  +"\n"
            output.write(tokens)
            
    data.close()
    output.close()
    #lex.input("a+b")
    #for tok in iter(lex.token, None):
    #    print repr(tok.type), repr(tok.value)

     #lex.runmain(lexer)
