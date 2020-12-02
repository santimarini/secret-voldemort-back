# secret-voldemort-back

### Comenzando

En el entorno de la materia Ingenieria del Software se desarrolló Secret Voldemort
un juego multiplayer de 5 a 10 jugadores con roles secretos. Existen 2 equipos, el equipo de la Orden del
Fenix y el equipo de los Mortifagos, el objetivo de la Orden del Fenix es descubrir
quien es Voldemort mientras que el objetivo de los Mortifagos es hacerse con el poder.
Para descargar los archivos clone el repositorio con el siguiente comando y tendra una copia
de la ultima version del juego:

    git clone https://github.com/santimarini/secret-voldemort-back.git
    
Si desea ejecutar el servidor backend junto con alguna interfaz le recomendamos visitar:

[secret-voldemort-front](https://github.com/santimarini/secret-voldemort-front)

### Instalacion

Antes de comenzar asegurese de tener python o python3 instalado:

    sudo apt install python-pip
    sudo apt install python3-pip
    
Si eligio instalar python3 el proceso de instalacion será similar, lo unico que debe cambiar en los
pasos es el comando **pip** por **pip3**

Este repositorio incluye paquetes instalables para su funcionamiento.
Al final de este informe encontrará la documentacion apropiada para cada tecnología utilizada.

    pip install fastapi

Tambien para poner en ejecucion el servidor necesitaras uvicorn

    pip install uvicorn

Para no tener problemas al ejecutar el servidor deberás tener las dependencias que 
en el archivo requirements.txt. Ejecutamos el siguiente comando:

    pip install -r requirements.txt
   
Una vez hecho estos pasos puede poner en funcionamiento el servidor en su ordenador ejecute lo siguiente:

    uvicorn app:app --reload --host 0.0.0.0
    
### Partes de este repositorio

Con el repositorio ya clonado usted tendrá en su directorio varios archivos y directorios:

#### app.py

Este archivo contiene la definicion del servidor y la API REST para recibir
peticiones. 

#### login_functions.py

Las funcionalidades de autenticacion, envio de email de verificacion y el checkeo
de la verificacion de usuario se encuentran acá.

#### pydantic_models.py

Las definiciones de algunas clases para poder recibir datos o enviar desde el sevidor
estan diseñadas a traves de la clase Models que nos proporciona el modulo pydantic.

#### database/

En este directorio encontrará el archivo database.py que contiene la definicion de la base de 
datos, su estructura y las funciones para manejar la logica del juego.

#### Test/

Este directorio contiene los tests automatizados para las pruebas de funcionalidad del servidor
Cabe destacar que son test no unitarios y solo prueban la funcionalidad a nivel endpoint.

#### requirements.txt

En este archivo estan todas las dependencias y paquetes para instalar y que funcione
el servidor correctamente

### Ejecutando las pruebas

Si eres un desarrollador tal vez te interese consultar la base de datos 
donde guardamos los objetos. Para ello necesitas instalar sqlite, que es el motor
que utilizamos para guardar la informacion. Corremos el comando:

    sudo apt install sqlite3

Una vez hecho esto nos dirigimos al directorio database y ejecutamos sqlite con:

    sqlite3

Con esto podemos realizar todas las consultas que queramos.

Por ultimo si quiere poner a prueba la robustez del servidor podemos ejecutar los
tests hechos en el directorio Test. Necesitarás tener los siquientes paquetes instalados:

    pip install os-sys
    pip install requests

Luego ejecutamos, estando en el directorio Test:

    python3 run.py
    
### Construido con

- [FastApi](https://fastapi.tiangolo.com/) (framework web utilizado)
- [PonyORM](https://ponyorm.org/) (manejador de base de datos)
- [JWT](https://jwt.io/) (implementacion de tokens para la autenticacion)

### Autores

Este repositorio se desarrolló a través de metodologia agil iterativa SCRUM.
Cada dia (lunes a viernes) usualmente 23:00hs el equipo se reune para charlar los avances de cada uno,
complicaciones y riesgos. En contexto de pandemia las reuniones se tomaban via virtual.

- [Centini Joaquin](https://github.com/JoaquinCentini)
- [Molina Agustin](https://github.com/agumolina)
- [Vilar Davila Valentin](https://github.com/ValenVilarDav)

### Contribuyentes

- [Marini Santiago](https://github.com/santimarini)
- [Frachia Joaquin](https://github.com/joacof98)