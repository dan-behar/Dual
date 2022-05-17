def Ingreso(cant_ecuaciones, problema, signos, vector_x, vector_y, vector_r, X_Intro, Y_Intro, Sig_x, Sig_y):    
    """
    Esta funcion recibe los parametros necesarios para construir las matrices primal y dual
    args:
        cant_ecuaciones (int): cantidad de ecuaciones
        problema (int): 1 si es max y 0 si es min
        signos (int): 1 si es >=, -1 si es <= y 0 si es indif
        vector_x (arr): agarra las x de las restricciones
        vector_y (arr): agarra las y de las restricciones
        vector_r (arr): agarra los resultados de las restricciones
        Intro_X (int): el coeficiente de X
        Intro_Y (int): el coeficiente de Y
        Sig_X (arr): signo de X, 1 si es <=, -1 si es >= y 0 si es =
        Sig_Y (arr): signo de Y, 1 si es <=, -1 si es >= y 0 si es =
    returns: (todos son arrays)
        titulos_primal: titulos del primal
        valores_primal: valores de la primal 
        titulos_primal_p: titulos de los precios sombra del primal
        valores_primal_p: valores sombre de la primal 
        titulos_dual: titulos del dual
        valores_dual: valores del dual
        titulos_dual_p: titulos de los precios sombra del dual
        valores_dual_p: valores sombre del dual
    """    
    cant_variables = 2
    cant_ecuacionesH = cant_ecuaciones

    if cant_ecuaciones >= cant_variables:
        variables = []
        variables.append(['/','x','y','R'])
        s = 0
        var_apar = 1
        extras = 0
        while s < len(signos): # guardo el signo. Si es <= uso s y si es >= uso a.
            t = signos[s]
            s = s + 1
            if t == "<=":
                variables[0].append(f's{var_apar}')
                var_apar = var_apar + 1
            elif t == ">=":
                variables[0].append(f'a{var_apar}')
                variables[0].append(f'A{var_apar}')
                cant_ecuacionesH = cant_ecuacionesH + 1
                extras = extras + 1
                var_apar = var_apar + 1
            else:
                if problema == 1: #maximización quedan igual los signos
                    variables[0].append(f'A{var_apar}')
                    var_apar = var_apar + 1
                else: #minimizacieon cambio el signo
                    variables[0].append(f'A{var_apar}')
                    var_apar = var_apar + 1
        r = 1
        # Ingreso de variables de coeficiente
        extras2 = 0
        flagss = 0
        #ahora sera el + 3 para meter laa parte de la restriccion de signo pero de las variables. 
        while r != (cant_ecuacionesH + 2): #guardo los datos de la matriz y asigno los valores a las variables slack y las varaiblas a, con 1 y -1 respectivamente.
            dif = (cant_ecuacionesH + 2) - r
            if (dif != 1):
                t = variables[0][cant_variables+r+1]
                if flagss == 0 and r > 1:
                    extras2 = extras2 + 1
                    r2 = r - extras2
                else:
                    r2 = r - extras2
                flagss = 0
                if t.find("a") != -1 or t.find("s") != -1:
                    variables.append([t])
                    flagss = 1
                else:
                    ante = cant_variables+r
                    if t.find("A") != -1 and variables[0][ante].find("a") == -1:
                        variables.append([t])
                        flagss = 1
                    else:
                        flagss = 0
                if flagss == 1:
                    s = 1
                    while s <= (cant_variables + cant_ecuacionesH + 2):
                        if s <= (cant_variables + 1):
                            variables[r2].append(float(vector_x[r2-1]))
                            variables[r2].append(float(vector_y[r2-1]))
                            variables[r2].append(float(0))
                            s = cant_variables + 2
                        elif(s <= (cant_variables + cant_ecuacionesH + 1)): 
                            x = variables[0][s]
                            s = s + 1
                            if t == x:
                                if x.find('s') != -1:
                                    u = 1
                                    variables[r2].append(u)
                                elif x.find('a') != -1:
                                    u = -1
                                    variables[r2].append(u)
                                elif x.find('A') != -1:
                                    u = 1
                                    variables[r2].append(u)
                                else:
                                    pass
                            else:
                                if x.find("A") != -1:
                                    ante = variables[0][s - 2]
                                    if ante.find("a") != -1:
                                        if t == ante:
                                            u = 1
                                            variables[r2].append(u)
                                        else:
                                            u = 0
                                            variables[r2].append(u)
                                    else:
                                        u = 0
                                        variables[r2].append(u)
                                else:
                                    u = 0
                                    variables[r2].append(u)
                        else:
                            resul = float(vector_r[r2-1])
                            if resul < 0:
                                u = 1
                                tope = len(variables[0])
                                while u < (tope):
                                    if u <= cant_variables + 1:
                                        variables[r2][u] = variables[r][u] * -1
                                        u = u + 1
                                    else:
                                        if variables[r2][u] == 1: # Es una s o una A(pero esta A debe de ser de un igual solamente)
                                            titulo = variables[0][u]
                                            bus = titulo.find("A")
                                            if bus != -1: #la unica forma de encontrar una A es que sea de un igual. porque antes va un a y en teoría la borro y la convierto en D
                                                pass
                                            else:# entonces es una s o D
                                                bus = titulo.find("D")
                                                if bus != -1:
                                                    pass #nada porque es una eliminada
                                                else: #como no es una D, es una s. Debo hacer: cambiar de s -> a, generar una A al final de la matriz. 
                                                    variables[r2][u] = variables[r2][u]
                                                    # paso de 1 a -1
                                                    variables[0][u] = f"a{titulo[1]}"
                                                    variables[r2][0] = variables[0][u]
                                                    variables[0].append(f"A{titulo[1]}")
                                                    z = 1
                                                    while z != (cant_ecuaciones + 1):
                                                        if z == r2:
                                                            variables[r2].append(1.0)
                                                        else:
                                                            variables[r2].append(0.0)
                                                    z = z + 1
                                            u = u + 1
                                        elif variables[r2][u] == -1: #entonces encontré una (a)
                                            variables[r2][u] = variables[r2][u] * -1 # paso de 1 a -1
                                            variables[0][u] = f"s{titulo[1]}"
                                            variables[r2][0] = variables[0][u]
                                            variables[0][u+1] = f"D{titulo[1]}"
                                            borroA = 1
                                            while borroA != (cant_ecuaciones + 1):
                                                variables[borroA][u+1] = 0
                                                borroA = borroA + 1
                                            u = u + 1
                                        else:
                                            u = u + 1
                                resul = resul * -1
                                variables[r2][cant_variables + 1] = (resul)
                            else:
                                variables[r2][cant_variables + 1] = (resul) 
                                s = s + 1
                r = r + 1
            else:
                variables.append(['Z'])
                s = 1
                b = r - extras
                while s < (len(variables[0])):
                    if s <= cant_variables:
                        Var_X = float(X_Intro)
                        if problema == 0:
                            Var_X = Var_X * -1
                        Var_X = Var_X * -1
                        variables[r - extras].append(Var_X)
                        #----------
                        Var_Y = float(Y_Intro)
                        if problema == 0:
                            Var_Y = Var_Y * -1
                        Var_Y = Var_Y * -1
                        variables[r - extras].append(Var_Y)
                        s = cant_variables + 1
                    elif(s > cant_variables + 1): 
                        x = variables[0][s]
                        if x.find('A') != -1:
                            variables[r - extras].append(1000000)
                            s = s + 1
                        else:
                            variables[r - extras].append(0)
                            s = s + 1
                    else:
                        variables[r - extras].append(0)  
                        s = s + 1
                r = r + 1
        vector_signos = [Sig_x, Sig_y]


        variables_DUAL = []
        variables_DUAL.append(['/'])
        vaas = 1
        var_apar = 1
        extras = 0
        cant_ecuacionesHD = len(vector_signos)
        cant_ecuacionesD = len(vector_signos)
        cant_variablesD = cant_ecuaciones
        while vaas <= (cant_ecuaciones + 2): # guardo el nombre de las variables.Si es <= uso s y si es >= uso a. 
            if vaas <= cant_ecuaciones:
                for i in range(cant_ecuaciones):
                    num = i + 1
                    ingresos_ = f"y{num}"
                    variables_DUAL[0].append(ingresos_)
                vaas = cant_ecuaciones + 1
            elif vaas == (cant_ecuaciones + 1):
                variables_DUAL[0].append('R')
                vaas = vaas + 1
            else:
                vaas = vaas + 1
                for t in vector_signos:
                    if t == -1:
                        if problema == 1:
                            variables_DUAL[0].append(f's{var_apar}')
                            var_apar = var_apar + 1
                        else:
                            variables_DUAL[0].append(f'a{var_apar}')
                            variables_DUAL[0].append(f'A{var_apar}')
                            cant_ecuacionesHD = cant_ecuacionesHD + 1
                            extras = extras + 1
                            var_apar = var_apar + 1
                    elif t == 1:
                        if problema == 1:
                            variables_DUAL[0].append(f'a{var_apar}')
                            variables_DUAL[0].append(f'A{var_apar}')
                            cant_ecuacionesHD = cant_ecuacionesHD + 1
                            extras = extras + 1
                            var_apar = var_apar + 1
                        else:
                            variables_DUAL[0].append(f's{var_apar}')
                            var_apar = var_apar + 1
                    else:
                        if problema == 1: #maximización quedan igual los signos
                            variables_DUAL[0].append(f'A{var_apar}')
                            var_apar = var_apar + 1
                        else: #minimizacieon cambio el signo
                            variables_DUAL[0].append(f'A{var_apar}')
                            var_apar = var_apar + 1
        r = 1
        extras2 = 0
        flagss = 0
        #ahora sera el + 3 para meter laa parte de la restriccion de signo pero de las variables. 

        columna_D = 0
        while r != (cant_ecuacionesHD + 2): #guardo los datos de la matriz y asigno los valores a las variables slack y las varaiblas a, con 1 y -1 respectivamente.
            dif = (cant_ecuacionesHD + 2) - r
            if (dif != 1):
                t = variables_DUAL[0][cant_variablesD+r+1]
                if flagss == 0 and r > 1:
                    extras2 = extras2 + 1
                    r2 = r - extras2
                else:
                    r2 = r - extras2
                flagss = 0
                if t.find("a") != -1 or t.find("s") != -1:
                    variables_DUAL.append([t])
                    flagss = 1
                else:
                    ante = cant_variablesD+r
                    if t.find("A") != -1 and variables_DUAL[0][ante].find("a") == -1:
                        variables_DUAL.append([t])
                        flagss = 1
                    else:
                        flagss = 0
                if flagss == 1:
                    s = 1
                    fila_D = 1
                    columna_D = columna_D + 1
                    while s <= (cant_variablesD + cant_ecuacionesHD + 2):
                        if s <= cant_variablesD:
                            variables_DUAL[r2].append(variables[fila_D][columna_D])
                            fila_D = fila_D + 1
                            s = s + 1
                        elif(s != (cant_variablesD + 1) and s <= (cant_variablesD + cant_ecuacionesHD + 1)): 
                            x = variables_DUAL[0][s]
                            s = s + 1
                            if t == x:
                                if x.find('s') != -1:
                                    u = 1
                                    variables_DUAL[r2].append(u)
                                elif x.find('a') != -1:
                                    u = -1
                                    variables_DUAL[r2].append(u)
                                elif x.find('A') != -1:
                                    u = 1
                                    variables_DUAL[r2].append(u)
                                else:
                                    pass
                            else:
                                if x.find("A") != -1:
                                    ante = variables_DUAL[0][s - 2]
                                    if ante.find("a") != -1:
                                        if t == ante:
                                            u = 1
                                            variables_DUAL[r2].append(u)
                                        else:
                                            u = 0
                                            variables_DUAL[r2].append(u)
                                    else:
                                        u = 0
                                        variables_DUAL[r2].append(u)
                                else:
                                    u = 0
                                    variables_DUAL[r2].append(u)
                        elif s == cant_variablesD + 1:
                            variables_DUAL[r2].append(0)
                            s = s + 1
                        else:
                            resul = variables[fila_D][columna_D]
                            if problema == 1:
                                resul = resul * -1
                            else:
                                pass 
                            fila_D = fila_D + 1
                            if resul < 0:
                                u = 1
                                tope = len(variables_DUAL[0])
                                while u < (tope):
                                    if u <= cant_variablesD + 1:
                                        variables_DUAL[r2][u] = variables_DUAL[r][u] * -1
                                        u = u + 1
                                    else:
                                        if variables_DUAL[r2][u] == 1: # Es una s o una A(pero esta A debe de ser de un igual solamente)
                                            titulo = variables_DUAL[0][u]
                                            bus = titulo.find("A")
                                            if bus != -1: #la unica forma de encontrar una A es que sea de un igual. porque antes va un a y en teoría la borro y la convierto en D
                                                pass
                                            else:# entonces es una s o D
                                                bus = titulo.find("D")
                                                if bus != -1:
                                                    pass #nada porque es una eliminada
                                                else: #como no es una D, es una s. Debo hacer: cambiar de s -> a, generar una A al final de la matriz. 
                                                    variables_DUAL[r2][u] = variables_DUAL[r2][u]
                                                    # paso de 1 a -1
                                                    variables_DUAL[0][u] = f"a{titulo[1]}"
                                                    variables_DUAL[r2][0] = variables_DUAL[0][u]
                                                    variables_DUAL[0].append(f"A{titulo[1]}")
                                                    z = 1
                                                    while z != (cant_ecuacionesD + 1):
                                                        if z == r2:
                                                            variables_DUAL[r2].append(1.0)
                                                        else:
                                                            variables_DUAL[r2].append(0.0)
                                                        z = z + 1
                                            u = u + 1
                                        elif variables_DUAL[r2][u] == -1: #entonces encontré una (a)
                                            variables_DUAL[r2][u] = variables_DUAL[r2][u] * -1 # paso de 1 a -1
                                            variables_DUAL[0][u] = f"s{titulo[1]}"
                                            variables_DUAL[r2][0] = variables_DUAL[0][u]
                                            variables_DUAL[0][u+1] = f"D{titulo[1]}"
                                            borroA = 1
                                            while borroA != (cant_ecuacionesD + 1):
                                                variables_DUAL[borroA][u+1] = 0
                                                borroA = borroA + 1
                                            u = u + 1
                                        else:
                                            u = u + 1
                                resul = resul * -1
                                variables_DUAL[r2][cant_variablesD + 1] = (resul)
                            else:
                                variables_DUAL[r2][cant_variablesD + 1] = (resul) 
                            s = s + 1
                r = r + 1
            else:
                variables_DUAL.append(['Z'])
                s = 1
                b = r - extras
                fila_D = 1
                while s < (len(variables_DUAL[0])):
                    if s <= cant_variablesD:
                        n = variables[fila_D][columna_D+1]
                        fila_D = 1 + fila_D
                        if problema == 1:
                            n = n * -1
                        n = n * -1
                        variables_DUAL[r - extras].append(n)
                        s = s + 1
                    elif(s > cant_variablesD + 1): 
                        x = variables_DUAL[0][s]
                        if x.find('A') != -1:
                            variables_DUAL[r - extras].append(1000000)
                            s = s + 1
                        else:
                            variables_DUAL[r - extras].append(0)
                            s = s + 1
                    else:
                        variables_DUAL[r - extras].append(0)  
                        s = s + 1
                r = r + 1
        Simplex_P(variables,cant_ecuaciones,variables_DUAL,cant_ecuacionesD,cant_variables,problema)
        Simplex_D(variables_DUAL,cant_ecuacionesD,cant_variablesD,problema)
        #Primal
        titulos_primal = []
        valores_primal = []
        for x in range(len(variables)):
            titulos_primal.append(variables[x][0])
            if variables[x][cant_variables + 1] != "R":
                valores_primal.append(int(variables[x][cant_variables + 1]))
            else:
                valores_primal.append(variables[x][cant_variables + 1])
        var = 0
        x = variables[0]
        titulos_primal_p = []
        valores_primal_p = []
        for xs in range(len(x)):
            voy = x[xs]
            atras = x[xs-1]
            if (voy.find('a') != -1 or voy.find('s') != -1):
                if variables[-1][xs] > 1000000:
                    titulos_primal_p.append(variables[0][xs])
                    valores_primal_p.append(int(1000000 - variables[-1][xs]))
                else:
                    titulos_primal_p.append(variables[0][xs])
                    valores_primal_p.append(int(variables[-1][xs]))
            elif (voy.find('A') != -1 and atras.find('A') != -1):
                if variables[-1][xs] < 1000000:
                    titulos_primal_p.append(variables[0][xs])
                    valores_primal_p.append(int(1000000 - variables[-1][xs]))
                else:
                    titulos_primal_p.append(variables[0][xs])
                    valores_primal_p.append(int(variables[-1][xs]))
        #Dual
        variables_DUAL[cant_ecuacionesD+1][cant_variablesD+1] = variables_DUAL[cant_ecuacionesD+1][cant_variablesD+1]*-1
        titulos_dual = []
        valores_dual = []
        for x in range(len(variables_DUAL)):
            titulos_dual.append(variables_DUAL[x][0])
            if variables_DUAL[x][cant_variablesD + 1] != "R":
                valores_dual.append(int(variables_DUAL[x][cant_variablesD + 1]))
            else:
                valores_dual.append(variables_DUAL[x][cant_variablesD + 1])
        var = 0
        x = variables_DUAL[0]
        titulos_dual_p = []
        valores_dual_p = []
        for xs in range(len(x)):
            voy = x[xs]
            atras = x[xs-1]
            if voy.find('a') != -1 or voy.find('s') != -1:
                if variables_DUAL[-1][xs] < 1000000:
                    titulos_dual_p.append(variables_DUAL[0][xs])
                    valores_dual_p.append(int(variables_DUAL[-1][xs]))
                else:
                    titulos_dual_p.append(variables_DUAL[0][xs])
                    valores_dual_p.append(int(variables_DUAL[-1][xs]- 1000000))
            elif (voy.find('A') != -1 and atras.find('A') != -1):
                if variables_DUAL[-1][xs] < 1000000:
                    titulos_dual_p.append(variables_DUAL[0][xs])
                    valores_dual_p.append(int(variables_DUAL[-1][xs]))
                else:
                    titulos_dual_p.append(variables_DUAL[0][xs])
                    valores_dual_p.append(int(variables_DUAL[-1][xs]- 1000000))
        return titulos_primal,valores_primal,titulos_primal_p,valores_primal_p,titulos_dual,valores_dual,titulos_dual_p,valores_dual_p


