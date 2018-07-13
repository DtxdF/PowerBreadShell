# PowerBreadShell
Un generador de puertas traseras con escalacion de privilegios para comprometer una maquina-objetivo (Windows)

# En que consiste?
Como la descripcion lo dice es un generador de puertas traseras utilizando varias tecnicas y herramientas para la escalacion de privilegios e infeccion, La escalacion de privilegios es hacia el servidor local con un sistema operativo "Windows" y este es comprometido por un documento php, cuando se sube a un servidor y este se ejecuta se recibira la terminal de windows

# Post explotacion:
- Al tener ya comprometida la maquina-objetivo usando el archivo php conseguiras privilegios del usuario :: NT AUTHORITY\SYSTEM, Probado en (winxp, win7 - con powershell instalado)
- Ejecutar comandos del sistema
- Creatividad por parte del atacante

# Dependencias
- Maquina-objetivo (Windows)
    Tener un sistema operativo windows instalado, con powershell
- Maquina-atacante (Windows - Si se usa una distribucion de linux, es recomendable usar wine con python (2.7 - recomendable) instalado)
    Tener un servidor apache con php incluido (Recomendable WampServer)
    
# Capturas de pantallas

![](https://i.imgur.com/qnL4ifU.png)

![](https://i.imgur.com/exRa3zH.png)
