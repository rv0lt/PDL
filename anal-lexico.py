import ply.lex as lex
import sys
palabras_clave = {
    #Definir las palabras clave
    'var': 'VAR',
    'int':'INT',
    'for':'FOR',
    'boolean':'BOOLEAN',
    'string' : 'STRING',
    'print' : 'PRINT',
    'return' : 'RETURN',
    'function': 'FUNCTION',
    'if' : 'IF',
    'input': 'INPUT'
}
tokens = (
    'ID',
    'ENTERO',
    'ASIGNACION', # =
    'COMA',
    #'CADENA', #"hola"
    'OPARITMETICO', #+
    'OPRELACIONAL', # >
    'OPLOGICO', # !
    'OPESPECIAL', # b1|=b2 -> b1 = b1 || b2
    'PUNTOCOMA', # ;
    'PARAB', # ( 
    'PARCER', # )
    'CORCHETEAB', # [
    'CORCHETECER' # ]    
)
# Reglas de expresiones regulares para tokens simples
t_OPESPECIAL = r'\|='
t_OPARITMETICO = r'\+'
t_OPRELACIONAL = r'>'
t_OPLOGICO = r'!'
t_ASIGNACION = r'='
t_COMA = r','
t_PUNTOCOMA = r';'
t_PARAB = r'\('
t_PARCER = r'\)'
t_CORCHETEAB = r'\{'
t_CORCHETECER = r'\}'

#Reglas de expresiones regulares ms complejas
def t_ID(t):
    r'[a-zA-z_][a-zA-Z_0-9]*'
    t.type = palabras_clave.get(t.value,'ID')
    return t
def t_NUMBER(t):
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
    while linea != "":
        lexer.input(linea)
        linea = data.readline()
        while True:
            tok = lexer.token()
            if not tok: break
            print tok
    #lex.input("a+b")
    #for tok in iter(lex.token, None):
    #    print repr(tok.type), repr(tok.value)

     #lex.runmain(lexer)
