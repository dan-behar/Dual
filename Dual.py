def Ingreso(cant_ecuaciones, problema, signos, vector_x, vector_y, vector_r, X_Intro, Y_Intro, Sig_x, Sig_y):    
    cant_variables = 2
    "cant_ecuaciones = 0 DEBE VENIR DE LA FUNCION"
    cant_ecuacionesH = cant_ecuaciones
    """
    problema = 0 #DEBE VENIR DE LA FUNCION
    signos = [] #DEBE VENIR DE LA FUNCION
    vector_x = [] #DEBE VENIR DE LA FUNCION
    vector_y = [] #DEBE VENIR DE LA FUNCION
    vector_r = [] #DEBE VENIR DE LA FUNCION
    X_Intro = 0 #DEBE VENIR DE LA FUNCION, VALOR X DE LA OBJETIVO
    Y_Intro = 0 #DEBE VENIR DE LA FUNCION, VALOR Y DE LA OBJETIVO
    Sig_x = 0 #DEBE VENIR DE LA FUNCION
    Sig_y = 0 #DEBE VENIR DE LA FUNCION
    """

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
                #print('Ingrese la funcion objetivo en termino de las n variables especificadas.')
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

def DualOp():
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
            variables_DUAL[0].append(input(f"Ingrese la variables No.{vaas}:  "))
            vaas = vaas + 1
        elif vaas == (cant_ecuaciones + 1):
            variables_DUAL[0].append('R')
            vaas = vaas + 1
        else:
            vaas = vaas + 1
            for t in vector_signos:
                print(t)
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
                    print(variables[fila_D][columna_D+1])
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