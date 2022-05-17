from flask import Flask, render_template, request, url_for, redirect
from jinja2 import Template, FileSystemLoader, Environment
from Dual import Ingreso

domain = "0.0.0.0:5000/"
templates = FileSystemLoader('templates')
environment = Environment(loader = templates)

app = Flask(__name__)

global titulos_primal
titulos_primal = []
global valores_primal
valores_primal = []
global titulos_primal_pvalores_primal_p
titulos_primal_pvalores_primal_p = []
global titulos_dual
titulos_dual = []
global valores_dual
valores_dual = []
global titulos_dual_p
titulos_dual_p = []
global valores_dual_p
valores_dual_p = []
global contar
contar = 1
global valx
valx = 0 
global valy
valy = 0 
global resx
resx = 0 
global resy
resy = 0 
global oper
oper = 0 
global res
res = 0 
global valxr
valxr = []
global valyr
valyr = []
global resr
resr = []
global resur
resur = [] 

@app.route("/funcion", methods=["GET", "POST"])
def register(): 
    if request.method == "POST":
        global valx, valy, resx, resy, oper, res
        valx = float(request.form['valx'])
        valy = float(request.form['valy'])
        resx = float(request.form['resx'])
        resy = float(request.form['resy'])
        oper = float(request.form['oper'])
        res = int(request.form['res'])

        return redirect("/restr", 301)
    return render_template("Principal.html")

@app.route("/restr", methods=["GET", "POST"])
def ta():
    mssg = "Agregar"
    if request.method == "POST":
        global valxr, valyr, resr, resur, contar, titulos_primal,valores_primal,titulos_primal_p,valores_primal_p,titulos_dual,valores_dual,titulos_dual_p,valores_dual_p
        if contar == 1:
            valxr = []
            valyr = []
            resr = []
            resur = []
        contar = contar + 1
        valxr.append(float(request.form['valxr']))
        valyr.append(float(request.form['valyr']))
        resr.append(request.form['resr'])
        resur.append(float(request.form['resur']))

        if contar < res:
            mssg = "Agregar"
            return render_template("Restricciones.html",mssg=mssg, contar=contar)
        elif contar == res:
            mssg = "Finalizar"
            return render_template("Restricciones.html",mssg=mssg, contar=contar)
        else:
            contar = 1
            titulos_primal,valores_primal,titulos_primal_p,valores_primal_p,titulos_dual,valores_dual,titulos_dual_p,valores_dual_p = Ingreso(res,oper,resr,valxr,valyr,resur,valx,valy,resx,resy)
            
            return redirect("/resultado", 301)
    return render_template("Restricciones.html",mssg=mssg, contar=contar)


@app.route("/resultado", methods=["GET", "POST"])
def resultado():
    global titulos_primal,valores_primal,titulos_primal_p,valores_primal_p,titulos_dual,valores_dual,titulos_dual_p,valores_dual_p
    return render_template("Resultados.html", titulos_primal=titulos_primal,valores_primal=valores_primal,titulos_primal_p=titulos_primal_p,valores_primal_p=valores_primal_p,titulos_dual=titulos_dual,valores_dual=valores_dual,titulos_dual_p=titulos_dual_p,valores_dual_p=valores_dual_p)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)