# Trabajo Práctico N° 1: Configuración y Análisis de Tráfico IPv4/IPv6

**Grupo**  
*NoLoSonIEEE*

**Integrantes**  
*Fernando E. Stefanovic Carroza*  
*Francisco J. Vásquez*  
*Sofía A. Ávalos*  
*Sofía Viale*  
*Tomás G. Daniel*

**Institución Educativa**  
*Universidad Nacional de Córdoba \- Facultad de Ciencias Exactas, Físicas y Naturales*

**Curso**  
*Cátedra de Redes de Computadoras \- Ciclo Lectivo 2025*

**Profesores**  
*Facundo N. Oliva Cuneo*  
*Santiago M. Henn*

**Fecha**  
*20/03/2025*

### Información de los Autores

**Fernando E. Stefanovic Carroza:** [*fernando.stefanovic@mi.unc.edu.ar*](mailto:fernando.stefanovic@mi.unc.edu.ar)  
**Sofia Viale:** [*sofia.viale@mi.unc.edu.ar*](mailto:sofia.viale@mi.unc.edu.ar)

\[TODO: Rellenar el resto con sus mails\]

## Resumen
En este trabajo se llevó a cabo la configuración y análisis de una red de computadoras con soporte para IPv4 e IPv6. Se implementó un esquema de interconexión utilizando dispositivos de red que permiten la comunicación entre distintas subredes, evaluando la correcta operación del enrutamiento y la resolución de direcciones. Para verificar la integridad de la red, se realizaron pruebas funcionales mediante el uso de comandos ping y herramientas de captura de tráfico, analizando los mensajes ICMP generados. Se inspeccionaron en detalle los protocolos ARP y NDP, observando su rol en la comunicación y comparación en ambos entornos de direccionamiento. Los resultados obtenidos permitieron validar el correcto funcionamiento de la infraestructura de red, asegurando la conectividad entre dispositivos y la efectividad de los protocolos utilizados.

**Palabras clave**: _Redes de computadoras, IPv4, IPv6, ICMP, ARP, NDP, enrutamiento, conectividad._

## Introducción

El crecimiento de las redes de computadoras ha impulsado la necesidad de protocolos eficientes que permitan la comunicación entre dispositivos en distintos entornos. IPv4 ha sido el estándar predominante, pero su limitación en el espacio de direccionamiento ha motivado la transición progresiva hacia IPv6, el cual ofrece mayor escalabilidad y eficiencia en la gestión de la red.

En este trabajo se implementó una infraestructura de red utilizando ambas versiones del protocolo IP para evaluar su funcionamiento y comportamiento en términos de conectividad y resolución de direcciones. Se estableció un esquema de interconexión que involucra múltiples dispositivos y se realizaron pruebas de tráfico utilizando ICMP e ICMPv6.

El objetivo principal fue analizar la integridad de la red a nivel funcional y protocolar, inspeccionando los mecanismos de descubrimiento de vecinos y enrutamiento. Para ello, se utilizaron herramientas de simulación que permitieron evaluar el flujo de paquetes y la interacción entre los protocolos de capa de red y enlace de datos.

Este análisis proporciona una comprensión detallada sobre las diferencias y similitudes en la operación de IPv4 e IPv6, destacando el reemplazo de ARP por NDP en la nueva versión del protocolo y la eliminación del concepto de broadcast en favor de multicast. A través de este estudio, se validó la correcta configuración de la red y se verificó su operatividad en distintos escenarios de comunicación.

## Marco Teórico

### Principio de la Interconexión entre Redes

La interconexión de redes es esencial para el diseño y la operatividad de las infraestructuras de comunicación, ya que **posibilita la comunicación entre dispositivos y sistemas distribuidos en redes diferentes**. Para asegurar la interoperabilidad entre equipos de diversos fabricantes y tecnologías, la comunicación se organiza en capas, según modelos como el OSI (Open Systems Interconnection) y la arquitectura TCP/IP. Cada capa cumple funciones específicas que, en conjunto, facilitan la compatibilidad y el intercambio eficiente de información entre sistemas heterogéneos, como el que se muestra en la Figura 1.

![Interconexión entre Redes](image-1.png)\
_Figura 1. Interconexión típica de Redes._

### Importancia de la Arquitectura en Capas

