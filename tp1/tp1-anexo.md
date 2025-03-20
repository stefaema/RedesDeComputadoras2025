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