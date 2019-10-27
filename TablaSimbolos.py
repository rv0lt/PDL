class TablaSimbolos:
    def __init__(self):

        self.cont = 2 #cuenta las tabla simbolos        
        self.pos =1 #posicion identificador
        self.declaracion = True #zona declaracion o uso        
        self.txt_completo=""

        self.txt_global ="TABLA PRINCIPAL #1:\n"
        self.tabla_global = {}
        self.despl_global = 0 #desplazamiento de la TS global
        
        self.tabla_local = None #TS local
        self.txt_local = None
        self.despl_local = None #desplazamiento de la TS local

        self.txt_actual=self.txt_global
        self.tabla_actual = self.tabla_global
        self.despl_actual= self.despl_global

    def buscarTS(self, lexema):
        if self.tabla_actual == self.tabla_global:
            pos=self.tabla_global.get(lexema)
            print(lexema)
        else: #estoy en una tabla local
            pos = self.tabla_local.get(lexema)
            if pos is None: #si no esta en la local busco en la global
                pos = self.tabla_global.get(lexema)
        return pos #contendra un valor pos o None si no estaba en la TS
    def insertarTSL(self):
        pos=self.pos
        self.pos+=1
        return pos
    def insertarTS(self, lexema, tipo):
        self.tabla_actual.update({lexema:self.pos})
        
        pos = self.pos
        self.pos+=1
        
        if tipo == 'int':
            despl = self.despl_actual            
            self.despl_actual+=2
            tp = "'int'"
        elif tipo == 'boolean':
            despl = self.despl_actual
            self.despl_actual+=2
            tp="'boolean'"
        elif tipo == 'string':
            despl = self.despl_actual
            self.despl_actual+=128
            tp ="'string'"
        elif tipo == "funcion":
            return pos
        self.txt_actual+=("* LEXEMA '" + lexema + "'\n" +
            "+ tipo: " + tp + "\n" +
            "+ despl: " + str(despl) +"\n"
            )
        return pos
    def crearFuncion(self,funcion):
        texto=("* LEXEMA '" + funcion.nombre + "'\n" +
            "+ tipo: 'funcion'\n" + 
            "+ numParam: " + str(funcion.nParam) + "\n")
        npar= funcion.nParam
        aux=1
        while(npar>0):
            texto+="+ TipoParam" + str(aux) +": '" + funcion.tipoParam[aux-1] +"'\n"
            npar-=1
            aux+=1
        texto+=("+ TipoRetorno: '" + str(funcion.retorno) + "'\n" +
            "+ EtiqFuncion: 'ET" + funcion.nombre + "'\n")
        self.txt_actual+=texto
        self.crearTSL(funcion.tipoParam, funcion.nombreParam)
    def crearTSL(self, tipoParam, nombreParam):
        #guardo en global los datos de local
        self.despl_global= self.despl_actual
        self.tabla_global = self.tabla_actual
        self.txt_global = self.txt_actual
        #inicializo la TSL
        self.tabla_local={}
        self.tabla_actual=self.tabla_local
        self.despl_local =0
        self.despl_actual= self.despl_local
        self.txt_local = ("TABLA LOCAL #" + str(self.cont)+ ":\n")
        self.txt_actual = self.txt_local
        #creo el texto para escribir
        self.cont+=1
        numPar = len(nombreParam)
        aux=0
        self.pos-=numPar
        while(numPar>0):
            tipo=tipoParam[aux]
            self.insertarTS(nombreParam[aux], tipo)
 
            numPar-=1
            aux+=1    
    
    def destuirTSL(self):
        self.tabla_actual=self.tabla_global
        self.despl_actual=self.despl_global
        self.txt_completo+=self.txt_actual
        self.txt_actual = self.txt_global
    def volcar(self):
        output= open("ts.txt", 'w')
        self.txt_completo=self.txt_global+self.txt_completo
        output.write(self.txt_completo)
        output.close

class Fun:
    def __init__(self):
            self.nombre=None
            self.retorno=None
            self.nParam=0
            self.tipoParam=[]
            self.nombreParam=[]
            self.flag=False
    def reinicio(self):
            self.flag=False
            self.nParam=0
            self.tipoParam=[]
            self.nombreParam=[]