def Simplex_P(variables,cant_ecuaciones,variables_DUAL,cant_ecuacionesD,cant_variables,problema):
    """
    Esta funcion recibe los parametros necesarios para operar simplex primal y mueve las M de todas
    args:
        variables (arr): matriz primal
        cant_ecuaciones (int): cantidad de ecuaciones primal
        variables_dual (arr): matriz dual
        cant_ecuacionesD (int): cantidad de ecuaciones dual
        cant_variables (int): cantidad de variables en total
        problema (int): 1 si es max y 0 si es min
    returns: 
        solo opera en los arrays, no retorna nada
    """   
    var = 0
    x = variables[0]
    for xs in range(len(x)):
        verS = x[xs]
        if verS.find('A') != -1:
            columna_A = xs
            p = 1 
            while p <= cant_ecuaciones:
                if variables[p][columna_A] == 1: # si es 1, encontre la fila. p es la fila.
                    ar_res = []
                    p2 = 1
                    while p2 < len(variables[0]):
                        resta = (variables[p][p2] * variables[-1][columna_A])
                        variables[-1][p2] = variables[-1][p2] - resta
                        p2 = p2 + 1
                    p = p + 1
                else:
                    p = p + 1
        else:
            pass
    var = 0
    x = variables_DUAL[0]
    for xs in range(len(x)):
        verS = x[xs]
        if verS.find('A') != -1:
            columna_A = xs
            p = 1 
            while p <= cant_ecuacionesD:
                if variables_DUAL[p][columna_A] == 1: # si es 1, encontre la fila. p es la fila.
                    ar_res = []
                    p2 = 1
                    while p2 < len(variables_DUAL[0]):
                        resta = (variables_DUAL[p][p2] * variables_DUAL[-1][columna_A])
                        variables_DUAL[-1][p2] = variables_DUAL[-1][p2] - resta
                        p2 = p2 + 1
                    p = p + 1
                else:
                    p = p + 1
        else:
            pass


    s_top = 0
    while(s_top != 1):
        track = variables[-1][1:(cant_variables+1)]
        track2 = variables[-1][(cant_variables+2):]
        for t in track2:
            track.append(t)
        pivote = min(track)
        if pivote < 0:
            pos_piv = variables[-1].index(pivote)
            col_vdivpc = []
            fila = 1
            while(fila <= cant_ecuaciones):
                value = variables[fila][cant_variables+1]
                pivot_colum = variables[fila][pos_piv]
                if pivot_colum > 0 and value != 0:
                    v = value/pivot_colum
                    col_vdivpc.append(v)
                else:
                    col_vdivpc.append(100000000.0)
                fila = fila + 1
            clave = col_vdivpc[0]
            for i in range(1,len(col_vdivpc)):
                clave = min(clave, col_vdivpc[i])
            if clave == 100000000.0:
                break
            fila_clave =  col_vdivpc.index(clave) + 1
            op_arr = 1
            #CAMBIAR FILA CLAVE
            s_top_col = 1
            fac_div_clave = variables[fila_clave][pos_piv]
            while s_top_col < (len(variables[0])):
                variables[fila_clave][s_top_col] = variables[fila_clave][s_top_col] / fac_div_clave
                s_top_col = s_top_col + 1
            variables[fila_clave][0] = variables[0][pos_piv]
            while op_arr <= cant_ecuaciones+1:
                if fila_clave != op_arr:
                    piv_col_n = variables[op_arr][pos_piv]
                    if piv_col_n != 0:# debo restarle la columna clave por su piv_col_n
                        s_top_col = 1
                        ar_res = []
                        while s_top_col < (len(variables[0])):
                            ar_res.append(variables[fila_clave][s_top_col] * piv_col_n)
                            s_top_col = s_top_col + 1 
                        s_top_col = 1
                        while s_top_col < (len(variables[0])):
                            variables[op_arr][s_top_col] = variables[op_arr][s_top_col] - ar_res[s_top_col-1]
                            s_top_col = s_top_col + 1 
                        op_arr = op_arr + 1
                    else:
                        op_arr = op_arr + 1
                        pass # esa fila no cambia, se queda igual
                else:
                    op_arr = op_arr + 1
        else:
            s_top = 1 #hasta que todas las variables(no S ni A) sean no negativas  

    if problema == 0:
        variables[-1][cant_variables + 1] = variables[-1][cant_variables + 1] * -1 

