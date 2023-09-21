# Web-Scraping-Sunat
# Este Web Scraper se crea con la necesidad de automatizar un proceso manual. 
# En promedio una persona podria hacer la consulta de 40 RUCs en 1 hora y escribirlos en un excel, para nuestro ejemplo se usaron 2500 RUCs, y como tiempo medio de la consulta de todos ellos de unos 5 minutos
# Este script leera un archivo de tipo EXCEL el cual debe tener las columnas INDICE - RUC - NOMBRE DE LA EMPRESA, no necesariamente escritos explicitamente en el excel
# Es posible solo tener 2 columnas, para eso revisar el script y eliminar el campo indice Ln8 excelDataFrame = pd.read_excel(excelFile, names=['indice','Ruc','Nombre_Empresa'])
# Posterior a la lectura del archivo lo que hara es empezar a hacer solicitudes al sitio web SUNAT consultando por los datos del RUC y nombre de nuestro archivo excel, y nos entregara como respuesta los representantes legales de cada uno de los RUCs, y los convertira en un archivo excel llamado DatosRepLeg.xlsx
# Revisar por los archivos excel en la carpeta excelDocs
# 
