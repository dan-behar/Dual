from flask import Flask, render_template, request, url_for, redirect
from jinja2 import Template, FileSystemLoader, Environment
from RegLin import reglin, grafreglin, imagen
from datetime import datetime
from datos import Datos
from NewInter import Newton
from Integracion import TrapecioM
from derivada import derivada
from lagrange import LagrangePol
from numpy import arange 
from resumenest import Media,Mediana,Moda,Maximo,Minimo,Desviacion
import matplotlib.pyplot as plt
import numpy as np
import sympy as sym
import pathlib

# Convertimos un string con formato <día>/<mes>/<año> en datetime

domain = "0.0.0.0:5000/"
templates = FileSystemLoader('templates')
environment = Environment(loader = templates)

app = Flask(__name__)

global name 
name = "" 
global hora 
hora = 0.0 
global muestra 
muestra = []
global data
data = '' 
global horaMuestra 
horaMuestra = []
global glucoMuestra 
glucoMuestra = []
global consMuestra 
consMuestra = []
global fecha1
fecha1 = ""
global fecha2
fecha2 = ""
global fechaMuestra
fechaMuestra = []
global glucoData
glucoData = []



@app.route("/", methods=["GET", "POST"])
def register():
    global name
    global hora 
    global data 
    if request.method == "POST":
        name = request.form['name']
        hora = request.form['appt']

        (h, m) = hora.split(':')
        hora = int(h) + int(m)/60 
        data = Datos('datos.xlsx',hora)
        return redirect("/rango", 301)
    return render_template("register.html")

@app.route("/rango", methods=["GET", "POST"])
def rango():
    global data
    global muestra 
    global horaMuestra
    global glucoMuestra
    global consMuestra
    global date1
    global date2
    global fecha1
    global fecha2
    global fechaMuestra
    global name
    if request.method == "POST":
        fecha1 = request.form['date1']
        fecha2 = request.form['date2']
        date1 = datetime.strptime(fecha1, '%Y-%m-%d')
        date2 = datetime.strptime(fecha2, '%Y-%m-%d')
        muestra = data.muestra(date1, date2)
        horaMuestra=[]
        glucoMuestra=[]
        consMuestra=[]
        fechaMuestra=[]
        for i in range(len(muestra)):
            horaMuestra.append(muestra[i][2])
            glucoMuestra.append(muestra[i][1])
            consMuestra.append(str(muestra[i][3]))
            fechaMuestra.append(str(muestra[i][0]))

    return render_template("rango.html", fecha1=fecha1,fecha2=fecha2,name=name)

@app.route("/graficas", methods=["GET", "POST"])
def gra():
    global horaMuestra 
    global glucoMuestra 
    global name
    if request.method == "POST":
        tipo = request.form['grafica']
        if tipo == "a": 
            fig=plt.figure()

            plt.plot(horaMuestra,glucoMuestra, 'b*',label=r'$y_1$')
            plt.xlabel('Tiempo')
            plt.ylabel('Glucosa en la Sangre')  
            plt.title('Relación Tiempo-Glucosa')
            plt.grid(True)

            #exportador de grafica
            ruta = str(pathlib.Path(__file__).parent.resolve()) # Obtiene la ruta del directorio 
            ruta = ruta.replace(chr(92),'/')+'/static/grafica.png' # Ruta final con el nombre del archivo
            fig.savefig(ruta)
        if tipo == "b": 
            fig=plt.figure()

            minimo = min(horaMuestra)
            maximo = max(horaMuestra)
            rango = arange(minimo, maximo,0.1)

            x=sym.Symbol('x')
            y=Newton(horaMuestra,glucoMuestra)
            espacio = []
            for i in rango:
                espacio.append(y.subs(x,i))
            plt.plot(rango,espacio)
            plt.xlabel('Tiempo')
            plt.ylabel('Glucosa en la Sangre')  
            plt.title('Relación Tiempo-Glucosa')
            plt.grid(True)

            #exportador de grafica
            ruta = str(pathlib.Path(__file__).parent.resolve()) # Obtiene la ruta del directorio 
            ruta = ruta.replace(chr(92),'/')+'/static/grafica.png' # Ruta final con el nombre del archivo
            fig.savefig(ruta)

    return render_template("graficas.html",name=name)

