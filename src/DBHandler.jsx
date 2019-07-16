export default class DBHandler{

    HOST = 'localhost:1700'

    pedirCuentas(fun,anio){
        this.enviarPeticion(fun,'datos/devolverCuentas','POST',{ejercicio:anio},true)
    }

    enviarFilas(fun,lista){
        this.enviarPeticion(fun,'conci/cargar','POST',{lineas:lista},true)
    }

    impactarExtracto(fun,datos){
        this.enviarPeticion(fun,'extracto/impactar','POST',datos,true)
    }


    enviarPeticion(fun,url,metodo,datos,asinc=true){
        var request = new XMLHttpRequest();
        request.onreadystatechange = function(){
        if(this.readyState === 4 && this.status === 200){
            if (fun != null){
            if (this.responseText.length > 0){
                fun(JSON.parse(this.responseText));
            }
            else{
                fun();
            }
            }
        }
        };
        request.open(metodo,"http://"+this.HOST+"/"+url,asinc);
        var datosFinales = {};
        datosFinales = datos;
        if (metodo == "POST"){
        request.setRequestHeader('Content-type','application/json');
        request.send(JSON.stringify(datosFinales));
        }
        else {request.send();}
    }
}