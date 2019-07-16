import cx_Oracle as ORA

HOST = '172.22.20.152'#'10.10.10.1'
US = 'owner_rafam'
PASS = 'ownerdba'
SID = 'BDRAFAM'#'MSV'




class DBServer:




    def __init__(self):
        self.con,self.cur = _conectar()
        

    def aceptarCambios(self):
        self.con.commit()
        return

    def conectar(self):
        self.con,self.cur = _conectar()


    def desconectar(self):
        self.con.close()

    def contestarQuery(self,sql,data=None,fetch=True):
        if(data == None):
            self.cur.execute(sql)
        else:
            self.cur.execute(sql,data)
        if fetch == False:
            return 
        return self.cur.fetchall()


def _conectar():
    con = ORA.connect(""+US + "/" + PASS + "@" + HOST + "/" + SID)
    cur = con.cursor()
    return con,cur
