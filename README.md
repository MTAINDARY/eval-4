# Evaluación 4: Automatización de Redes con Ansible y Python 🚀
### Sede INACAP - Ingeniería en Automatización de Redes
 
Este repositorio contiene la solución automatizada para la **Evaluación N° 4**, aplicando conceptos de **NetDevOps** e **Infraestructura como Código (IaC)** para el aprovisionamiento, endurecimiento de seguridad (hardening), auditoría programática y respaldo de un router **Cisco CSR1000v**.
 
---
 
## 👥 Integrantes
* **Martín Cortés**
* **José Tapia**
 
---
 
## 🗺️ Topología y Segmentación Lógica
El proyecto implementa un esquema de enrutamiento **Router-on-a-Stick** basado en el diseño oficial de la pauta:
 
* **Red de Gestión:** Conexión SSH a través de `GigabitEthernet1` (`192.168.56.10`).
* **Enlace Troncal:** Interfaz física `GigabitEthernet2` hacia el Switch.
* **Gateways Inter-VLAN:**
 * **VLAN 10 (PC1):** `GigabitEthernet2.10` — IP: `192.168.10.1/24`
 * **VLAN 20 (PC2):** `GigabitEthernet2.20` — IP: `192.168.20.1/24`
 * **VLAN 30 (SERVER):** `GigabitEthernet2.30` — IP: `192.168.30.1/24`
 
---
 
## 📁 Estructura del Proyecto
 
```bash
├── inventory.ini        # Inventario de Ansible (credenciales, IPs y variables de conexión).
├── config_base.yml      # Playbook de Ansible para aprovisionamiento base, VLANs y ACL.
├── validar_red.py       # Script Python (Netmiko) para auditoría, ping y desafío de email.
├── backup_config.py     # Script Python (Netmiko) para respaldar el running-config en JSON.
├── ejecutar_todo.sh     # Orquestador maestro en Bash que ejecuta el pipeline en orden.
└── README.md            # Documentación técnica (Este archivo).
```
 
---
 
## 🛠️ Resumen de las Fases del Pipeline
 
### 🔹 Fase 1: Aprovisionamiento con Ansible (`config_base.yml`)
* **Ejercicio 1:** Configuración de Hostname (`R1`), dominio corporativo (`inacap.cl`) y servidor NTP.
* **Ejercicio 2:** Levantamiento de troncal físico y subinterfaces lógicas encapsuladas en 802.1Q con sus IPs de Gateway.
* **Ejercicio 3 (Seguridad):** Bloqueo por fuerza bruta (`login block-for 60 attempts 3 within 30`), creación de usuarios (`admin` priv 15 y `operador` priv 1), hardening de líneas VTY (SSH local) e implementación de la lista de acceso perimetral `ACL_SSH_GESTION`.
 
### 🔹 Fase 2: Validación y Diagnóstico (`validar_red.py`)
* Conexión automatizada mediante la librería **Netmiko**.
* Auditoría programática de interfaces (`show ip interface brief`) y estado NTP (`show ntp status`).
* **Validación de Conectividad:** Auto-ping automático desde el router para verificar el tráfico inter-VLAN.
* **Reporte:** Exportación automatizada de evidencias estructuradas en el archivo `reporte_salud.json`.
* **Desafío (Alertas):** Integración con el módulo nativo `smtplib`. Si el script detecta un fallo crítico en la conexión, captura la excepción y gatilla una alerta de correo de inmediato al administrador.
 
### 🔹 Fase 3: Respaldo de Configuraciones (`backup_config.py`)
* Extracción remota del estado de la memoria RAM (`show running-config`) mediante Netmiko.
* Almacenamiento dinámico en formato JSON con una marca de tiempo precisa (`YYYYMMDD_HHMMSS`) para resguardar el historial de auditoría y evitar la sobreescritura de datos (ej. `backup_R1_20260708_144502.json`).
 
### 🔹 Fase 4: Orquestación Centralizada (`ejecutar_todo.sh`)
* Script de automatización en Bash que unifica y ejecuta de forma estrictamente secuencial cada una de las herramientas del ecosistema con un único comando.
 
---
 
## 🚀 Instrucciones de Uso
 
Para lanzar, auditar y respaldar toda la infraestructura de red sin intervenciones manuales, ejecute el orquestador principal desde la terminal de Linux:
 
```bash
chmod +x ejecutar_todo.sh
./ejecutar_todo.sh
```
 
---
 
> 💡 **Nota sobre Resiliencia e Idempotencia:** El playbook de Ansible garantiza alta disponibilidad. Ante un borrado completo de la memoria volátil del equipo (`running-config`), la reejecución de este pipeline reconstruye de manera autónoma los servicios de enrutamiento, VLANs, direccionamiento IP y políticas de seguridad perimetral en menos de 40 segundos.