Dentro del contexto de la interconexión de redes, se evidencia la adopción del patrón arquitectónico basado en capas. Este enfoque permite descomponer funciones complejas en módulos independientes, facilitando tanto el diseño como el mantenimiento de las infraestructuras. Cada capa asume responsabilidades específicas—desde la transmisión de bits hasta el enrutamiento y la gestión de aplicaciones—permitiendo que distintos protocolos y tecnologías interactúen de manera estructurada y eficiente. Esta organización modular no solo simplifica la implementación y solución de problemas, sino que también logra una de las mejores características que puede existir para las tecnologías que gobiernan nuestra actualidad: **la interoperabilidad entre dispositivos heterogéneos**, abarcando diferencias entre fabricantes, arquitecturas, propósitos e incluso grados de obsolescencia.

### Dispositivos de Red

Debido a la adopción de la arquitectura basada en capas en los sistemas de red, **surge de manera natural la especialización de dispositivos para cada capa específica**. Se utilizan, por ejemplo e ilustrados en la Figura 2, enrutadores o routers para gestionar las operaciones de la capa de red, encargados del encaminamiento y la determinación de rutas óptimas, y conmutadores o switches, que operan en la capa de enlace, facilitando la transmisión de datos en el ámbito local. Además, existen otros dispositivos especializados como puntos de acceso, firewalls y servidores proxy, que complementan la infraestructura, contribuyendo a la seguridad y al control del tráfico de datos en la red.

![Dispositivos de Red](image.png)\
_Figura 2. Dispositivos de Red Típicos._

#### El rol de los Switches en las Redes
En una red, los switches desempeñan un papel crucial en la entrega eficiente de tramas Ethernet dentro de una misma subred. Mientras que los routers operan en la Capa 3 (Red) y son responsables de la interconexión entre redes distintas, los switches trabajan en la Capa 2 (Enlace de Datos), facilitando la comunicación entre dispositivos dentro de la misma red local.


Los switches almacenan direcciones MAC en una tabla de conmutación o tabla CAM (Content Addressable Memory), lo que les permite reenviar tramas únicamente a los puertos donde se encuentran los dispositivos de destino, en lugar de retransmitirlas a toda la red. Este proceso optimiza la eficiencia y reduce la congestión dentro del dominio de broadcast.


Dado que el switch no opera en la capa de red, no requiere una dirección IP para su funcionamiento en una red conmutada. Sin embargo, algunos switches administrables permiten configurar direcciones IP para su gestión remota.


En el contexto del presente trabajo, el switch interconecta los hosts h2 y h3, facilitando la transmisión de tramas dentro de la subred 192.168.2.0/24 en IPv4 y 2001:aaaa:cccc:1::/64 en IPv6, permitiendo la comunicación sin necesidad de un router cuando ambos dispositivos se encuentran en la misma red.


### Cómo los Dispositivos de Red Comunican Datos


El proceso de comunicación entre dispositivos de red se basa en el **principio de encapsulación de datos**. Conforme la información desciende por las capas del modelo, cada nivel añade su propia información de control en forma de encabezados (y, en algunos casos, trailers) al paquete original. Estos encabezados contienen datos específicos—como direcciones de origen y destino, protocolos de control y mecanismos de verificación—que aseguran que la información se transmita de forma íntegra y llegue correctamente a su destino. Durante el trayecto, routers y switches realizan **procesos de verificación y decapsulación parcial**, analizando la dirección de destino para elegir la ruta más adecuada mediante el encaminamiento (routing) y transfiriendo el paquete a la siguiente etapa mediante el reenvío (forwarding).


Además, en cada nodo intermedio de la red, los dispositivos aplican algoritmos que analizan factores críticos como la congestión, el número de saltos (hops) y la disponibilidad de rutas, permitiendo así evitar cuellos de botella y optimizar la entrega de datos. **Los mecanismos de control de congestión y calidad de servicio** (QoS) desempeñan un papel clave en redes complejas, priorizando paquetes críticos—como aquellos utilizados en aplicaciones sensibles a la latencia, como VoIP o transmisión en tiempo real—sobre otros tipos de tráfico. En conjunto, estos procesos permiten que, incluso en condiciones de alta demanda o en presencia de fallos, los dispositivos puedan redirigir los paquetes a través de rutas alternativas, manteniendo la integridad y el rendimiento del sistema de comunicación.


### Enfoques de Interconexión: Orientado a Conexión vs. Sin Conexión


La interconexión de redes puede clasificarse en dos enfoques principales: orientado a conexión y sin conexión. Cada uno presenta características distintas que determinan cómo se establece y mantiene la comunicación entre dispositivos.


En el enfoque **orientado a conexión**, se establece un canal de comunicación antes de enviar cualquier dato. Este método garantiza una entrega ordenada y confiable de los paquetes, asegurando que cada uno siga la misma ruta y llegue en el orden correcto. El **Protocolo de Control de Transmisión** (TCP, por sus siglas en inglés) es un ejemplo de este tipo de comunicación. TCP proporciona mecanismos de control de errores y retransmisión en caso de pérdida, asegurando que todos los paquetes enviados sean recibidos y ensamblados correctamente en el destino.