@app.route("/tabla", methods=["GET", "POST"])
def ta():
    global horaMuestra
    global glucoMuestra
    global consMuestra
    global fechaMuestra
    global name
    cambio=derivada(horaMuestra,glucoMuestra)
    for i in range(len(cambio)):
        cambio[i]=round(cambio[i],4)
    return render_template("tabla.html",cambio=cambio,fecha=fechaMuestra,condicion=consMuestra,name=name)

@app.route("/aceleracion", methods=["GET", "POST"])
def ace():
    global horaMuestra
    global glucoMuestra
    global name
    cambio = derivada(horaMuestra, glucoMuestra)
    aceleracion = derivada(horaMuestra, cambio)
    maximo = round(max(aceleracion),4)
    minimo = round(min(aceleracion),4)
    return render_template("aceleracion.html",maximo=maximo,minimo=minimo,name=name)

@app.route("/promedio", methods=["GET", "POST"])
def pro():
    global horaMuestra
    global glucoMuestra
    global name

    for i in range(1,len(horaMuestra)):
        for j in range(0,len(horaMuestra)-i):
            if(horaMuestra[j] > horaMuestra[j+1]):
                k = horaMuestra[j+1]
                horaMuestra[j+1] = horaMuestra[j]
                horaMuestra[j] = k
    for i in range(1,len(glucoMuestra)):
        for j in range(0,len(glucoMuestra)-i):
            if(glucoMuestra[j] > glucoMuestra[j+1]):
                k = glucoMuestra[j+1]
                glucoMuestra[j+1] = glucoMuestra[j]
                glucoMuestra[j] = k
    integr=TrapecioM(horaMuestra,glucoMuestra)
    res=round(integr/(max(horaMuestra)-min(horaMuestra)),4)
    return render_template("promedio.html",res=res,name=name)

@app.route("/meta", methods=["GET", "POST"])
def met():
    global data
    global date1
    global date2
    global name
    muestra = data.muestraMeta(date1, date2)
    horaMuestra=[]
    glucoMuestra=[]
    for i in range(len(muestra)):
        horaMuestra.append(muestra[i][2])
        glucoMuestra.append(muestra[i][1])
    meta = 0 
    if request.method == "POST":
        meta = request.form['meta']
        meta = int(meta)
    tiempo=LagrangePol(glucoMuestra,horaMuestra,meta)
    return render_template("meta.html",tiempo=round(tiempo),name=name)

@app.route("/tendencia", methods=["GET", "POST"])
def ten():
    global horaMuestra
    global glucoMuestra
    global name
    (a,b,r2)=reglin(horaMuestra,glucoMuestra)
    text=grafreglin(horaMuestra,glucoMuestra,(a,b,r2))
    imagen(horaMuestra,glucoMuestra,text[1],text[0])
    return render_template("tendencia.html",r2=round(r2, 4),name=name)

@app.route("/resumen", methods=["GET", "POST"])
def res():
    global data
    global glucoData
    global date1
    global date2
    global name
    glucoData = []
    todos = data.MuestraTodos(date1,date2)
    for i in range(len(todos)):
        glucoData.append(todos[i][1])
    media=Media(glucoData)
    mediana=Mediana(glucoData)
    moda=Moda(glucoData)
    maximo=Maximo(glucoData)
    minimo=Minimo(glucoData)
    desviacion=Desviacion(glucoData)
    
    fig=plt.figure()
    plt.hist(x=glucoData, color='#F2AB6D', rwidth=0.85)

    # configuramos
    plt.xlabel('Cantidad de Glucosa en la sangre')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de cantida de Glucosa')

    ruta = str(pathlib.Path(__file__).parent.resolve()) # Obtiene la ruta del directorio 
    ruta = ruta.replace(chr(92),'/')+'/static/grafica.png' # Ruta final con el nombre del archivo
    fig.savefig(ruta)
    
    return render_template("resumen.html",media=round(media,4),mediana=mediana,moda=moda[0],maximo=maximo,minimo=minimo,desviacion=round(desviacion,4),name=name)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
