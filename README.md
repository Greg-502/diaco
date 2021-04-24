## Instalaciones

1. Descargar e instalar [Brew](https://brew.sh/index_es) desde la terminal
2. Instalar con Brew MySQL desde la terminal `brew install mysql`
3. Descargar e instalar [Python](https://www.python.org)
4. Pip se instalará con Python
5. Instalar con pip(3) Virtualenv desde la terminal `pip3 install virtualenv`

## Creación de entorno virtual
6. Crear una carpeta en cualquier ubicación
7. Desde la carpeta abrir una terminal y escribir: `virtualenv env`
8. Activar entorno virtual `source env/bin/activate`
9. Se antepodrá (env) en las líneas de la terminal

## Descargar Django e iniciar proyecto y aplicación 
10. `pip3 install django`
11. `django-admin startproject nombre_proyecto`
12. `cd nombre_proyecto`
13. `python3 manage.py startapp nombre_app`

## Base de batos/migraciones
14. Crear base de datos sino fuera SQLite
15. En settings.py agregar las credenciales
16. Correr migraciones
```
python3 manage.py makemigrations
python3 manage.py migrate
```
17. Llenar tablas y correr procedimientos almacenados.

## Correr
18. `python3 manage.py runserver`
19. Detener con `ctrl` + `c`

## Desactivar entorno
20. `deactivate`

## Agregar dependecias a fichero.txt
21. Desde la ubicación de la(s) aplicacion(es), crear requirements.txt y agregar, ademas de django las futuras dependencias con sus versiones ej.: 
- Django == 3.1.7
- mysqlclient == 2.0.3
- gunicorn == 20.1.0
- ...

## Instalar requirements desde fichero
22. Con el entorno virtual activado `pip3 install -r requirements.txt`

## Capturas
### Formulario principal
![Principal](https://mega.nz/file/2EM2mTyY#64V9n2sVp1we35k8ZtS7Vm8HzgqlCc_RXrfs-lAMSu0)