Por otro lado, la **interconexión sin conexión** no requiere la creación previa de un canal antes del envío de datos. Los paquetes se transmiten de manera independiente y pueden tomar rutas distintas según el estado actual de la red. Un ejemplo característico de este enfoque es el **Protocolo de Internet** (IP), el cual no garantiza ni la entrega ni el orden de los paquetes, delegando esta responsabilidad a los dispositivos receptores, que deben encargarse del reensamblado y detección de errores.


El enfoque sin conexión brinda mayor flexibilidad y eficiencia en redes dinámicas, ya que permite que los paquetes tomen rutas distintas en caso de congestión o fallos en la infraestructura. Sin embargo, como IP no garantiza la entrega de los paquetes ni su orden de llegada, es necesario utilizar protocolos adicionales en las capas superiores, como TCP, cuando se requiere una comunicación fiable. TCP complementa a IP proporcionando control de errores, confirmación de entrega y reensamblado de los paquetes en el orden correcto, asegurando así una transmisión de datos más confiable en aplicaciones que lo necesiten.


### Cómo los Dispositivos de Red se Identifican y Enrutan en la Red


En una red, cada dispositivo necesita un identificador único que le permita ser reconocido dentro del entorno de comunicación. En el nivel más básico, esta función es realizada por la **dirección MAC (Media Access Control)**, un identificador asignado de forma única a cada tarjeta de red durante su fabricación. Esta dirección, representada en un formato hexadecimal, está asociada físicamente al hardware y permite la comunicación entre dispositivos dentro de una misma red local.


Sin embargo, en redes más amplias y estructuradas, donde la comunicación no se limita a un solo segmento de red, es necesario un esquema de direccionamiento que permita la identificación y localización de dispositivos a través de múltiples redes. Para ello, entra en juego el **Protocolo de Internet** (IP), que asigna a cada dispositivo una dirección lógica que puede cambiar dependiendo de la red en la que se encuentre. Esta dirección IP, utilizada en conjunto con mecanismos de enrutamiento, permite que los paquetes de datos sean dirigidos de manera eficiente desde un origen hasta su destino, incluso a través de diferentes redes interconectadas.


IP es el pilar fundamental de la comunicación en Internet y en redes privadas, operando en la **capa de red** del modelo OSI y formando parte de la suite de protocolos TCP/IP. A lo largo de su evolución, se han desarrollado dos versiones principales: **IPv4 e IPv6**, cada una con características diseñadas para responder a los desafíos del crecimiento exponencial de dispositivos conectados y la necesidad de mayor seguridad y eficiencia en la transmisión de datos.


#### IPv4: La Base del Protocolo IP


El **Protocolo de Internet versión 4** (IPv4) ha sido el estándar dominante en redes desde la década de 1980\. Utiliza direcciones de 32 bits, lo que permite aproximadamente 4.3 mil millones de direcciones únicas. Si bien esta cantidad era suficiente en sus inicios, el crecimiento exponencial de dispositivos conectados ha generado una escasez de direcciones, lo que ha requerido la implementación de soluciones temporales como la **Traducción de Direcciones de Red** (NAT, Network Address Translation). NAT permite que múltiples dispositivos dentro de una red privada compartan una única dirección IP pública, mitigando la falta de direcciones, pero a costa de generar problemas en ciertas aplicaciones, aumentando la latencia y dificultando la conectividad extremo a extremo.


Otro inconveniente de IPv4 es su dependencia de mecanismos como **DHCP (Dynamic Host Configuration Protocol)** para la asignación de direcciones IP. En redes dinámicas con una alta rotación de dispositivos, este método puede generar una mayor complejidad en la administración y en la configuración inicial de la red.


El protocolo opera mediante el envío de datagramas, donde cada paquete es tratado de forma independiente y puede tomar rutas diferentes hasta su destino. Aunque esto proporciona flexibilidad, también introduce desafíos como el desorden en la recepción o la pérdida de paquetes, problemas que son resueltos mediante protocolos complementarios como **TCP**, que garantiza el reensamblado y la integridad de los datos.


A pesar de haber sido un pilar fundamental en la evolución de Internet, las limitaciones de IPv4 en términos de espacio de direcciones, seguridad y eficiencia en la transmisión fueron evidenciandose al punto en el que cada día esta tecnología se acerca a un estado de obsolescencia.