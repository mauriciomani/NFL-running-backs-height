# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 10:55:26 2018

@author: Mauricio Mani
"""


from requests import get
from bs4 import BeautifulSoup
from time import time
from random import randint
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.style as style
from scipy import stats 
import numpy as np
import math
import pandas as pd
from statsmodels.stats.diagnostic import kstest_normal

#Convierte la altura de pie a metro. 
def pie_metro(x):
    if x =='5-6 ':
        y = 167.5
    elif x =='5-7 ':
        y = 170
    elif x == '5-8 ':
        y = 172.5
    elif x == '5-9 ':
        y = 175
    elif x== '5-10':
        y = 177.5
    elif x== '5-11':
        y = 180
    elif x =='6-0 ':
        y = 182.88
    elif x == '6-1 ':
        y = 185.928
    elif x == '6-2 ':
        y = 188.976
    elif x == '6-3 ':
        y = 192.024
    elif x == '6-4 ':
        y = 195.072
    elif x == '6-5 ':
        y = 198.12
    elif x == '6-6 ':
        y = 201.168
    elif x == '6-7 ':
        y = 204.216
    else:
        y = 'NaN'
    return(y)

#Extrae todos los runningbacks historicos de la pagina de la NFL.
def links_tabla(i):
    pedidos = 1
    altura = []
    pesos = []
    data = []
    diccionario = {}
    names = []
    years = []
    tot_yards = []
    inicio = time()
    url = 'http://www.nfl.com/players/search?category=position&playerType=historical&conference=ALL&d-447263-p=' + str(i) +'&filter=runningback'
    response = get(url)
    soup=BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', id="result")
    for link in table.find_all('a', href=True):
        respuesta = get('http://www.nfl.com' + link['href'])
        espera = time() - inicio
        print('Pedido: {}, Frequencia: {} pedidos'.format(pedidos, pedidos/espera))
        html_soup=BeautifulSoup(respuesta.text, 'html.parser')
        info = html_soup.find('div', class_='player-info').text
        alt = info.find('Height: ')
        altura.append(pie_metro(info[alt+8:alt+12]))
        pes = info.find('Weight:')
        peso = info[pes+7:pes+11]
        pesos.append(peso)
        pedidos +=1
        #Este tiempo se puede cambiar 
        sleep(randint(2,9))
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    for dat in data:
        year1, year2 = int(dat[2][0:4]), int(dat[2][7:11])
        year = round((year2 -year1) / 2)
        year = year1 + year
        names.append(dat[0])        
        years.append(year)
        tot_yards.append(dat[6])
    diccionario['Nombre'] = names
    diccionario['Año'] = years
    diccionario['Peso'] = pesos
    diccionario['Altura'] = altura
    diccionario['Yardas_totales'] = tot_yards
    df = pd.DataFrame.from_dict(diccionario)
    return(df)

#Extrae de la pagina de la NFL todos los runningbacks que juegan hoy en dia. 
def RB_2017(i):    
    pedidos = 1
    altura = []
    pesos = []
    data = []
    diccionario = {}
    names = []
    status = []
    yards = []
    positions = []
    inicio = time()
    url = 'http://www.nfl.com/players/search?category=position&playerType=current&d-447263-p=' + str(i) +'&conference=ALL&filter=runningback'
    response = get(url)
    soup=BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', id="result")
    for link in table.find_all('a', href=True):
        if (link['href'])[0:6] == '/teams':
            pass
        else:
            respuesta = get('http://www.nfl.com' + link['href'])
            espera = time() - inicio
            print('Pedido: {}, Frequencia: {} pedidos'.format(pedidos, pedidos/espera))
            html_soup=BeautifulSoup(respuesta.text, 'html.parser')
            info = html_soup.find('div', class_='player-info').text
            alt = info.find('Height: ')
            altura.append(pie_metro(info[alt+8:alt+12]))
            pes = info.find('Weight:')
            peso = info[pes+7:pes+11]
            pesos.append(peso)
            pedidos +=1
            #Este tiempo se puede cambiar 
            sleep(randint(2,9))
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    for dat in data:
        names.append(dat[2])        
        status.append(dat[3])
        yards.append(dat[7])
        positions.append(dat[0])
    diccionario['Nombre'] = names
    diccionario['Status'] = status
    diccionario['Peso'] = pesos
    diccionario['Altura'] = altura
    diccionario['Yardas'] = yards
    diccionario['Posicion'] = positions
    df = pd.DataFrame.from_dict(diccionario)
    return(df)

#Grafica 11 imagenes conteniendo la informacion de peso y altura a través de las decadas. 
def graficar_tiempo(lista, df):
    print(df.loc[df['Peso']>275])
    plt.style.use('ggplot')
    espacio = ' '
    titulos = []
    n = 0
    e = [año for año in range(1920, 2011, 10)]
    e.append(2016)
    for i in e:
        try:
            titulos.append(str(e[n])+ ' - ' + str(e[n+1]))
        except IndexError:
            break
        n += 1
    titulos.append(2017)
    n = 0
    for i in lista:
        fig = plt.figure(figsize = (13, 7))
        ax = fig.add_subplot(111)
        plt.xlim(df['Altura'].min() - 1, df['Altura'].max() + 1) 
        #Ya que solo hay 10 jugadores con tan alto peso.
        plt.ylim(df['Peso'].min() - 1, 275)
        ax.scatter(x= i['Altura'], y= i['Peso'])
        titulo = titulos[n]
        print('La altura media de ' + str(titulo) + ' es: ' + str(i['Altura'].mean()))
        plt.xlabel('Altura')
        plt.ylabel('Peso')
        ax.text(x = 164.5 , y = 127,
                s = '   ©Mauricio Mani' + espacio * 170 + 'Source: NFL: www.nfl.com/players   ',
                fontsize = 10, color = '#f0f0f0', backgroundcolor = 'grey')
        ax.text(x = 162.5, y = 285, 
               s = 'Cambio en el peso y la altura de los corredores de la NFL a través del tiempo',
              fontsize = 20, weight = 'bold', alpha = .75)
        ax.text(x = 178, y = 278, s = 'Decada: ' + str(titulo), fontsize = 18, alpha = 0.85)
        #plt.savefig('Images/'+ str(titulo) + '.png')
        n +=1

#Genera boxplots e histogramas para entender el cambio de la estatura a través del tiempo.             
def entender_2017(df_2017):
    style.use('ggplot')
    altura = df_2017['Altura']
    print('Media de la estatura de los runningbacks de la temporada 2017: ')
    print(altura.loc[(df_2017['Status']=='ACT') & (df_2017['Yardas'] > 100)].mean())
    print('Mediana de la estatura de los runningbacks de la temporada 2017: ')
    print(altura.loc[(df_2017['Status']=='ACT') & (df_2017['Yardas'] > 100)].median())
    espacio = ' '
    fig = plt.figure()
    ax = fig.add_subplot(111)
    n, bins, patches = ax.hist(altura, bins = 9, color = 'orange', normed = True)
    x_min, x_max = min(bins), max(bins)
    lnspc = np.linspace(x_min, x_max, len(altura))
    mu, sigma = stats.norm.fit(altura)
    pdf = stats.norm.pdf(lnspc, mu, sigma)
    ax.plot(lnspc, pdf, color = 'dodgerblue')
    fig.subplots_adjust(bottom = 0.10)
    ax.text(x = 165, y = -0.008,
            s = '   ©Mauricio Mani' + espacio*150 + 'Source: NFL: www.nfl.com/players   ',
            fontsize = 12, color = '#f0f0f0', backgroundcolor = 'grey')
    ax.text(x = 168, y = 0.087, s = "Estatura de runningbacks activos del 2017 - NFL ",
               fontsize = 23, weight = 'bold', alpha = .75)
    ax.text(x = 167, y = 0.083, 
               s = 'Histograma de la estatura de corredores activos comparados con una distribución normal',
              fontsize = 16, alpha = .85)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    stats.probplot(altura, plot=plt)
    ax.set_title('Normal Q-Q plot')
    plt.show()
    #Prueba kolmogorov-smirnov para normailidad (bondad de ajuste), similar a Lilliefors, pero con distribución KS.
    ks, p_v = kstest_normal(altura)
    print('El valor de la prueba Kolmogorov-Smirnov es: ' + str(ks))
    print('El valor p de la prueba es: ' + str(p_v))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(altura, bins = 9, cumulative=True, normed=True, histtype = 'step', linewidth=1.4)
    cdf = stats.norm.cdf(lnspc, mu, sigma)
    ax.plot(lnspc, cdf, color = 'dodgerblue')
    plt.xlim(xmin=x_min, xmax = x_max)
    fig.subplots_adjust(bottom = 0.10)
    ax.text(x = 166, y = -0.10,
            s = '   ©Mauricio Mani' + espacio*130 + 'Source: NFL: www.nfl.com/players   ',
            fontsize = 12, color = '#f0f0f0', backgroundcolor = 'grey')
    ax.text(x = 167, y = 1.12, s = "Distribución acumulada de la estatura de corredores 2017 - NFL",
               fontsize = 21, weight = 'bold', alpha = .75)
    ax.text(x = 170, y = 1.05, 
               s = 'Para uso de la prueba de normalidad Kolmogorov-Smirnov y Lilliefors.',
              fontsize = 16, alpha = .85)
    ax.text(x = 169.5, y = 0.8, 
               s = 'Prueba Kolmogorov-Smirnov: ' + str(ks),
              fontsize = 10)
    ax.text(x = 169.5, y = 0.75, 
               s = 'P-value: ' + str(p_v),
              fontsize = 10)
    sw, sw_pv = stats.shapiro(altura)
    print('El valor de la prueba Shapiro-Wilk es: ' + str(sw))
    print('El valor p de la prueba es: ' + str(sw_pv))
    plt.show() 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.boxplot(df_2017['Altura'].loc[(df_2017['Status']=='ACT') & (df_2017['Yardas'] > 800)])
    print('Estadisticas básicas: ')
    print('Media: ')
    print(df_2017['Altura'].loc[(df_2017['Status']=='ACT') & (df_2017['Yardas'] > 800)].mean())
    print('Meidana: ')
    print(df_2017['Altura'].loc[(df_2017['Status']=='ACT') & (df_2017['Yardas'] > 800)].median())
    print('Moda: ')
    print(df_2017['Altura'].loc[(df_2017['Status']=='ACT') & (df_2017['Yardas'] > 800)].mode())
    #La mediana y la moda son muy similares.
    #El boxplot tamnien nos sirve para revisar la normalidad de un dataset.
    plt.xticks([1], ['Mas de 800 yardas'])
    fig.subplots_adjust(bottom = 0.10)
    ax.text(x = 0.5, y = 169.5,
            s = '   ©Mauricio Mani' + espacio*120 + 'Source: NFL: www.nfl.com/players   ',
            fontsize = 12, color = '#f0f0f0', backgroundcolor = 'grey')
    ax.text(x = 0.5, y = 195, s = "Entender como funcionan los diagramas de caja - Boxplot",
               fontsize = 22, weight = 'bold', alpha = .75)
    ax.text(x = 0.5, y = 193, 
               s = 'Con un ejemplo sencillo de la National Football League con la estatura de los corredores con mas\nde 800 yardas en la temporada 2017.',
              fontsize = 15, alpha = .85)
    ax.annotate(s = 'Esta es la mediana\n"NO es la media"', xy =(1.075, 180), xytext = (1.15, 180), arrowprops=dict(facecolor='red', color='red'))
    ax.annotate(s = 'Q1 o 25% de los datos', xy =(1.075, 177), xytext = (1.15, 177), arrowprops=dict(facecolor='red', color='red'))
    ax.annotate(s = 'Q3 o 75% de los datos', xy =(0.925, 182.6), xytext = (0.72, 182.6), arrowprops=dict(facecolor='red', color='red'))
    ax.annotate(s = 'Q3 + 1.5 * Rango Intercuatil', xy =(1.04, 185.9), xytext = (1.1, 185.9), arrowprops=dict(facecolor='red', color='red'))
    ax.annotate(s = 'Q1 - 1.5 * Rango Intercuartil', xy =(0.96, 172.5), xytext = (0.7, 172.5), arrowprops=dict(facecolor='red', color='red'))
    ax.annotate(s = 'Latavius Murray\nOutlier', xy =(1, 191.8), xytext = (0.85, 189), arrowprops=dict(facecolor='red', color='red'))
    return(df_2017.loc[(df_2017['Status']=='ACT') & (df_2017['Yardas'] > 800)])

#Genera una lista, requerida por otras funciones. 
#La lista contiene los dataframes de altura y peso por decada. 
def obtener_lista(df, df_2017):
    lista = []
    lista1 = []
    for año in range(1930, 2011, 10):
        lista.append(df[['Altura', 'Peso']].loc[(df['Año'] < año) & (df['Año'] >= año -10)])
        lista1.append(df['Altura'].loc[(df['Año'] < año) & (df['Año'] >= año -10)])
    lista1.append(df['Altura'].loc[(df['Año'] < 2017) & (df['Año'] >= 2010)])
    lista1.append(df_2017['Altura'])
    lista.append(df[['Altura', 'Peso']].loc[(df['Año'] < 2017) & (df['Año'] >= 2010)])
    lista.append(df_2017[['Altura', 'Peso']])
    return(lista, lista1)

#Genera un boxplot que compara las estaturas a través de las decadas.        
def graficar_estatura(lista):
    style.use('fivethirtyeight')
    plt.figure()
    ax = plt.subplot(111)
    ax.boxplot(lista)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height * 0.85])
    plt.xticks([i for i in range(1, 12)], ["20's", "30's", "40's", "50's", "60's",
                "70's", "80's", "90's", "2000's", "2010's", '2017'])   
    espacio = ' ' 
    ax.text(x = 0, y = 160,
            s = '   ©Mauricio Mani' + espacio*150 + 'Source: NFL: www.nfl.com/players   ',
            fontsize = 12, color = '#f0f0f0', backgroundcolor = 'grey')
    ax.text(x = 1, y = 208, s = "Diseñando al runningback perfecto - National Football League",
               fontsize = 23, weight = 'bold', alpha = .75)
    ax.text(x = 1, y = 203, 
               s = 'Cambio de estatura a través de tiempo en centímetros de los corredores de la National Football \n League por decadas. Desde 1920 hasta la temporada 2017. ',
              fontsize = 16, alpha = .85)
    plt.show()

#Algoritmo de prueba z-test. Genera el valor z, el valor p y los intervalos.
#No podemos usar el paired t-test por que nuestros dataset son de distinto tamaño. 
#Suponemos que las dos muestras son completamente independientes, lo cual no es del todo cierto. 
def z_test(dset1, dset2, alpha = 0.05):
    #Standar Error
    #suponemos que conocemos la desviacion estandar de la población.
    SE1 = dset1.var(ddof=0) / len(dset1)
    SE2 = dset1.var(ddof=0) / len(dset2)
    SEd = math.sqrt(SE1 + SE2)
    mean1, mean2 = dset1.mean(), dset2.mean()
    diff = mean1 - mean2
    z_stat= (mean1 - mean2) / SEd
    p_value = stats.norm.sf(abs(z_stat))*2
    z_val = stats.norm.ppf(alpha / 2)
    Upp_CI = diff + z_val * SEd
    Low_CI = diff - z_val * SEd
    #Difference between means
    #Population is normally distributed
    return(z_stat, p_value, Low_CI, Upp_CI)
 
#Imprime la informacion de la prueba z y grafica los resutados.
def prueba_hipotesis(lista):
    espacio = ' '
    style.use('ggplot')
    lista = lista[:-1]
    vein = lista[0]
    trein = lista[1]
    cuar = lista[2]
    cinc = lista[3]
    ses = lista[4]
    seten = lista[5]
    ochen = lista[6]
    nov = lista[7]
    dosm = lista[8]
    dosmd = lista[9]
    anova, p_val = stats.f_oneway(vein, trein, cuar, cinc, ses, seten, ochen, nov, dosm, dosmd)
    #Podemos concluir que a través del tiempo la altura de los corredores efectivamente ha cambiado.
    anova2, p_val2 = stats.f_oneway(trein, cuar, cinc, ses, seten, ochen)
    anova3, p_val3 = stats.f_oneway(ochen, nov, dosm, dosmd)
    z_diff_och_set = z_test(ochen, seten)
    pv1_och_set = seten.mean() + z_diff_och_set[2]
    pv2_och_set = seten.mean() + z_diff_och_set[3]
    z_diff_ses_set = z_test(ses, seten)
    pv1_ses_set = seten.mean() + z_diff_ses_set[2]
    pv2_ses_set = seten.mean() + z_diff_ses_set[3]
    mins = min(seten.min(), ochen.min())
    maxs = max(seten.max(), ochen.max())
    fig, ax = plt.subplots(3, 1, figsize = (10,60))
    print('E valor p de la prueba de hipotesis de dos muestras (independientes) en la decada de los setentas y los ochentas es: ', z_diff_och_set[1])
    print('Los intervalos de confianza de la diferencia de medias para la decada de los setentas y los ochentas son: ')
    print('LOW99CI: ', z_diff_och_set[2])
    print('HIGH99CI: ', z_diff_och_set[3])
    print('E valor p de la prueba de hipotesis de dos muestras (independientes) en la decada de los sesentas y los sesentas es: ', z_diff_ses_set[1])
    print('Los intervalos de confianza de la diferencia de medias para la decada de los sesentas y los setentas son: ')
    print('LOW99CI: ', z_diff_ses_set[2])
    print('HIGH99CI: ', z_diff_ses_set[3])
    ax[2].hist(ochen, bins = 9, alpha = 0.7, color = 'blue')
    ax[2].set_xlim([mins, maxs])
    ax[2].axvline(x=ochen.mean(), color = 'red', linewidth = 4)    
    ax[2].axvline(x=pv1_och_set, color = 'red', linestyle='--', linewidth = 4)
    ax[2].axvline(x=pv2_och_set, color = 'red', linestyle='--', linewidth = 4)
    ax[2].text(x = 171, y=86, s='Decada de\nlos Ochentas')
    ax[2].text(x = 166, y = -45,
      s = '   ©Mauricio Mani' + espacio*150 + 'Source: NFL: www.nfl.com/players   ',
            fontsize = 12, color = '#f0f0f0', backgroundcolor = 'grey')
    ax[2].set_ylabel('Cuenta')
    ax[1].hist(seten, bins = 9, alpha = 0.7, color = 'blue')
    ax[1].set_xlim([mins, maxs])
    ax[1].axvline(x = seten.mean(), color = 'red', linewidth = 4)
    ax[1].set_ylabel('Cuenta')
    ax[1].text(x = 171, y=71, s='Decada de\nlos Setentas')
    ax[0].hist(ses, bins = 9, alpha=0.7, color = 'blue')
    ax[0].set_xlim([mins, maxs])
    ax[0].axvline(x=ses.mean(), color = 'red', linewidth = 4) 
    ax[0].axvline(x=pv1_ses_set, color = 'red', linestyle='--', linewidth = 4)
    ax[0].axvline(x=pv2_ses_set, color = 'red', linestyle='--', linewidth = 4)
    ax[0].set_ylabel('Cuenta')
    ax[0].text(x = 171, y=87, s='Decada de\nlos Sesentas')
    ax[0].text(x = 168, y = 158, s = "Diseñando al runningback perfecto - proceso de aprendizaje",
               fontsize = 23, weight = 'bold', alpha = .75)
    ax[0].text(x = 168, y = 120, 
               s = 'Intervalos de confianza de la diferencia de medias en la estatura de los corredores de la NFL\nEn la decada de los sesentas, setentas y ochentas.',
              fontsize = 16, alpha = .85)
    plt.show()  

#Muestra si la altura o el peso influyen en las yardas para la temporada 2017.
def graficar_dispersion_2017(df_2017):
    espacio = ' ' 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x= df_2017['Altura'], y= df_2017['Peso'], s= df_2017['Yardas'], c = 'dodgerblue')
    plt.ylim(175, 260)
    plt.xlabel('Altura')
    plt.ylabel('Peso')
    ax.text(x = 165 , y = 164,
            s = '   ©Mauricio Mani' + espacio * 170 + 'Source: NFL: www.nfl.com/players   ',
    fontsize = 10, color = '#f0f0f0', backgroundcolor = 'grey')
    ax.text(x = 166.5, y = 269.5, 
            s = '¿Altos o no tanto? - ¿Pesados o rápidos y elusivos?',
            fontsize = 18, weight = 'bold', alpha = .75)
    ax.text(x = 166.5, y = 260.5, s = 'Gráfico de dispersión de la altura y peso de los corredores cada punto muestra las yardas\nParece no haber una clara relación entre yardas y altura o peso',
            fontsize = 16, alpha = 0.85)
    plt.show()

if __name__ =='__main__':
    df = pd.DataFrame(columns = ['Nombre', 'Año', 'Peso', 'Altura', 'Yardas_totales'])
    df_2017 = pd.DataFrame(columns = ['Nombre', 'Status', 'Peso', 'Altura', 'Yardas', 'Posicion'])
    for i in range(1, 56):
        df1 = links_tabla(i)
        df = df.append(df1)
        #df.to_csv('data/history_RB.csv')
        print(df)
    for i in range(1, 5):
        df2 = RB_2017(i)
        df_2017 = df_2017.append(df2)
        #df_2017.to_csv('data/2017_RB.csv')
    #Wrangling, cleaning
    df = df.reset_index(drop = True)
    df = df[['Año', 'Nombre', 'Altura', 'Peso', 'Yardas_totales']]
    df.dtypes
    df['Yardas_totales'] = df["Yardas_totales"].str.replace(",","")
    df['Yardas_totales'] = df["Yardas_totales"].str.replace(".","")
    df['Peso'] = pd.to_numeric(df.Peso, errors='coerce')
    df['Yardas_totales'] = df['Yardas_totales'].astype(int)
    #Revisar todos los valores con NaN
    df[df.isnull().any(axis=1)]
    #Elimina las filas que contienen NaN en altura o peso
    df = df.dropna(subset=['Altura', 'Peso'])    
    #2017
    df_2017 = df_2017[['Nombre', 'Altura', 'Peso', 'Yardas', 'Status', 'Posicion']]
    df_2017 = df_2017.reset_index(drop=True)
    df_2017['Yardas'] = df_2017["Yardas"].str.replace(",","")
    df_2017['Yardas'] = pd.to_numeric(df_2017.Yardas, errors='coerce')
    #Historia
    # Runningbacks historicos con mas de 6,000 yardas
    df.loc[df['Yardas_totales'] > 6000 ]
    print('Altura de Runningbacks con más de 6,000 yardas: ')
    print(df['Altura'].loc[df['Yardas_totales'] > 6000].mean())
    #Comparar la estatura de un fullback y un runningback
    print('Estatura media Fullback en la temporada 2017:')
    print(df_2017['Altura'].loc[df_2017['Posicion']=='FB'].mean())
    print('Estatura media Runningback en la temporada 2017:')
    print(df_2017['Altura'].loc[df_2017['Posicion']=='RB'].mean())
    print('Media total:')
    print(df_2017['Altura'].mean())
    print('Estatura media de los jugadores activos de la temporada 2017: ')
    print(df_2017['Altura'].loc[df_2017['Status']=='ACT'].mean())
    #Estatura media de los jugadores activos con mas de 1,000 yardas en la temporada 2017
    print('Estatura media de los jugadores activos de la temporada 2017 con mas de 1000 yardas: ')
    print(df_2017['Altura'].loc[(df_2017['Status']=='ACT') & (df_2017['Yardas'] > 1000)].mean())
    #Entender gráficas
    print(df_2017.loc[df_2017['Altura']==167.5])
    #Realizar funciones. 
    lista, lista1 = obtener_lista(df, df_2017)
    graficar_tiempo(lista, df)
    graficar_estatura(lista1)
    mejores_2017 = entender_2017(df_2017)
    prueba_hipotesis(lista1)
    graficar_dispersion_2017(df_2017)
#df = pd.read_csv('data/history_RB.csv', index_col=[0], encoding = "ISO-8859-1")
#df_2017 = pd.read_csv('data/2017_RB.csv')