def Simplex_D(variables_DUAL,cant_ecuacionesD,cant_variablesD,problema):
  s_top = 0
  while(s_top != 1):
    track = variables_DUAL[-1][1:(cant_variablesD+1)]
    track2 = variables_DUAL[-1][(cant_variablesD+2):]
    for t in track2:
      track.append(t)
    pivote = min(track)
    if pivote < 0:
      pos_piv = variables_DUAL[-1].index(pivote)
      col_vdivpc = []
      fila = 1
      while(fila <= cant_ecuacionesD):
        value = variables_DUAL[fila][cant_variablesD+1]
        pivot_colum = variables_DUAL[fila][pos_piv]
        if pivot_colum > 0 and value != 0:
          v = value/pivot_colum
          col_vdivpc.append(v)
        elif pivot_colum < 0 or value < 0:
          v = value/pivot_colum
          col_vdivpc.append(v)
        else:
          col_vdivpc.append(100000000.0)
        fila = fila + 1
      clave = col_vdivpc[0]
      for i in range(1,len(col_vdivpc)):
        clave = min(clave, col_vdivpc[i])
      #AQUI VA LO DE BUSCAR LA QUE GENERE MENOS NEGATIVOS
      #...
      #----------
      if clave == 100000000.0:
        break
      fila_clave =  col_vdivpc.index(clave) + 1
      op_arr = 1
      #CAMBIAR FILA CLAVE
      s_top_col = 1
      fac_div_clave = variables_DUAL[fila_clave][pos_piv]
      while s_top_col < (len(variables_DUAL[0])):
        variables_DUAL[fila_clave][s_top_col] = variables_DUAL[fila_clave][s_top_col] / fac_div_clave
        s_top_col = s_top_col + 1
      variables_DUAL[fila_clave][0] = variables_DUAL[0][pos_piv]
      while op_arr <= cant_ecuacionesD+1:
        if fila_clave != op_arr:
          piv_col_n = variables_DUAL[op_arr][pos_piv]
          if piv_col_n != 0:# debo restarle la columna clave por su piv_col_n
            s_top_col = 1
            ar_res = []
            while s_top_col < (len(variables_DUAL[0])):
              ar_res.append(variables_DUAL[fila_clave][s_top_col] * piv_col_n)
              s_top_col = s_top_col + 1 
            s_top_col = 1
            while s_top_col < (len(variables_DUAL[0])):
              variables_DUAL[op_arr][s_top_col] = variables_DUAL[op_arr][s_top_col] - ar_res[s_top_col-1]
              s_top_col = s_top_col + 1 
            op_arr = op_arr + 1
          else:
            op_arr = op_arr + 1
            pass # esa fila no cambia, se queda igual
        else:
          # estoy en la fila clave.
          op_arr = op_arr + 1
    else:
      s_top = 1 #hasta que todas las variables(no S ni A) sean no negativas  

  if problema == 0:
    variables_DUAL[-1][cant_variablesD + 1] = variables_DUAL[-1][cant_variablesD + 1] * -1
    """
    Esta funcion recibe los parametros necesarios para operar simplex primal y mueve las M de todas
    args:
        variables_dual (arr): matriz dual
        cant_ecuacionesD (int): cantidad de ecuaciones dual
        cant_variablesD (int): cantidad de variables dual
        problema (int): 1 si es max y 0 si es min
    returns: 
        solo opera en los arrays, no retorna nada
    """ 