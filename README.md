# Proyecto_Login
Aplicacion basada en el paquete de streamlit para visualizacion y analisis de distribucion de horas cumplidas por ejecutivos durante el día, ademas de validar el requerimiento del cliente comparando las horas completadas por parte de la plataforma.

* Se limpian el archivo de las horas Login - Logout de cada ejecutivo.
* Se filtra la informacion en base a nuestra base de ejecutivos activos en plataforma, validando que este se encuentre laborando antes de la fecha de evaluacion y en caso de ser baja esta fecha debe ser posterior a la fecha a evaluar.
* En caso de querer evaluar las horas cumplidas en plataforma vs las propuestas por el cliente se debe cargar posterior a estos dos archivos anteriores.


Modo de uso:
1. En el sidebar se encuentran las opciones a configurar para comenzar el despliegue de la informacion.
2. Se registra la fecha a la cual se desea evaluar. En este caso procederemos a evaluar el 11-05-2021, ya que es los reportes que dejo como muestras en la seccion Document Input
3. En la seccion Reporte día, colocaremos el archivo .csv denominado "Agent_Login-Logout_Details_Report_11-Enero" que representa el reporte diario. Validar el tipo de Delimitador utilizado dentro del .csv, por default se utilizar ','.

Este nos mostrara su contenido en la seccion principal de la pagina. Pero esta informacion se encuentra poblada por usuarios que no son necesariamente de nuestra importancia, por lo cual debemos importar nuestra base, con el objetivo de filtrar la informacion de acuerdo a nuestra informacion actualizada.

4.En la seccion reporte día, "Base de datos de referencia" procederemos a importar los datos de los usuarios a ser considerados para el analisis, esta base esta dispuesta en la seccion Document Input como "BDD_HOLDTECH_26022021".

Ahora tenemos el mismo formato anterior, pero esta vez filtrada por los datos que nos interesa.

Aqui dispondremos de un desglose de cantidad de horas cumplidas por cada usuario señalados segun su jornada laboral.

5. En caso de querer corroborar la cantidad de horas efectivas cumplidas VS la informacion requerida por el cliente debemos suministrar el archivo en la seccion "Ingresar Requerido", este archivo se encuentra en la seccion Document Input como "Requerido call Holdtech Enero 2021 v1".

Aqui tendremos el Requerido suministrado por el cliente, las Horas de log efectivas, y el Cumplimiento de este requerido en porcentaje% ademas de la visualizacion de la distribucion de las horas Cumplidas VS Requeridas.

Este proceso puede ser evaluado por "Cargos" o "Servicio", que estan dispuestos en el sidebar de la pagina.
