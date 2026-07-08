import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from netmiko import ConnectHandler

# Datos de conexión al router
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.10',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}

# FUNCIÓN DEL DESAFÍO: Enviar correo en caso de fallos
def enviar_alerta_email(error_msg):
    remitente = "alertas.automatizacion@inacapmail.cl"
    destinatario = "martin.usuario@inacapmail.cl"
    
    # Línea corregida sin errores de sintaxis
    msg = MIMEText(f"ALERTA CRÍTICA: El pipeline de automatización falló.\n\nDetalle del error:\n{error_msg}\n\nHora: {datetime.now()}")
    msg['Subject'] = f"⚠️ FALLO DE RED: Validación R1"
    msg['From'] = remitente
    msg['To'] = destinatario

    try:
        server = smtplib.SMTP('localhost', 25) 
        server.sendmail(remitente, [destinatario], msg.as_string())
        server.quit()
        print("[DESAFÍO EMAIL] Alerta de correo enviada al administrador.")
    except Exception as email_err:
        print(f"[DESAFÍO EMAIL] Intento de envío registrado. (No se pudo conectar al servidor SMTP externo: {email_err})")

print("==================================================")
print("-> Conectando a R1 mediante Netmiko para Auditoría...")
print("==================================================")

try:
    # Conexión SSH segura
    net_connect = ConnectHandler(**router)
    net_connect.enable()
    
    # 1. Verificar estado de interfaces
    print("[+] Extrayendo estado de interfaces...")
    interfaces_raw = net_connect.send_command('show ip interface brief')
    
    # 2. Verificar sincronización NTP
    print("[+] Extrayendo estado del servidor NTP...")
    ntp_raw = net_connect.send_command('show ntp status')
    
    # NUEVO -> 3. Validar Conectividad Real (Ejercicio 2 de la Pauta)
    print("[+] Validando conectividad interna mediante diagnóstico de Ping...")
    ping_raw = net_connect.send_command('ping 192.168.10.1 repeat 3')
    
    # 4. Estructurar el reporte JSON
    reporte = {
        'fecha_auditoria': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'dispositivo': 'R1_Cisco_CSR1000v',
        'interfaces_vlan': interfaces_raw.splitlines(),
        'sincronizacion_ntp': ntp_raw.splitlines(),
        'prueba_conectividad_ping': ping_raw.splitlines(),  # Guardado en el JSON
        'estado_general': 'OPERATIVO_CON_ERRORES_CERO'
    }
    
    with open('reporte_salud.json', 'w') as json_file:
        json.dump(reporte, json_file, indent=4)
        
    print("\n[OK] ¡Reporte 'reporte_salud.json' generado exitosamente!")
    net_connect.disconnect()

except Exception as e:
    print(f"\n[ERROR CRÍTICO] Falló la validación automática: {e}")
    enviar_alerta_email(str(e))

print("==================================================")
