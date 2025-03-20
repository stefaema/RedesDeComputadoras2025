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
## 🔹 a. Conectar una PC al puerto de consola del switch Cisco a 9600 baudios utilizando PUTTY

- [ ] Conectar un cable **console** (RJ-45 a DB-9 o USB) entre el puerto de consola del switch y la PC.
- [ ] Si es necesario, instalar los **drivers** del adaptador USB a serial en la PC.
- [ ] Abrir el **Administrador de Dispositivos** en Windows y verificar el número del puerto COM asignado.
- [ ] Descargar e instalar **PuTTY** si aún no está instalado.
- [ ] Abrir **PuTTY** y configurar:
  - [ ] Tipo de conexión: **Serial**
  - [ ] Puerto **COM** detectado previamente
  - [ ] Velocidad (Baudrate): **9600**
  - [ ] Datos: **8 bits**
  - [ ] Paridad: **Ninguna**
  - [ ] Bits de parada: **1**
  - [ ] Control de flujo: **Ninguno**
- [ ] Hacer clic en **Abrir** para iniciar la sesión.
- [ ] Presionar **Enter** si no aparece el prompt del switch inmediatamente.

---

### b. Acceder a las opciones de administración del switch y modificar claves de acceso

- [ ] Conectar la PC al switch mediante **consola** (ver procedimiento a).
- [ ] Iniciar sesión en el switch. Si hay una contraseña establecida, ingresarla.
- [ ] Acceder al modo privilegiado con:
  - [ ] `enable` (y escribir la contraseña si se solicita).
- [ ] Entrar en modo de configuración global:
  - [ ] `configure terminal`
- [ ] Cambiar la contraseña de acceso al modo privilegiado:
  - [ ] `enable secret NUEVA_CONTRASEÑA`
- [ ] Cambiar la contraseña de acceso por consola:
  - [ ] `line console 0`
  - [ ] `password NUEVA_CONTRASEÑA`
  - [ ] `login`
  - [ ] `exit`
- [ ] Cambiar la contraseña de acceso por Telnet/SSH:
  - [ ] `line vty 0 4`
  - [ ] `password NUEVA_CONTRASEÑA`
  - [ ] `login`
  - [ ] `exit`
- [ ] Guardar los cambios:
  - [ ] `write memory` o `copy running-config startup-config`
- [ ] Salir de la configuración:
  - [ ] `exit`

---

### c. Conectar dos computadoras al switch, configurar una red y testear conectividad

- [ ] Conectar ambas computadoras a **puertos diferentes** del switch con cables Ethernet.
- [ ] Acceder a la interfaz del switch (ver procedimiento a).
- [ ] Verificar las interfaces activas con:
  - [ ] `show ip interface brief`
- [ ] Configurar cada PC con direcciones IP dentro de la misma subred:
  - [ ] PC1: `192.168.1.10/24`, Gateway: `192.168.1.1`
  - [ ] PC2: `192.168.1.11/24`, Gateway: `192.168.1.1`
- [ ] Comprobar la conectividad entre las PCs:
  - [ ] Abrir **Símbolo del sistema** o **Terminal** en PC1.
  - [ ] Ejecutar `ping 192.168.1.11`.
  - [ ] Si la respuesta es satisfactoria, la conexión es exitosa.

---

### d. Configurar un puerto del switch en modo mirroring y monitorear el tráfico

- [ ] Conectar una tercera computadora al switch para monitoreo.
- [ ] Acceder a la configuración del switch (ver procedimiento a).
- [ ] Identificar los puertos donde están conectadas las computadoras:
  - [ ] `show interfaces status`
- [ ] Configurar **port mirroring** (SPAN) en el switch:
  - [ ] `configure terminal`
  - [ ] `monitor session 1 source interface <puerto_PC1>`
  - [ ] `monitor session 1 source interface <puerto_PC2>`
  - [ ] `monitor session 1 destination interface <puerto_monitor>`
  - [ ] `exit`
- [ ] Instalar y ejecutar un software de captura de tráfico en la computadora de monitoreo (ej. **Wireshark**).
- [ ] Configurar Wireshark para capturar tráfico en la interfaz Ethernet correspondiente.
- [ ] Iniciar la captura y realizar pruebas de conectividad entre **PC1** y **PC2**.
- [ ] Verificar que se capturan paquetes en la computadora de monitoreo.

---
