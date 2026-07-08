import json
from datetime import datetime
from netmiko import ConnectHandler

# Datos de conexión al router Cisco
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.10',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}

# Obtener fecha y hora exacta para cumplir con la pauta en el nombre del archivo
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
archivo_backup = f'backup_R1_{timestamp}.json'

print("==================================================")
print("-> Iniciando Respaldo Automático de Configuración...")
print("==================================================")

try:
    # Conexión SSH segura usando Netmiko
    net_connect = ConnectHandler(**router)
    net_connect.enable()
    
    print("[+] Extrayendo el running-config actual de R1...")
    running_config = net_connect.send_command('show running-config')
    
    # Estructurar los datos en el formato JSON exigido por la rúbrica
    backup_data = {
        'host': '192.168.56.10',
        'dispositivo': 'R1',
        'fecha_y_hora_respaldo': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'running_config_raw': running_config
    }
    
    # Escribir el archivo JSON definitivo
    with open(archivo_backup, 'w') as json_file:
        json.dump(backup_data, json_file, indent=4)
        
    print(f"\n[OK] ¡Respaldo guardado exitosamente en: {archivo_backup}!")
    net_connect.disconnect()

except Exception as e:
    print(f"\n[ERROR CRÍTICO] No se pudo extraer el respaldo: {e}")

print("==================================================")
