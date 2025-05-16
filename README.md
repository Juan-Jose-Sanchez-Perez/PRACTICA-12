paso 1.- Debemos realizar nuestra base de datos

paso 2.- Debemos crear nuestra base de datos en nuestro equipo
    mysql> SOURCE C:/ruta/a/tu/base.sql;
    USE name_db;
    mysql> SOURCE C:/ruta/a/tu/datos.sql;

paso 3.- Debemos crear un entorno virtual dentro de la carpeta de trabajo que almacena nuestros CRUD'S
        Python -m venv env23270628

paso 4.- Activamos nuestro entorno virtual
        env23270628\Scripts\activate

paso 5.- Instalamos todas las liberias necesarias para nuestro proyecto
        pip install flet
        pip install mysql_connector

paso 6.- Ejecutar el menu principal que almaneca todos los CRUD'S y su funcionamiento
        main_menu.py