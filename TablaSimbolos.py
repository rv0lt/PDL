class TablaSimbolos:
    def __init__(self):

        self.cont = 2 #cuenta las tabla simbolos        
        self.pos =1 #posicion identificador
        self.declaracion = True #zona declaracion o uso        
        self.txt_completo=""
        self.tipos={}
        self.tiposRetorno={}
        self.nParams={}
        self.tipoParams={}

        self.txt_global ="#1:\n"
        self.tabla_global = {}
        self.despl_global = 0 #desplazamiento de la TS global
        
        self.tabla_local = None #TS local
        self.txt_local = None
        self.despl_local = None #desplazamiento de la TS local

        self.txt_actual=self.txt_global
        self.tabla_actual = self.tabla_global
        self.despl_actual= self.despl_global
    def buscarTipo(self,lexema):
        tipo = self.tipos.get(lexema)
        return tipo
    def buscarTipoRetorno(self, lexema):
        tipo = self.tiposRetorno.get(lexema)
        return tipo
    def buscarnParamFuncion(self,lexema):
        n = self.nParams.get(lexema)
        return n
    def buscarTipoParamFuncion(self,lexema):
        tips = self.tipoParams.get(lexema)
        return tips
    def buscarTS(self, lexema):
        if self.tabla_actual == self.tabla_global:
            pos=self.tabla_global.get(lexema)
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
        self.tipos.update({lexema:tipo})     
        pos = self.pos
        self.pos+=1
        
        if tipo == 'int':
            despl = self.despl_actual            
            self.despl_actual+=1
            tp = "'ent'"
        elif tipo == 'boolean':
            despl = self.despl_actual
            self.despl_actual+=1
            tp="'log'"
        elif tipo == 'string':
            despl = self.despl_actual
            self.despl_actual+=64
            tp ="'cadena'"
        elif tipo == "funcion":
            return pos
        self.txt_actual+=("*'" + lexema + "'\n" +
            "+ tipo:" + tp + "\n" +
            "+ despl:" + str(despl) +"\n"
            )
        return pos
    def crearFuncion(self,funcion):
        texto=("*'" + funcion.nombre + "'\n" +
            "+ tipo:'funcion'\n" + 
            "+ numParam:" + str(funcion.nParam) + "\n")
        npar= funcion.nParam
        self.nParams.update({funcion.nombre:funcion.nParam})
        aux=1
        while(npar>0):
            texto+="+ TipoParam" + str(aux) +":'" 
            parm=funcion.tipoParam[aux-1]
            if parm == 'string': parm='cadena'
            elif parm == 'boolean': parm='log'
            else: parm='ent'
            texto+= parm +"'\n"
            npar-=1
            aux+=1
        self.tipoParams.update({funcion.nombre:funcion.tipoParam})
        if not(funcion.retorno is None):
            retn=funcion.retorno
            if retn == 'string': retn='cadena'
            elif retn == 'boolean' : retn = 'log'
            else: retn = 'ent' 
            texto+=("+ TipoRetorno:'" + str(retn) + "'\n")
            self.tiposRetorno.update({funcion.nombre:funcion.retorno})
        else:
            texto+=("+ TipoRetorno: " + "\n")
        texto+=("+ EtiqFuncion:'ET" + funcion.nombre + "'\n")
        self.txt_actual+=texto
        self.crearTSL(funcion.tipoParam, funcion.nombreParam)
        
    def crearTSL(self, tipoParam, nombreParam):
        #guardo en global los datos de actual
        self.despl_global= self.despl_actual
        self.tabla_global = self.tabla_actual
        self.txt_global = self.txt_actual
        #inicializo la TSL
        self.tabla_local={}
        self.tabla_actual=self.tabla_local
        self.despl_local =0
        self.despl_actual= self.despl_local
        self.txt_local = ("#" + str(self.cont)+ ":\n")
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
        self.txt_completo=self.txt_actual+self.txt_completo
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