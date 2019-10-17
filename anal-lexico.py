import ply.lex as lex
import sys
posTs=1
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
    #'CADENA', #"hola"
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
    t.value="-"
    return t
def t_opRel(t):
    r'>'
    t.value=1
    return t
def t_opLog(t):
    r'!'
    t.value=1
    return t
def t_asignacion(t):
    r'='
    t.value="-"
    return t
def t_coma(t):
    r','
    t.value="-"
    return t
def t_puntoComa(t):
    r';'
    t.value="-"
    return t
def t_parAb(t):
    r'\('
    t.value="-"
    return t
def t_parCerr(t):
    r'\)'
    t.value="-"
    return t
def t_corchAb(t):
    r'\{'
    t.value="-"
    return t
def t_corchCerr(t):
    r'\}'
    t.value="-"
    return t
def t_opArt(t):
    r'\+'
    t.value = 1
    return t        
 
def t_id(t):
    r'[a-zA-z_][a-zA-Z_0-9]*'
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
    r'\d+'
    t.value = int(t.value)
    return t
#def t_CADENA(t) :  
#no se me ocurre como implementarlo

def t_comments(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
def t_newline(t):
    r'\n'
    t.lexer.lineno+=1  
def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)
t_ignore = ' \t' #Contiene espacios y tabuladores
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("ERROR: no se ha especificado archivo ")
        sys.exit(1)
    lexer=lex.lex()
    data = open(sys.argv[1], 'r')
    linea = data.readline()
    output = open("output.txt", 'w')
    while linea != "":
        lexer.input(linea)
        linea = data.readline()
        while True:
            tok = lexer.token()
            if not tok: break
            tokens  = ("(" + tok.type + ","  + str(tok.value) +")" ) 
            print tokens
            tokens+= " token number "+ str(tok.lexpos +1) + " in line " + str(tok.lineno)  +"\n"
            output.write(tokens)
            
    data.close()
    output.close()
    #lex.input("a+b")
    #for tok in iter(lex.token, None):
    #    print repr(tok.type), repr(tok.value)

     #lex.runmain(lexer)
