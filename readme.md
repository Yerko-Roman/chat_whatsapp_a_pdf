# Objetivo

LLevar una conversacion de whatsapp a un documento pdf.

# Uso

1. Exportar tu historial de chat. (https://faq.whatsapp.com/1180414079177245/?locale=es_LA&cms_platform=android)

2. El archivo zip que se genere es que alojarlo en la carpeta zip.

3. El nombre del archivo zip es que llevarlo a la variable 'nombre_zip' que se encuentra en el archivo 'main.py', la variable se encuentra en la linea 8.

4. Ejecutar el archivo main.py.

5. Se creara una carpeta con el nombre del archivo zip en la carpeta pdf, esta carpeta contendra un archivo pdf y 6 carpetas. El archivo pdf contiene la conversacion y las carpetas los documentos seprados por tipo.

### *Nota: 

- El archivo txt que se genera no es igual en android y iphone. Este programa funciona solo con archivos zip 
provenienetes de android.


.z.la
# Requisitos

- python
- zipfile
- fpdf
- clean-text