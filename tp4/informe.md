# Trabajo Práctico N° 4: Ruteo Externo Dinámico y Sistemas Autónomos

**Grupo**  
*NoLoSonIEEE*

**Integrantes**  
*Fernando E. Stefanovic Carroza*  
*Francisco J. Vásquez*  
*Sofía A. Ávalos*  
*Sofía Viale*  
*Tomás G. Daniel*

**Institución Educativa**  
*Universidad Nacional de Córdoba - Facultad de Ciencias Exactas, Físicas y Naturales*

**Curso**  
*Cátedra de Redes de Computadoras - Ciclo Lectivo 2025*

**Profesores**  
*Facundo N. Oliva Cuneo*  
*Santiago M. Henn*

**Fecha**  
*20/03/2025*

### Información de los Autores

**Fernando E. Stefanovic Carroza:** [*fernando.stefanovic@mi.unc.edu.ar*](mailto:fernando.stefanovic@mi.unc.edu.ar)  
**Sofia Viale:** [*sofia.viale@mi.unc.edu.ar*](mailto:sofia.viale@mi.unc.edu.ar)  
**Francisco J. Vásquez:** [*javier.vasquez@mi.unc.edu.ar*](mailto:javier.vasquez@mi.unc.edu.ar)  
**Tomas G. Daniel:** [*tomas.daniel@mi.unc.edu.ar*](mailto:tomas.daniel@mi.unc.edu.ar)  
**Sofía Aldana Ávalos:** [*aldana.avalos@mi.unc.edu.ar*](mailto:aldana.avalos@mi.unc.edu.ar)

## 1. Resumen
Este trabajo práctico explora los conceptos fundamentales del ruteo externo dinámico, centrándose en los Sistemas Autónomos (AS) y el Protocolo de Gateway Fronterizo (BGP). Se detalla la definición, estructura y función de los AS y sus números identificatorios (ASN), incluyendo la identificación del ASN de conexiones de red reales. Posteriormente, se profundiza en BGP, su funcionamiento, tipos de mensajes, y la distinción entre eBGP e iBGP. El informe también analiza las conexiones BGP de AS específicos, investiga un incidente de enrutamiento BGP con impacto significativo y concluye con una simulación práctica de una red con dos AS interconectados mediante BGP, explorando la configuración y el comportamiento del protocolo tanto en IPv4 como en IPv6.

## 2. Introducción
Internet es una vasta red de redes interconectadas, cuya operación coordinada depende de mecanismos de enrutamiento robustos y escalables. A gran escala, estas redes se organizan en Sistemas Autónomos (AS), cada uno con su propia política de enrutamiento y administración. La comunicación entre estos AS se gestiona principalmente a través del Border Gateway Protocol (BGP), el protocolo de enrutamiento exterior estándar de facto.

El presente trabajo tiene como objetivo principal comprender la estructura y el funcionamiento de los Sistemas Autónomos y el protocolo BGP. Se investigarán los números de AS (ASN), su conformación y ejemplos relevantes. Se analizará en detalle BGP, sus procedimientos funcionales, tipos de mensajes, y las diferencias entre sus variantes interna y externa. Además, se realizarán análisis prácticos de conexiones AS y se estudiará un caso histórico de fallo de enrutamiento BGP. Finalmente, se llevará a cabo una simulación en Packet Tracer para consolidar los conocimientos adquiridos sobre la configuración y operación de BGP en un entorno controlado.

## 3. Desarrollo

### 3.1. Sistemas Autónomos (AS) y Números de Sistema Autónomo (ASN)

#### 3.1.1. Definición de Sistema Autónomo (AS)
Un **Sistema Autónomo (Autonomous System - AS)** es un conjunto de redes IP (bloques de direcciones IP llamados "prefijos") que operan bajo una **única política de enrutamiento externa claramente definida** y son administradas por una **única entidad administrativa**.

**Características Clave:**

*   **Administración Única:** Una sola organización (como un proveedor de servicios de Internet (ISP), una gran empresa, una universidad o una agencia gubernamental) es responsable de la gestión y operación del AS.
*   **Política de Enrutamiento Común:** Todas las redes dentro del AS comparten y siguen las mismas reglas sobre cómo se enruta el tráfico hacia y desde otras redes externas (otros AS).
*   **Identificación Única:** Cada AS se identifica globalmente mediante un número único llamado ASN (Autonomous System Number).
*   **Protocolos de Enrutamiento:**
    *   **Internamente (Intra-AS):** Utilizan un Protocolo de Gateway Interior (IGP) como OSPF (Open Shortest Path First) o IS-IS (Intermediate System to Intermediate System) para intercambiar información de enrutamiento *dentro* del propio AS.
    *   **Externamente (Inter-AS):** Utilizan un Protocolo de Gateway Exterior (EGP), siendo **BGP (Border Gateway Protocol)** el estándar de facto en Internet, para intercambiar información de enrutamiento *entre* diferentes AS.

