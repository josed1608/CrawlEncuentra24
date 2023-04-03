# Guía de troubleshooting

En esta guía se registrarán problemas encontrados y sus soluciones para futuros arreglos que sean necesarios. Recuerde que la salida del scrapper se encuentra en el archivo de logs `CrawlEncuentra24/scarpy_output.txt`, donde se pueden revisar los errores que reportó la aplicación al correr.

## Timeouts al iniciar a correr el scrapper
El error que se encuentra en el `scrapy_output.txt` se ve de la siguiente forma:
```
twisted.internet.error.TimeoutError: User timeout caused connection failure: Getting http://0.0.0.0:8050/execute took longer than 180.0 seconds..
```
Esto ocurre debido a que la instancia de Dockr que corre Splash dejó de responder. Probablemente el script para correr el scrapper tuvo problemas deteniendo la instancia cuando se terminó la última corrida, por lo que se dejó la instancia corriendo por mucho tiempo y quedó en un estado de freeze. Para solucionarlo simplemente se debe detener la instancia y correr y nueva. Si se presentan problemas de permisos al detener la instacia, se debe revisar si `app-armor` no está interfieriendo con el servicio de Docker (consultar con el procurador de IT en este caso), en cuyo caso se debe deshabilitar esta protección.

## El scrapper corre y hace requests pero no recolecta todos o algunos datos
La forma en que se presenta esta error puede variar de muchas formas. Pueden o no encontrarse errores en el archivo de logs. Sin embargo, la razón será siempre el cambio en estilos o forma de la página Encuetra24.

Para solucionarlo, se deben utilizar herramientas como la consola de desarrollador del navegador o esta [extensión de Google Chorme](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb?hl=en-US) que permité encontrar identificadores para elementos que se seleccionen de la página. Una vez encontrado el nuevo identificador, se debe reemplazar en el código.