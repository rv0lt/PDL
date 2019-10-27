class TablaSimbolos:
    def __init__(self):

        self.txt =("TABLA PRINCIPAL #1:\n")
        self.cont = 2 #cuenta las tabla simbolos        

        self.tabla_global = {}
        self.pos_global =1 #posicion identificador en la tabla global
        self.despl_global = 0 #desplazamiento de la TS global
        
        self.tabla_local = None #TS local
        self.pos_local = None #posicion identificador en la tabla local
        self.despl_local = None #desplazamiento de la TS local
        
        self.pos_actual = self.pos_global
        self.tabla_actual = self.tabla_global
        self.despl_actual= self.despl_global
        self.declaracion = True #zona declaracion o uso

    def buscarTS(self, lexema):
        if self.tabla_actual == self.tabla_global:
            pos=self.tabla_global.get(lexema)
        else: #estoy en una tabla local
            pos = self.tabla_local.get(lexema)
            if pos is None: #si no esta en la local busco en la global
                pos = self.tabla_global.get(lexema)
        return pos #contendra un valor pos o None si no estaba en la TS
    def insertarTS(self, lexema, tipo):
        self.tabla_actual.update({lexema:self.pos_actual})
        
        pos = self.pos_actual
        self.pos_actual+=1
        print("AAAA " + tipo)
        
        if tipo == 'int':
            print("GGGGGGGG")
            despl = self.despl_actual            
            self.despl_actual+=2
            tp = "'int'"
        if tipo == 'boolean':
            despl = self.despl_actual
            self.despl_actual+=2
            tp="'boolean'"
        if tipo == 'string':
            despl = self.despl_actual
            self.despl_actual+=128
            tp ="'string'"

        texto=("* LEXEMA '" + lexema + "'\n" +
            "+ tipo: " + tp + "\n" +
            "+ despl: " + str(despl) +"\n"
            )
        self.txt+=texto
        return pos
    def crearFuncion(self,funcion):
        texto=("* LEXEMA '" + funcion.nombre + "'\n" +
            "+ tipo: 'funcion'\n" + 
            "+ numParam: " + str(funcion.nParam) + "\n")
        npar= funcion.nParam
        aux=1
        while(npar>0):
            texto+="+ TipoParam" + str(aux) +": " + funcion.tipoParam[aux-1] +"\n"
            npar-=1
            aux+=1
        texto+=("+ TipoRetorno: '" + str(funcion.retorno) + "'\n" +
            "+ EtiqFuncion: 'ET" + funcion.nombre + "'\n")
        self.txt+=texto
        self.crearTSL()
    def crearTSL(self):
        #guardo en global los datos de local
        self.pos_global = self.pos_actual
        self.despl_global= self.despl_actual
        self.tabla_global = self.tabla_actual
        #inicializo la TSL
        self.tabla_local={}
        self.tabla_actual=self.tabla_local
        self.pos_local = 0
        self.pos_actual = self.pos_local
        self.despl_local =0
        self.despl_actual= self.despl_local
        #creo el texto para escribir
        self.txt+=("TABLA LOCAL #" + str(self.cont)+ "\n")
        self.cont+=1
    def destuirTSL(self):
        self.tabla_actual=self.tabla_global
        self.pos_actual=self.pos_global
        self.despl_actual=self.despl_global
        
    def volcar(self):
        output= open("ts.txt", 'w')
        output.write(self.txt)
        output.close

class Fun:
    def __init__(self):
            self.nombre=None
            self.retorno=None
            self.nParam=0
            self.tipoParam=[]
            self.nombreParam=[]
            self.flag=False