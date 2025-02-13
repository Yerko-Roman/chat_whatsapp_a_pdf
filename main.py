import zipfile
import os 
from fpdf import FPDF
from cleantext import clean

#Nombre archivo zip.

nombre_zip = ''

#Limpiar el nombre del archivo zip de los emoji.

nombre_zip_sin_emoji = clean(nombre_zip, no_emoji=True)

#Variables.

ruta_zip = './zip/' + nombre_zip
nombre_proyecto = nombre_zip_sin_emoji.replace('.zip', '')
cont_img = 0
cont_vid = 0
cont_audio = 0
cont_stiker = 0
cont_documento = 0


#Creacion de carpetas.

carpeta_descomprimido = './zip_descomprimido/' + nombre_proyecto + 'zip'
carpeta_pdf = './pdf/' + nombre_proyecto + 'pdf'

if not os.path.exists(carpeta_descomprimido):
    os.mkdir(carpeta_descomprimido)

if not os.path.exists(carpeta_pdf):
    os.mkdir(carpeta_pdf)
    os.mkdir((carpeta_pdf + '/audio'))
    os.mkdir((carpeta_pdf + '/img'))
    os.mkdir((carpeta_pdf + '/video'))
    os.mkdir((carpeta_pdf + '/contacto'))
    os.mkdir((carpeta_pdf + '/documento'))
    os.mkdir((carpeta_pdf + '/stiker'))


#Descomprimir el archivo zip.

descomprimido = zipfile.ZipFile(ruta_zip,"r")
descomprimido = descomprimido.extractall(path=carpeta_descomprimido)

#Recorrer los archivos hasta encontrar el archivo txt.

lista_archivos = os.listdir(carpeta_descomprimido)

for archivo in lista_archivos:
    if '.txt' in archivo:
        nombre_txt = archivo
        pass

#Ruta donde se encuentra el archivo txt.

ruta_conversacion = carpeta_descomprimido + '/' + nombre_txt

#Abrir el archivo txt que contiene la conversacion.

conversacion = open(ruta_conversacion)

#Crear el archivo pdf.

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_font('Arial', '', 18)

#Leer el txt linea a linea.

