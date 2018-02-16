Estadística divertida y running backs de la NFL
--------------------------------------------------

#Traducciones:
* [Español](README.md)
* [English](README-en.md)

## La idea y el artículo.
Para la temporada 2013 solo 2 jugadores de los mejores 10 medían mas de 6 pies: Adrian Peterson y Arian Foster. 
La NFL se caracteriza por tener a los jugadores mas grandes pero no necesariamente para la posición de corredor. 
Primero: No queremos a un jugador demasiado alto ya que le podrán ver muy fácil por atras de la línea. Los corredores mas 
pequeños se pueden esconder atras de los jugadores grandes, "la línea". 
Segundo: Queremos que tengan un centro de gravedad bajo.

¿Ha cambiado en algo la NFL desde que empezó? Sí y mucho. Pero, ¿cómo se han generado estos cambios? Aprendiendo del pasado.
La idea de analizar la base de datos de todos los corredores proviene de un artículo escritó por `bleacherreport.com`.
¿Acaso la NFL ha aprendido del pasado? ¿Tenemos a los mejores corredores posibles? BJKissel hace un intento en diseñar al mejor 
corredor posible, basandose en la altura, el peso y la velocidad. Toma como referencia a los corredores de la temporada 2013.
Pero, ¿Qué nos dice la historia?

<br/>
<p align="center">
<img src="Images/corredores_tiempo.gif" alt="gif">
</p><br/>

## Altura promedio por decadas.
* 1920 - 1930 es: `178.25`
* 1930 - 1940 es: `181.25`
* 1940 - 1950 es: `181.39`
* 1950 - 1960 es: `182.5`
* 1960 - 1970 es: `184.54` 

Gale Sayers (183cm). John David Crow, Paul Hornung (188cm)

* 1970 - 1980 es: `183.92` 

O. J. Simpson (185cm)

* 1980 - 1990 es: `181.48` 

Earl Campbell, Tony Dorsett (180cm)

* 1990 - 2000 es: `181.46` 

Emmitt Smith (175cm). Marshall Faulk, Thurman Thomas (178cm). Terrell Davis, Jerome Bettis (180cm). 

* 2000 - 2010 es: `181.73` 

Warrick Dunn (175cm). Thomas Jones, Ricky Williams, Bryan Westbrook, LaDainian Tomlinson (178cm). Clinton Portis (180cm).

* 2010 - 2016 es: `180.92`
* 2017 es: `180.16`

Esta imagen muestra como ha cambiado la altura y el peso a través de las decadas desde 1920 hasta la temporada del 2017. 
Durante los cincuentas y hasta finales de los setentas la distribución de la altura se encontrará a la derecha y en las decadas 
posteriores retrocederá a una media de 181cm. 
En el eje horizontal o de las abscisas se muestra el peso y el eje vertical o real muestra la altura. Por lo que un aumento
en la altura desplazaría las observaciones hacia arriba y un aumento en el peso hacia la derecha. Parece que los corredores son mas 
fuertes hoy en día y menos altos que en décadas anteriores a los ochentas.
Para entender mejor el aprendizaje sobre los corredores graficaremos boxplots (diagrama de caja y bigotes) que son difíciles de entender
por lo que explicaré un boxplot con un ejemplo: "la temporada 2017".

## Entendiendo estadísticas con la información de la temporada 2017. 
El boxplot es de las herramientas mas completas para hacer un análisis preliminar sde los datos obtenidos. Ya que a diferencia del 
histograma permite de forma más sencilla comparar dos distribuciones. Comunmente queremos saber que tan normal son los datos, 
¡usa un boxplot!
La normalidad es más fácil de ver graficamente con un histograma (pero no te preocupes, también con un boxplot). 
Primero graficaremos la estatura de los corredores activos de  la temporada 2017 y la compararemos con una distribución normal.  

<br/>
<p align="center">
<img src="Images/histograma_normal.png" alt="histograma">
</p><br/>

La altura mínima es 167.5cm. Son dos jugadores con esa altura:
* `Tarik Cohen`: 377 yardas
* `Jacquizz Rodgers`: 244 yardas

