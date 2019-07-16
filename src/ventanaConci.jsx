import React,{Component} from 'react';
import {TextField,Paper,Select,MenuItem,Typography,Button,FormControl,InputLabel} from '@material-ui/core';
import DBHandler from './DBHandler';

function convertirFecha(fecha){
    let anio = fecha.substring(0,4)
    let mes = fecha.substring(5,7)
    let dia = fecha.substring(8,10)
    return dia + '/' + mes + '/' + anio
}



export default class Menu extends Component{

    constructor(props){
        super(props);
        this.state = {
            banco:'BP',
            cuentasBancarias:[],
            cuentasContables:[],
            cuentaBacanria:'',
            cuentaContable:'',
            cuentas:[],
            sucursal:'',
            archivo:'',
            movimientos:[],
            posicion:null,
            desde:'',
            hasta:'',
            resumen:''
        }
        this.db = new DBHandler()
        this.db.pedirCuentas(this.cargarCuentas.bind(this),2019)
    }


    seleccionarCuenta(cuenta){
        
        let dic = {
            cuentaBancaria:this.state.cuentas[cuenta].cuenta,
            cuentaContable:this.state.cuentas[cuenta].nro_cuenta,
            sucursal:this.state.cuentas[cuenta].sucursal,
            posicion:cuenta,
        }
        this.setState(dic)

    }
    enviarDatos(datos){
        return;
    }

    limpiarInterfaz(resumen){
        this.setState({
            cuentaBacanria:'',
            cuentaContable:'',
            sucursal:'',
            archivo:'',
            movimientos:[],
            posicion:null,
            desde:'',
            hasta:'',
            resumen:resumen
        })
    }

    leerArchivo(){
        let file = this.state.archivo;
        let reader = new FileReader();
        let dic ={
            desde:convertirFecha(this.state.desde),
            hasta:convertirFecha(this.state.hasta),
            cuentabancaria:this.state.cuentaBancaria,
            cuentacontable:this.state.cuentaContable,
            banco:this.state.banco,
            sucursal:this.state.sucursal,
        }

        if(dic.desde.length === 0 || dic.hasta.length === 0 || 
            dic.cuentabancaria.length === 0 || dic.cuentacontable.length === 0 
            || dic.banco.length === 0 || dic.sucursal.length === 0){
                return
        }
        let fun = this.limpiarInterfaz.bind(this)
        let db = this.db
        reader.onload = function(progressEvent){
        
            let lines = this.result.split('\n');
            dic.entrada = lines;
            db.impactarExtracto(fun,dic);
            
    
        };
        reader.readAsText(file);
    }

    cargarCuentas(cuentas){
        let cuentasBancarias = [];
        let cuentasContables = [];
        for (let x = 0; x < cuentas.length; x++){

            cuentasBancarias.push(<MenuItem value={x} key={x}> {cuentas[x].cuenta}</MenuItem>);
            cuentasContables.push(<MenuItem value={x} key={x}> {cuentas[x].nro_cuenta}</MenuItem>);
            
        }

        this.setState(
            {
                cuentasBancarias:cuentasBancarias,
                cuentasContables:cuentasContables,
                cuentas:cuentas
            })
    }

    render(){
        return (<div style={{textAlign:'center'}}>
            <Typography variant='title'>Conciliaciones Banco Provincia</Typography><br/>
            <div>
                <TextField 
                    value={this.state.sucursal} label='Codigo de Sucursal'
                    onChange={(ev)=>this.setState({banco:ev.target.value})}
                ></TextField>
                <FormControl>
                    <InputLabel htmlFor='cuentabancaria' shrink={true}>Cuenta Bancaria</InputLabel>
                    <Select inputProps={{id:'cuentabancaria'}}
                        value={this.state.posicion} style={{width:'150px'}}
                        onChange={(ev)=>this.seleccionarCuenta.bind(this)(ev.target.value)}
                    >
                        {this.state.cuentasBancarias}
                    </Select>
                </FormControl>
                <FormControl>
                    <InputLabel htmlFor='cuentacontable' shrink={true}>Cuenta Contable</InputLabel>
                    <Select
                        value={this.state.posicion} style={{width:'150px'}} inputProps={{id:'cuentabancaria'}}
                        onChange={(ev)=>this.seleccionarCuenta.bind(this)(ev.target.value)}
                    >
                        {this.state.cuentasContables}
                    </Select>
                </FormControl>
            </div>
            <div>
                <TextField
                    InputLabelProps={{shrink:true}}
                    value={this.state.desde} label='Desde' type='date'
                    onChange={(ev)=>{this.setState({desde:ev.target.value})}}
                ></TextField>
                <TextField
                    InputLabelProps={{shrink:true}}
                    value={this.state.hasta} label='Hasta' type='date'
                    onChange={(ev)=>{this.setState({hasta:ev.target.value})}}
                ></TextField>
            </div>
            <div>
                <TextField
                    value={this.state.urlArchivo} label='Archivo' type='file'
                    onChange={(ev)=>this.setState({
                        urlArchivo:ev.target.value,
                        archivo:ev.target.files[0]})}
                ></TextField>
                <Button
                    onClick={this.leerArchivo.bind(this)}
                >
                    Enviar
                </Button>
            </div>
        </div>)
    }
}