En esencia, Internet está compuesto por una vasta red de Sistemas Autónomos interconectados que intercambian información de alcance (reachability) usando BGP.

#### 3.1.2. El Número de Sistema Autónomo (ASN)
Un **Autonomous System Number (ASN)** es un **identificador numérico único** asignado a cada Sistema Autónomo. Es utilizado principalmente por el protocolo BGP para identificar de forma única a cada red en Internet y para aplicar políticas de enrutamiento entre ellas.

**Conformación y Tipos:**

1.  **Formato Original (16 bits):**
    *   Inicialmente, los ASN eran números de 16 bits (rango 0-65535).
    *   **Rango Público:** 1 a 64511. Asignados por IANA a través de los Registros Regionales de Internet (RIRs como ARIN, RIPE NCC, APNIC, LACNIC, AFRINIC). Deben ser globalmente únicos.
    *   **Rango Privado:** 64512 a 65534. Pueden ser utilizados internamente por organizaciones para comunicación entre redes propias que usan BGP, pero *no deben* ser anunciados a la Internet pública global. Similar a las direcciones IP privadas (RFC 1918).
    *   **Reservados:** 0 y 65535 son reservados.

2.  **Formato Extendido (32 bits):**
    *   Debido al agotamiento del espacio de 16 bits, se introdujeron los ASN de 32 bits (definido en RFC 4893 y actualizado por RFC 6793).
    *   Esto amplió el rango a 0 a 4294967295 ($2^{32} - 1$).
    *   **Rango Público:** Incluye los números de 16 bits y se extiende hasta 4200000000 - 1.
    *   **Rango Privado:** 4200000000 a 4294967294.
    *   **Representación:** Los ASN de 32 bits se pueden escribir como un número entero simple (ej., `262144`) o en notación "asdot" (ej., `3.65536`, donde el primer número es el valor de los 16 bits superiores y el segundo el de los 16 bits inferiores).

La asignación de ASN públicos requiere una justificación técnica ante el RIR correspondiente, demostrando la necesidad de una política de enrutamiento externa única o interconexión con múltiples AS.

#### 3.1.3. Ejemplos de ASN en Diferentes Entidades
A continuación, se presentan ejemplos de ASN pertenecientes a diversas organizaciones:

1.  **Empresa (Google LLC):**
    *   **ASN:** `AS15169`
    *   **Nombre:** GOOGLE
    *   **Descripción:** Este es uno de los principales ASN utilizados por Google para su infraestructura global y servicios como búsqueda, YouTube, Google Cloud, etc.

2.  **Universidad (Massachusetts Institute of Technology):**
    *   **ASN:** `AS3`
    *   **Nombre:** MIT-GATEWAYS
    *   **Descripción:** El MIT fue una de las primeras organizaciones en obtener un ASN, por eso tiene un número tan bajo. Lo utiliza para la red de su campus.

3.  **Organización (RIPE NCC - Réseaux IP Européens Network Coordination Centre):**
    *   **ASN:** `AS3333`
    *   **Nombre:** RIPE-NCC-AS
    *   **Descripción:** ASN perteneciente a uno de los Registros Regionales de Internet (RIR), responsable de la asignación de recursos de numeración de Internet (IPs, ASNs) en Europa, Medio Oriente y partes de Asia Central.

#### 3.1.4. Identificación del ASN de la Conexión Actual y Protocolos Soportados
Para averiguar el ASN de la conexión actual, se utilizó la herramienta en línea proporcionada por `bgp.he.net`.

*   **ASN:** `AS11664`
*   **Nombre de la Organización:** `Techtel LMDS Comunicaciones Interactivas S.A.`
*   **País:** `AR - Argentina`

**Protocolos Soportados por el AS:**
La información sobre qué protocolos específicos soporta un AS (más allá de BGP para interconexión) generalmente se deduce de los prefijos que anuncia y los servicios que ofrece el propietario del AS:

*   **IPv4:** Casi todos los AS del mundo anuncian prefijos IPv4. Esto se puede confirmar buscando los prefijos IPv4 anunciados por el ASN en herramientas como Hurricane Electric BGP Toolkit (`bgp.he.net`).
*   **IPv6:** La mayoría de los ISPs modernos y grandes organizaciones también anuncian prefijos IPv6. Si el ASN anuncia bloques IPv6, significa que soporta enrutamiento IPv6 en su red troncal.
*   **Multicast:** El soporte de multicast (para transmitir datos de uno a muchos) es más complejo. BGP puede usarse para transportar información de enrutamiento multicast entre AS (usando extensiones como MBGP), pero el soporte real depende de la implementación de protocolos multicast (como PIM) dentro de su red y acuerdos de peering multicast. Generalmente, se asume soporte básico si el ISP ofrece servicios que lo requieren (como IPTV gestionada).