for mensaje in conversacion:

    #Limpiar el mensaje del caracter LRM y los emoji.

    mensaje_limpio = mensaje.replace('‎', '')
    mensaje_limpio = clean(mensaje_limpio, no_emoji=True)

    #Comprobar si es mensaje o archivo.

    if '(archivo adjunto)' in mensaje:

        #Separa el mensaje por los espacios en blanco.

        mensaje_segmentado = mensaje_limpio.split()

        #Detectar el tipo de archivo que es.

        if '.jpg' in mensaje:

            try:
                
                #Mover la imagen de carpeta.

                os.replace((carpeta_descomprimido + '/' + mensaje_segmentado[-3]), (carpeta_pdf + '/img/' + mensaje_segmentado[-3]))

                #Nuevo nombre de la imagen.

                nombre_img = ('img' + str(cont_img) + '.jpg')
                cont_img += 1

                #Cambiar el nombre de la imagen.

                os.replace((carpeta_pdf + '/img/' + mensaje_segmentado[-3]), ((carpeta_pdf + '/img/' + nombre_img)))

                #Formatear el mensaje con el nuevo nombre de la imagen.

                mensaje_fromateado = ' '.join(mensaje_segmentado[:-3])
                mensaje_fromateado = mensaje_fromateado + ' ' + nombre_img

                #Agregar mensaje formateado al pdf.

                pdf.multi_cell(190, 10,  txt=mensaje_fromateado)
                pdf.multi_cell(190, 10,  txt='\n')

                #Agregar la imagen al pdf.

                pdf.image((carpeta_pdf + '/img/' + nombre_img), w = 150, h= 150)

            except FileNotFoundError:

                #En caso de no encontrar la imagen se guarda el mensaje y se indica que el archivo no existe.

                pdf.multi_cell(190, 10,  txt= (mensaje_limpio + '(imagen no encontrada)'))
                pdf.multi_cell(190, 10,  txt='\n') 

        elif '.mp4' in mensaje:

            try:
                
                #Mover el video de carpeta.

                os.replace((carpeta_descomprimido + '/' + mensaje_segmentado[-3]), (carpeta_pdf + '/video/' + mensaje_segmentado[-3]))

                #Nuevo nombre del video.

                nombre_vid = ('video' + str(cont_vid) + '.mp4')
                cont_vid += 1

                #Cambiar el nombre del video.

                os.replace((carpeta_pdf + '/video/' + mensaje_segmentado[-3]), ((carpeta_pdf + '/video/' + nombre_vid)))

                #Formatear el mensaje con el nuevo nombre del video.

                mensaje_fromateado = ' '.join(mensaje_segmentado[:-3])
                mensaje_fromateado = mensaje_fromateado + ' ' + nombre_vid + ' (Video)'

                #Agregar mensaje formateado al pdf.

                pdf.multi_cell(190, 10,  txt=mensaje_fromateado)
                pdf.multi_cell(190, 10,  txt='\n') 

            except FileNotFoundError:

                #En caso de no encontrar el video se guarda el mensaje y se indica que el archivo no existe.

                pdf.multi_cell(190, 10,  txt= (mensaje_limpio + '(video no encontrada)'))
                pdf.multi_cell(190, 10,  txt='\n') 

        elif '.opus' in mensaje:

            try:

                #Mover el audio de carpeta.

                os.replace((carpeta_descomprimido + '/' + mensaje_segmentado[-3]), (carpeta_pdf + '/audio/' + mensaje_segmentado[-3]))

                #Nuevo nombre del audio.

                nombre_audio = ('audio' + str(cont_audio) + '.opus')
                cont_audio += 1

                #Cambiar el nombre del audio.

                os.replace((carpeta_pdf + '/audio/' + mensaje_segmentado[-3]), ((carpeta_pdf + '/audio/' + nombre_audio)))

                #Formatear el mensaje con el nuevo nombre del audio.

                mensaje_fromateado = ' '.join(mensaje_segmentado[:-3])
                mensaje_fromateado = mensaje_fromateado + ' ' + nombre_audio + ' (Audio)'

                #Agregar mensaje formateado al pdf.

                pdf.multi_cell(190, 10,  txt=mensaje_fromateado)
                pdf.multi_cell(190, 10,  txt='\n') 

            except FileNotFoundError:

                #En caso de no encontrar el audio se guarda el mensaje y se indica que el archivo no existe.

                pdf.multi_cell(190, 10,  txt= (mensaje_limpio + '(audio no encontrada)'))
                pdf.multi_cell(190, 10,  txt='\n')

        elif '.vcf' in mensaje:

            try:

                #Extraer el nombre del contacto, del mensaje.

                nombre_contacto = mensaje.split(':')
                nombre_contacto = nombre_contacto[2]
                nombre_contacto = nombre_contacto.replace('(archivo adjunto)', '')
                nombre_contacto = nombre_contacto.replace('‎', '')
                nombre_contacto = nombre_contacto.replace('\n' , '')
                nombre_contacto = nombre_contacto.replace(' ' , '', 1)
                nombre_contacto = nombre_contacto[:-1]

                #Mover el contacto de carpeta.

                os.replace((carpeta_descomprimido + '/' + nombre_contacto), (carpeta_pdf + '/contacto/' + nombre_contacto))

                #Eliminar emojis del nombre.

                nombre_contacto_sin_emoji = clean(nombre_contacto, no_emoji=True)

                #Cambiar nombre del contacto.

                os.replace((carpeta_pdf + '/contacto/' + nombre_contacto),(carpeta_pdf + '/contacto/' + nombre_contacto_sin_emoji))

                #Formatear el mensaje.

                mensaje_fromateado = mensaje_limpio.replace('(archivo adjunto)', '(Contacto)')

                #Agregar mensaje formateado al pdf.

                pdf.multi_cell(190, 10,  txt= mensaje_fromateado)
                pdf.multi_cell(190, 10,  txt='\n') 

            except FileNotFoundError:

                #En caso de no encontrar el contacto se guarda el mensaje y se indica que el archivo no existe.

                pdf.multi_cell(190, 10,  txt= (mensaje_limpio + '(contacto no encontrada)'))
                pdf.multi_cell(190, 10,  txt='\n')

        elif '.webp' in mensaje:

            try:

                #Mover el stiker de carpeta.

                os.replace((carpeta_descomprimido + '/' + mensaje_segmentado[-3]), (carpeta_pdf + '/stiker/' + mensaje_segmentado[-3]))

                #Nuevo nombre del stiker.

                nombre_stiker = ('stiker' + str(cont_stiker) + '.webp')
                cont_stiker += 1

                #Cambiar el nombre del stiker.

                os.replace((carpeta_pdf + '/stiker/' + mensaje_segmentado[-3]), ((carpeta_pdf + '/stiker/' + nombre_stiker)))

                #Formatear el mensaje con el nuevo nombre del stiker.

                mensaje_fromateado = ' '.join(mensaje_segmentado[:-3])
                mensaje_fromateado = mensaje_fromateado + ' ' + nombre_stiker + ' (Stiker)'

                #Agregar mensaje formateado al pdf.

                pdf.multi_cell(190, 10,  txt=mensaje_fromateado)
                pdf.multi_cell(190, 10,  txt='\n') 

            except FileNotFoundError:

                #En caso de no encontrar el stiker se guarda el mensaje y se indica que el archivo no existe.

                pdf.multi_cell(190, 10,  txt= (mensaje_limpio + '(stiker no encontrada)'))
                pdf.multi_cell(190, 10,  txt='\n')

        else:

            try:

                #Extraer el nombre del docuemnto del mensaje.

                nombre_documento = mensaje.split(':')
                nombre_documento = nombre_documento[2]
                nombre_documento = nombre_documento.replace('(archivo adjunto)', '')
                nombre_documento = nombre_documento.replace('‎', '')
                nombre_documento = nombre_documento.replace('\n' , '')
                nombre_documento = nombre_documento.replace(' ' , '', 1)
                nombre_documento = nombre_documento[:-1]

                #Mover el documento de carpeta.

                os.replace((carpeta_descomprimido + '/' + nombre_documento), (carpeta_pdf + '/documento/' + nombre_documento))

                #Formatear el mensaje.

                mensaje_formateado = mensaje_limpio.replace('adjunto', '')

                #Agregar mensaje formateado al pdf.

                pdf.multi_cell(190, 10,  txt=mensaje_formateado)
                pdf.multi_cell(190, 10,  txt='\n') 

            except FileNotFoundError:

                #En caso de no encontrar el documento se guarda el mensaje y se indica que el archivo no existe.

                pdf.multi_cell(190, 10,  txt= (mensaje_limpio + '(documento no encontrada)'))
                pdf.multi_cell(190, 10,  txt='\n')

    else:

        #Agregar el mensaje al pdf.

        pdf.multi_cell(190, 10,  txt=mensaje_limpio)
        pdf.multi_cell(190, 10,  txt='\n')

#Cerrar el pdf y guardarlo. 
    
pdf.output((carpeta_pdf + '/Conversacion.pdf'))