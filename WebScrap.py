import requests
from bs4 import BeautifulSoup
import pandas as pd

        # LECTURA DEL ARCHIVO EXCEL
        
excelFile = 'excelDocs/DatosRuc.xlsx'
excelDataFrame = pd.read_excel(excelFile, names=['indice','Ruc','Nombre_Empresa'])
excelDataFrame['Representante_Legal'] = None
excelRows = excelDataFrame.shape[0]    # SE ASIGNA LA CANTIDAD DE FILAS A LA VARIABLE excelRows
rowCounter = 0   # CONTADOR

        #VARIABLES QUE SE ENVIAN EN EL REQUEST
        
urlInicial = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
payload={}
headers = {
'Host': 'e-consultaruc.sunat.gob.pe',
'Origin': 'https://e-consultaruc.sunat.gob.pe',
'Referer': urlInicial,
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
'sec-ch-ua-mobile': '?0',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}


        # METODO PARA BUSCAR REPRESENTANTES LEGALES POR RUC Y NOMBRE

for rowCounter in range(excelRows):   

    stringDf = ""
    numeroRUC = excelDataFrame.Ruc[rowCounter]
    nombrEmpresa = excelDataFrame.Nombre_Empresa[rowCounter]
    
    
    url = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=getRepLeg&nroRuc=%s&contexto=ti-it&modo=1&desRuc=%s" % (numeroRUC, nombrEmpresa)       
    
    # VARIABLES PARA REINTENTAR EL REQUEST   
    max_retries = 100
    retries = 0
    
    # METODO QUE INTENTA EL REQUEST CON LA INFORMACION ENVIADA HASTA QUE REGRESE LA INFORMACION QUE SE PIDIO
    while retries < max_retries:
       
        sesion = requests.Session()
        response = sesion.request("POST", url, headers=headers, data=payload, verify=True)
        contenidoHTML = response.text   
        
        if "<head><title>Request Rejected</title></head>" not in contenidoHTML and (response.status_code == 200):
            
            try:
                soup = BeautifulSoup(contenidoHTML, 'html.parser')
                table = soup.find('table')
                data = []
                
                #METODO PARA ENCONTRAR LAS TABLAS
                for row in table.find_all('tr'):
                    cols = row.find_all(['th', 'td'])
                    cols = [col.text.strip() for col in cols]
                    data.append(cols)       
                
                
                #METODO PARA ELIMINAR COLUMNAS INNECESARIAS
                
                dataFrameWeb = pd.DataFrame(data[1:], columns=data[0])
                
                dataFrameWeb.drop(['Documento','Nro. Documento','Fecha Desde','Cargo'],
                  axis='columns', inplace=True)
                
                #METODO PARA CONCATENAR MULTIPLES NOMBRES PARA UNA SOLA CELDA 
                dataLength = dataFrameWeb.shape[0]
                for i in range(dataLength):
                    stringDf += str(dataFrameWeb.Nombre[i]) + ', '
                    i = i+1
                    
                    
                #INGRESO DE DATOS AL DATAFRAME 
                excelDataFrame.loc[rowCounter, 'Representante_Legal'] = stringDf
                
                print( "***************" ,rowCounter,"***************" )    
                
            except AttributeError as e:
                print(f"An AttributeError occurred for row {rowCounter}")
                print(excelDataFrame.Ruc[rowCounter])
                
            break
        
        else:
            print("Request Rejecter. Retrying....")
            retries += 1
            
    else:
        print(f"failed to retrieve data :(")
        
    rowCounter = rowCounter + 1


excelDataFrame.to_excel('excelDocs/DatosRepLeg.xlsx', index=False)