La altura máxima es de 192cm. Son tres jugadores con esa estatura:

* `Derrick Henry`: 744 yardas
* `Latavius Murray`: 842 yardas
* `Rod Smith`: 232 yardas
La media es de 180.16cm, pero en el histograma claramente podemos ver que la moda se encuentra en otro intervalo.
Por lo que es más común ver corredores más pequeños que la media. 
Sin embrago, ¿parece normal, cierto? Bueno, no los podemos afirmar a simple vista. Podemos usar un Q-Q plot. Que compara los valores 
vistos con valores de probabilidad hipotéticos normales, una distribución normal será una línea de 45 grados. En este caso no parece normal.

<br/>
<p align="center">
<img src="Images/Q-Q_plot.png" alt="Q-Q plot">
</p><br/>

Como podemos ver los puntos parecen encontrarse en ciertas regiones, esto se debe a que no hay continuidad en la altura.
Por lo que el Q-Q plot no es un buen indicador. 
Una de las suposiciones de normalidad es una media igual, una mediana igual y una moda igual. La media es ´180.21´
La mediana es ´180.16´ y no hay moda (o todos los valores son la moda). 
¡Hagamos estadísticas mas avanzadas!
Para probar la normalidad de una distribución podemos usar la prueba X^2 de normalidad, la prueba Kolmogorov-Smirnov, 
la prueba Shapiro-Wilk y la prueba Lilliefors estas últimas son la más famosas para comprobar normalidad. Todas son derivaciones de 
pruebas de hipótesis, donde tenemos una hipótesis nula y una alternativa. 

* El valor de la prueba Kolmogorov-Smirnov es: `0.123436625014`
* El valor p de la prueba es: `5.73947997152e-10`
* El valor de la prueba Shapiro-Wilk es: `0.9677223563194275`
* El valor p de la prueba es: `1.819115823309403e-05`

La prueba Shapiro Wilk plantea la hipótesis nula donde las observaciones provienen de una distribución normal.
Ahora veamos una distribución acumulada de la estatura de los corredores y su normal:

<br/>
<p align="center">
<img src="Images/Histograma_acumulado.png" alt="Kolmogorov">
</p><br/>

Los datos y la imagen niegan la normalidad de nuestra distribución. Tanto la prueba Lilliefors como la prueba Kolmogorov-Smirnov
se basan en la distancia más extrema de la distribución acumulada vista y la distribucion acumulada hipotética normal.
Además las 2 pruebas que realizamos tienen valores p extremadamente pequeños. 
Y se puede ver muy "claro" en el boxplot (la normalidad) gracias a la dispersión de las cajas. Nos muestra valores extremos tambien.
Para este caso son los jugadores con más de 800 yardas en la temporada 2017.

<br/>
<p align="center">
<img src="Images/entender_boxplot.png" alt="boxplot">
</p><br/>

```
| Nombre               | Altura  | Peso | Yardas | 
|----------------------|---------|------|--------| 
| "Anderson, C.J."     | 172.5   | 224  | 1007.0 | 
| "Lewis, Dion"        | 172.5   | 195  | 896.0  | 
| "Freeman, Devonta"   | 172.5   | 206  | 865.0  | 
| "Ingram, Mark"       | 175.0   | 215  | 1124.0 | 
| "Gore, Frank"        | 175.0   | 212  | 961.0  | 
| "Hunt, Kareem"       | 177.5   | 216  | 1327.0 | 
| "Collins, Alex"      | 177.5   | 210  | 973.0  | 
| "Miller, Lamar"      | 177.5   | 225  | 888.0  | 
| "McCoy, LeSean"      | 180.0   | 210  | 1138.0 | 
| "Lynch, Marshawn"    | 180.0   | 215  | 891.0  | 
| "Crowell, Isaiah"    | 180.0   | 225  | 853.0  | 
| "Howard, Jordan"     | 182.88  | 224  | 1122.0 | 
| "Fournette, Leonard" | 182.88  | 228  | 1040.0 | 
| "Elliott, Ezekiel"   | 182.88  | 228  | 983.0  | 
| "Hyde, Carlos"       | 182.88  | 235  | 938.0  | 
| "Ajayi, Jay"         | 182.88  | 223  | 873.0  | 
| "Gurley, Todd"       | 185.928 | 227  | 1305.0 | 
| "Bell, Le'Veon"      | 185.928 | 225  | 1291.0 | 
| "Gordon, Melvin"     | 185.928 | 215  | 1105.0 | 
| "Murray, Latavius"   | 192.024 | 230  | 842.0  | 
```

