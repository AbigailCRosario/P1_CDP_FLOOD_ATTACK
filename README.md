# CDP_DoS_ATTACK
Herramienta PoC (Proof of Concept) desarrollada en Python y Scapy para demostrar vulnerabilidades de agotamiento de recursos mediante inundación de tramas CDP (Cisco Discovery Protocol).

# 🌸 Herramienta de CDP Flood 
**Desarrollado por:** Abi.R (Matrícula 2024-1179)
**Asignatura:** Seguridad de Redes

### Demo del Proyecto
Haz clic aquí para ver el video:
https://drive.google.com/file/d/1Mo3txWWATB2Jft-pF5ZZNdKoo0TrSocz/view?usp=sharing 

---

## El Protocolo CDP: 
**CDP (Cisco Discovery Protocol)** es un protocolo de capa de enlace (Capa 2) propietario de Cisco. Su función técnica es permitir que los dispositivos de red (Routers, Switches, Teléfonos IP) anuncien su existencia a otros dispositivos conectados directamente mediante el mismo cable.

A través de CDP, un equipo transmite datos como su modelo de hardware, versión de software, y dirección IP.

### La Vulnerabilidad
El protocolo CDP, en su configuración por defecto, **carece de autenticación**. El switch confía y procesa cualquier trama CDP que recibe en sus interfaces, sin verificar si el remitente es un dispositivo Cisco legítimo o un atacante.

### Funcionamiento de la Herramienta
Este script genera y transmite tramas CDP malformadas y aleatorias a alta velocidad. Al recibir estos paquetes, el switch víctima intenta procesarlos y guardarlos en su tabla de vecinos. Debido al volumen masivo de datos falsos, la memoria del switch se agota, provocando lentitud en la administración o inestabilidad en el equipo o en otras palabras DoS.

---

## ⚙️ Configuración de Topología

La red LAN opera bajo el segmento de red `20.24.11.0/24`. A continuación, se detalla la configuración específica para cada dispositivo:

### 1. Router R1 (Gateway)
* **Interfaz:** `Ethernet0/0` (LAN)
* **Dirección IP:** `20.24.11.1`
* **Máscara:** `/24` (255.255.255.0)
* **Función:** Actúa como la Puerta de Enlace predeterminada para salir a Internet y funciona como Servidor DHCP para los clientes.

### 2. PC1 (Víctima)
* **Interfaz:** `eth0`
* **Dirección IP:** *Dinámica (DHCP)*
* **Rango esperado:** `20.24.11.x`
* **Gateway:** `20.24.11.1`
* **Descripción:** Simula un usuario normal de la red. Obtiene su configuración de red automáticamente del Router R1.

### 3. Kali Linux (Atacante)
* **Interfaz:** `eth0`
* **Dirección IP:** `20.24.11.20` (Estática)
* **Gateway:** `20.24.11.1`
* **Descripción:** Se ha configurado una IP fija manualmente para asegurar la estabilidad al ejecutar los scripts de ataque y evitar conflictos durante la suplantación.


## 🚀 Guía de Uso Paso a Paso

A continuación, se detalla el procedimiento para replicar el ataque de inundación CDP utilizando las herramientas desarrolladas.

### Paso 1: Verificación de la Topología
Antes de iniciar, confirmamos que la topología en GNS3 esté activa y conectada. El atacante (Kali) debe estar en el mismo segmento de red que el Switch objetivo.

### Paso 2: Ejecución de la Herramienta
Desde la terminal de Kali Linux, ejecutamos el script con privilegios de superusuario (`sudo`). El script detectará automáticamente nuestra IP e iniciará la inyección de paquetes.

**Comando:**
```bash sudo python3 atack_cdp_abi.py ```

**Resultado :** Veremos el banner DoSofCDP y una animación de corazones indicando que el ataque está activo y transmitiendo datos.

## Paso 3: 
Análisis de Tráfico (Wireshark) Para confirmar que los paquetes están saliendo realmente de nuestra tarjeta de red, utilizamos **Wireshark**. Aquí podemos observar las tramas CDP generadas por Scapy. Note cómo cada paquete tiene una dirección MAC de origen diferente y un "Device ID" aleatorio (ej. Router_NJCG, Router_DIPL).

## Paso 4: 
Verificación de Impacto (En el Switch) Finalmente, accedemos a la consola del Switch Cisco para verificar el éxito del ataque. Al consultar la tabla de vecinos, observamos que esta se ha saturado con cientos de dispositivos inexistentes, lo que demuestra la vulnerabilidad del equipo al procesar toda esta información basura.

**Comando en el Switch:** 
```bash: SW1-Access# show cdp neighbors```

## 🛡️ Medidas de Mitigación

El protocolo CDP viene activo por defecto en equipos Cisco ("Cisco Proprietary"). Para anular este vector de ataque, se debe deshabilitar el protocolo en las interfaces que conectan a dispositivos finales (PCs, Impresoras, Teléfonos ajenos) o zonas no confiables.

### 1. Deshabilitación por Interfaz (Best Practice)
La mejor práctica es apagar CDP solo en los puertos de acceso donde se conectan los usuarios, manteniendo activo el protocolo en los enlaces entre Switches y Routers para gestión. Según la Guías de Hardening de Cisco, pero se alinea directamente con los controles de la norma ISO/IEC 27001.

```bash
Switch(config)# interface range ethernet 0/0 - 3
Switch(config-if-range)# no cdp enable



