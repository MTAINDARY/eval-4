#!/bin/bash

echo "========================================================"
echo " INICIANDO PIPELINE DE AUTOMATIZACIÓN - EVALUACIÓN 4"
echo "========================================================"

echo -e "\n[FASE 1] Ejecutando aprovisionamiento con Ansible..."
ansible-playbook -i inventory.ini config_base.yml

echo -e "\n[FASE 2] Ejecutando validación de salud de red con Python..."
python3 validar_red.py

echo -e "\n[FASE 3] Ejecutando respaldo de configuraciones con Python..."
python3 backup_config.py

echo -e "\n========================================================"
echo " ¡PROCESO FINALIZADO CON ÉXITO!"
echo "========================================================"
