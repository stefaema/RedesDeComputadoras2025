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