## Aprendizaje.
>El aprendizaje es una propiedad de la actividad mental que produce en el organismo el resultado de cambiar o modificar 
>su sistema  cognitivo y su comportamiento observable. Son cambios relativamente permanentes que ocurren por condiciones de prática.

¡Listo! Ahora si podemos entender como ha cambiado la estatura de los corredores a traves de las décadas y sobre todo el 
aprendizaje (prueba y error) para diseñar al mejor running back de la NFL. 

<br/>
<p align="center">
<img src="Images/boxplot_historico.png" alt="historico">
</p><br/>

¿Qué vemos?
En los años veinte la mediana es muy baja pero hay muchos outliers (idea de corredores altos) y la medida de tendencia central debe ser 
tan baja por la estatura media de los americanos. 
De los años treintas a los años setentas la mediana de la estatura claramente se eleva. Estos años sirven de aprendizaje.
A partir de la década de los ochentas vemos que la mediana se ha reducido y se ha establecido hasta la temporada 2017.
La distribución de los datos parece estar sesagada positivamente por lo que se concentran más jugadores pequeños. 
Además las distribuciones se han encogido, lo que nos muestra que la NFL ahora sabe lo que quiere.
Esta es información poblacional, por ende, sea lo que sea que veamos en este grafico es la realidad (a diferencia de 
usar una muestra). Sin embargo, realizaremos una prueba de hipótesis de la diferencia de dos muestras independientes.
(Para mayor información correr el código).

<br/>
<p align="center">
<img src="Images/prueba_hipotesis.png" alt="hipotesis">
</p><br/>

Podemos ver claramente que es improbable que se haya dado por aleatoriedad la altura de los corredores. 
Pero, ¿Qué no son mejores los jugadores altos, ¿qué no los mas altos tienen más yardas? Veamos que pasa en la temporada 2017.
Al igual que al principio usaremos un gráfico de dispersión pero en este caso las observaciones estarán en 
función de las yardas por temporada. Claramente se ve que no hay una relacion entre las yardas por temporada y la altura o inclusive el peso. 

<br/>
<p align="center">
<img src="Images/dispersion.png" alt="dispersion">
</p><br/>

## Conclusión.
La imagen anterior nos muestra que el hecho de ser mas alto o mas pesados no significa que corras más yardas. 
Tanto la media como la mediana son medidas de tendencia central y debemos de buscar la que mejor represente los datos. 
La media en este caso puede no ser el mejor parámetro y hay que recordar que el hecho de tener cierta media, no excluye que podamos
encontrar valores extremos (mientras se compensen). 
Efectivamente, nos podemos dar cuenta que la NFL ha aprendido a través de los años. Y esto se demuestra con el desplazamiento
de la distribución a través de las décadas (y por ende un movimiento en la media). 
Como comentan en el artículo, la NFL considera que tener jugadores que oscilen entre 178 y 182 centímetros son más reclutados.
Esto no quiere decir que si eres alto, seas un mal corredor. Tal vez al contrario, si eres alto eres mejor (ya que la NFL ha optado por jugadores mas pequeños). 

## ¿Qué hace el código?
Primero, el codigo extrae (scrape) toda la información de los corredores históricos y del 2017 de la página oficial de la NFL. 
Transforma los pies en centímetros.
Gráfica y realiza todas las pruebas estadísticas que has visto aquí.
Además de información adicional sobre la estatura de los corredores y los full backs.

## Referencias.
* http://bleacherreport.com/articles/1669734-height-weight-and-speed-designing-the-perfect-nfl-running-back
* Romero Medina A. (2017). "Concepto de Apredizaje". Universidad de Murcia.