Para el ASN `AS11664`, la verificación en `bgp.he.net` confirma el anuncio de prefijos IPv4. El soporte para IPv6 y multicast por parte de `Techtel LMDS Comunicaciones Interactivas S.A.` requeriría un análisis más detallado de sus anuncios y servicios.

### 3.2. Border Gateway Protocol (BGP)

#### 3.2.1. Definición de BGP
El **Border Gateway Protocol (BGP)** es el protocolo de enrutamiento exterior (Exterior Gateway Protocol - EGP) estándar de Internet. Su función principal es **intercambiar información de enrutamiento y alcanzabilidad entre diferentes Sistemas Autónomos (AS)**.

A diferencia de los protocolos de enrutamiento interior (Interior Gateway Protocols - IGPs) como OSPF o IS-IS, que se enfocan en encontrar la ruta más rápida *dentro* de una red única (un AS), BGP se enfoca en determinar las rutas *entre* las grandes redes que componen Internet (los AS).

**Características Clave de BGP:**

1.  **Protocolo de Vector de Rutas (Path Vector):** BGP toma decisiones de enrutamiento basadas en **rutas (paths)**, que son secuencias de números de AS (AS_PATH) por los que debe pasar el tráfico para llegar a un destino. También considera **políticas** definidas por los administradores de red, no solo métricas técnicas como la velocidad o el número de saltos.
2.  **Fiabilidad:** Utiliza **TCP (Transmission Control Protocol)** como protocolo de transporte en el **puerto 179**. TCP garantiza una entrega ordenada y fiable de los mensajes BGP entre routers vecinos (peers).
3.  **Escalabilidad:** Está diseñado para manejar la enorme tabla de enrutamiento global de Internet. Utiliza actualizaciones incrementales.
4.  **Basado en Políticas:** Permite a las organizaciones implementar políticas complejas sobre cómo se anuncia su red y qué rutas prefieren.
5.  **Tipos de Sesiones:**
    *   **eBGP (External BGP):** Se establece entre routers en *diferentes* AS.
    *   **iBGP (Internal BGP):** Se establece entre routers *dentro* del mismo AS para distribuir rutas eBGP aprendidas.

En resumen, BGP es el protocolo que permite que las redes independientes (AS) se comuniquen y dirijan el tráfico globalmente basándose en rutas y políticas.

#### 3.2.2. Funcionamiento de BGP: Procedimientos Funcionales
El funcionamiento de BGP se puede entender a través de tres procedimientos clave:

##### 3.2.2.1. Adquisición de Vecino (Neighbor Acquisition)
Este proceso establece una sesión BGP entre dos routers configurados como vecinos.
*   **Configuración Manual:** Los administradores configuran explícitamente la IP y el AS del vecino.
*   **Conexión TCP:** Se inicia una conexión TCP al puerto 179 del vecino.
*   **Intercambio de Mensajes `OPEN`:** Contienen:
    *   **Versión de BGP:** (Actual: BGP-4).
    *   **Mi AS (My Autonomous System):** ASN del emisor.
    *   **Hold Time:** Tiempo máximo sin recibir `KEEPALIVE` o `UPDATE` antes de declarar la conexión caída. Se negocia el mínimo.
    *   **BGP Identifier:** IP única (usualmente loopback) que identifica al router BGP.
    *   **Parámetros Opcionales:** Capacidades adicionales (soporte MP-BGP, ASN de 4 bytes, etc.).
*   **Establecimiento de la Sesión:** Si los parámetros son aceptados, se responde con `KEEPALIVE` y la sesión pasa a **Established**. Errores resultan en `NOTIFICATION` y cierre de conexión.

##### 3.2.2.2. Detección de Vecino Alcanzable (Neighbor Reachability)
Mecanismo para asegurar que el vecino sigue activo.
*   **Mensajes `KEEPALIVE`:** Intercambiados periódicamente (típicamente cada tercio del Hold Time).
*   **Detección de Fallo:** Si no se recibe `KEEPALIVE` o `UPDATE` dentro del Hold Time, se asume fallo.
*   **Acción ante Fallo:** Sesión BGP y conexión TCP se cierran, rutas aprendidas del vecino se eliminan. Se intenta restablecer la sesión.

##### 3.2.2.3. Detección de Red Alcanzable (Network Reachability)
Compartición de información sobre qué redes (prefijos IP) son alcanzables y por qué camino.
*   **Mensajes `UPDATE`:** Intercambian toda la información de rutas. Pueden anunciar nuevas rutas o retirar rutas inválidas.
*   **Contenido de un Mensaje `UPDATE`:**
    *   **Withdrawn Routes:** Lista de prefijos IP ya no alcanzables.
    *   **Path Attributes (PAs):** Características de la ruta (ej., `AS_PATH`, `NEXT_HOP`, `ORIGIN`, `LOCAL_PREF`, `MED`).
    *   **Network Layer Reachability Information (NLRI):** Lista de prefijos IP alcanzables a través de la ruta descrita.
*   **Proceso:** Se envían `UPDATE` solo con cambios (incremental).