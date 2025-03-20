# Anexo TP1: Implementación Física de la Red Propuesta

## Resumen de Características - Cisco Catalyst 2950 Series

### 1. Concepto General
- **Switches fijos y gestionados de capa 2:** Conmutación 10/100 Mbps con uplinks Gigabit.
- **Cisco IOS Standard Image (SI):** Funcionalidades básicas de datos, voz y video.
- **Administración web integrada:** Cisco Device Manager y Cisco Network Assistant.

### 2. Modelos Principales
| Modelo                 | Puertos Fast Ethernet | Uplinks |
|------------------------|----------------------|---------|
| **Cisco Catalyst 2950SX-48** | 48 × 10/100 Mbps  | 2 × 1000BASE-SX (fibra) |
| **Cisco Catalyst 2950T-48**  | 48 × 10/100 Mbps  | 2 × 10/100/1000BASE-T (cobre) |
| **Cisco Catalyst 2950SX-24** | 24 × 10/100 Mbps  | 2 × 1000BASE-SX (fibra) |
| **Cisco Catalyst 2950-24**   | 24 × 10/100 Mbps  | No |
| **Cisco Catalyst 2950-12**   | 12 × 10/100 Mbps  | No |

### 3. Rendimiento y Disponibilidad
- **Ancho de banda de conmutación:** Hasta **13.6 Gbps**.
- **Wire-speed switching** en todos los puertos.
- **Spanning Tree Protocol (STP, RSTP, MSTP, PVST+):** Redundancia sin bucles.
- **EtherChannel / LACP:** Agregación de enlaces para mayor ancho de banda.
- **Soporte de RPS (fuente de alimentación redundante).**

### 4. Funciones de Seguridad
- **802.1X (autenticación por puerto).**
- **Port Security:** Control de acceso por MAC address.
- **SSHv2:** Administración segura por CLI.
- **TACACS+ / RADIUS:** Integración con servidores de autenticación.
- **Private VLAN Edge:** Aislamiento de puertos en el switch.
- **SNMPv3 (no criptográfico):** Monitoreo seguro.

### 5. Calidad de Servicio (QoS)
- **802.1p (CoS) y clasificación de tráfico por puerto.**
- **4 colas de prioridad por puerto (Strict Priority / WRR).**
- **Soporte para priorización de tráfico de voz y video.**

### 6. Administración
- **Cisco Device Manager:** Configuración vía navegador.
- **Cisco Express Setup:** Inicio rápido sin CLI.
- **Cisco Network Assistant:** Gestión centralizada de múltiples switches.
- **SNMP (v1, v2, v3) y RMON:** Monitoreo y estadísticas.
- **CiscoWorks:** Gestión avanzada de red.

### 7. Características Físicas y Consumo
- **Factor de forma:** 1U, rackeable.
- **Dimensiones:** De **9.52” a 13” de profundidad** (según modelo).
- **Peso:** Entre **6.5 lb y 10.5 lb**.
- **Temperatura de operación:** 0°C a 45°C.
- **Consumo:** Entre **30W y 45W** según el modelo.

---

## Procedimientos para Configuración y Administración de la Red

### a. Conectar una PC al puerto de consola del switch Cisco a 9600 baudios utilizando PuTTY
- [ ] **Preparar conexión física:**
  - [ ] Conectar el cable de consola (RJ-45 a DB-9 o USB a RJ-45) entre la PC y el switch.
  - [ ] Verificar el puerto COM asignado en la PC (p. ej., usando el Administrador de Dispositivos).
- [ ] **Configurar y abrir PuTTY:**
  - [ ] Ejecutar PuTTY.
  - [ ] Seleccionar el modo **Serial**.
  - [ ] Ingresar los parámetros:
    - **Puerto COM:** (ejemplo: COM3)
    - **Baud rate:** 9600
    - **Data bits:** 8
    - **Parity:** Ninguna
    - **Stop bits:** 1
    - **Flow control:** Ninguno
  - [ ] (Opcional) Iniciar PuTTY desde la línea de comandos:
    ```
    putty.exe -serial COM3 -sercfg 9600,8,n,1,N
    ```

### b. Acceder a las opciones de administración del switch y modificar claves de acceso
- [ ] **Acceder al switch:**
  - [ ] Conectar la PC al switch (vía consola o mediante conexión Ethernet a la IP de administración).
  - [ ] Iniciar sesión usando PuTTY (o navegador si es vía web).
- [ ] **Ingresar al modo privilegiado y de configuración:**
  - [ ] Ingresar el comando para modo privilegiado:
    ```
    enable
    ```
  - [ ] Entrar al modo de configuración global:
    ```
    configure terminal
    ```
- [ ] **Modificar claves de acceso:**
  - [ ] Cambiar la contraseña del modo privilegiado:
    ```
    enable secret [nueva_contraseña]
    ```
  - [ ] (Opcional) Configurar contraseñas para acceso remoto (línea VTY):
    ```
    line vty 0 15
    password [nueva_contraseña_vty]
    login
    exit
    ```
- [ ] **Guardar la configuración:**
  - [ ] Ejecutar:
    ```
    copy running-config startup-config
    ```

### c. Conectar dos computadoras al switch, configurar una red y testear conectividad
- [ ] **Conexión física:**
  - [ ] Conectar cada computadora a un puerto del switch usando cables Ethernet.
  - [ ] Verificar que las luces de enlace en los puertos estén activas.
- [ ] **Configurar direcciones IP en cada computadora:**
  - [ ] En PC1, asignar una IP estática (ejemplo: 192.168.1.10/24) o configurar DHCP.
  - [ ] En PC2, asignar una IP estática (ejemplo: 192.168.1.11/24) o configurar DHCP.
  - [ ] (Opcional) Revisar la configuración actual:
    - En Windows:
      ```
      ipconfig /all
      ```
    - En Linux/Mac:
      ```
      ifconfig
      ```
- [ ] **Testear conectividad:**
  - [ ] En PC1, abrir la terminal y ejecutar:
    ```
    ping 192.168.1.11
    ```
  - [ ] Verificar que se reciben respuestas de PC2.

### d. Configurar un puerto del switch en modo mirroring y monitorear, con una tercera computadora, el tráfico entre las dos computadoras conectadas en el procedimiento c.
- [ ] **Conexión física:**
  - [ ] Conectar la tercera computadora al switch usando un cable Ethernet.
- [ ] **Configurar port mirroring en el switch:**
  - [ ] Acceder al modo de configuración:
    ```
    configure terminal
    ```
  - [ ] Configurar la sesión de monitorización (ejemplo: sesión 1):
    - [ ] Establecer el puerto fuente (por ejemplo, GigabitEthernet0/2):
      ```
      monitor session 1 source interface GigabitEthernet0/2
      ```
    - [ ] Establecer el puerto de destino (por ejemplo, GigabitEthernet0/3, conectado a la PC de monitoreo):
      ```
      monitor session 1 destination interface GigabitEthernet0/3
      ```
- [ ] **Guardar la configuración:**
  - [ ] Ejecutar:
    ```
    copy running-config startup-config
    ```
- [ ] **Monitorear tráfico:**
  - [ ] En la tercera computadora, abrir una herramienta de análisis de red (por ejemplo, Wireshark).
  - [ ] Iniciar la captura en la interfaz correspondiente.
  - [ ] Mientras se ejecuta el comando `ping` entre PC1 y PC2, observar el tráfico capturado.

