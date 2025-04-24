<center>

# Trabajo Práctico N° 3: Evaluación de Performance en Redes y Ruteo Interno Dinámico OSPF


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
**Francisco J. Vásquez:**: [*javier.vasquez@mi.unc.edu.ar*](mailto:javier.vasquez@mi.unc.edu.ar)  
**Tomas G. Daniel:** [*tomas.daniel@mi.unc.edu.ar*](mailto:tomas.daniel@mi.unc.edu.ar)  
**Sofía Aldana Ávalos** [*aldana.avalos@mi.unc.edu.ar*](mailto:aldana.avalos@mi.unc.edu.ar)  

</center>

---

## 1. Resumen

## 2. Introducción

### 2.1. El Enrutamiento Dinámico y su Importancia

En el ámbito de las redes de computadoras, el enrutamiento es el proceso fundamental de seleccionar caminos para dirigir el tráfico IP entre distintos segmentos de red. Si bien el enrutamiento estático, donde las rutas se configuran manualmente, es viable en redes pequeñas y estables, presenta limitaciones significativas en entornos más complejos y dinámicos. La configuración manual es propensa a errores, no se adapta automáticamente a cambios en la topología (como fallos de enlace o adición de nuevos routers) y su gestión se vuelve impracticable a medida que la red crece.

Para superar estas limitaciones, surgen los protocolos de enrutamiento dinámico. Estos protocolos, que se integran a la extensa suite de protocolos que gobiernan internet, permiten a los routers intercambiar información sobre la topología de la red y calcular automáticamente las mejores rutas. Se clasifican principalmente en Protocolos de Gateway Interior (IGP) y Protocolos de Gateway Exterior (EGP), y se diferencian en cómo administran al Sistema Autónomo (AS - Autonomous System).

#### 2.1.1. Sistemas Autónomos (ASs)

Un Sistema Autónomo (AS) representa una colección de redes bajo el control de una única entidad administrativa (como un ISP, una empresa o institución) que presenta una política de enrutamiento común hacia el exterior. 

Internet puede visualizarse como una interconexión de múltiples ASs. Cada AS gestiona su propia red interna y decide cómo enrutar el tráfico dentro de sus límites. Para identificarse globalmente y permitir la comuniación, a cada AS se le asigna un número único conocido como ASN (Autonomous System Number), que permite ser usado como punto de entrada para protocolos de enrutamiento.

#### 2.1.2. Protocolos de Gateway Interior (IGP)

Los Protocolos de Gateway Interior (IGP) están diseñados para operar **dentro** de los límites de un único Sistema Autónomo. Su principal objetivo es descubrir la topología de la red interna del AS y calcular las rutas más eficientes (basadas en métricas como el número de saltos, el ancho de banda, el retardo o el costo) entre los diferentes routers y subredes dentro de ese AS.

Para lograr esto, los IGPs emplean diferentes algoritmos y métodos de intercambio de información, lo que lleva a su clasificación principal en dos familias: protocolos de **Vector Distancia** (que aprenden rutas a través de la información resumida de sus vecinos) y protocolos de **Estado de Enlace** (que construyen un mapa completo de la topología basado en información detallada de todos los routers).

Se encuentran ejemplos de implementación en ambas familias, tales como RIP (un clásico de vector distancia) u OSPF e IS-IS (prominentes ejemplos de estado de enlace), además de enfoques híbridos como EIGRP. Independientemente de su mecanismo subyacente, todos actúan como un *sistema de navegación para los datos dentro de una colección de redes*, determinando las mejores rutas locales dentro de esa colección para conectar orígenes con destinos en la misma.

De esta forma, un IGP adecuado brinda eficiencia en el ruteo y permite una convergencia rápida ante cambios de topología o ajustes de escala que puedan surgir en el Sistema Autónomo donde esté implementado.

#### 2.1.3. Protocolos de Gateway Exterior (EGP)

Los Protocolos de Gateway Exterior (EGP) se utilizan para intercambiar información de enrutamiento **entre** diferentes Sistemas Autónomos. Su función principal es permitir que los ASs se comuniquen entre sí sobre qué redes son alcanzables a través de ellos, basándose en políticas de enrutamiento definidas administrativamente.

En este caso, el enfoque está en brindarle a internet su escalabilidad global tan característica, permitiendo introducir en las decisiones de enrutamiento aspectos que van más allá de lo puramente técnico, como acuerdos comerciales o políticos entre las organizaciones que administran los Sistemas Autónomos.


### 2.2. OSPF (Open Shortest Path First): Un Protocolo de Estado de Enlace

Como se introdujo en la sección anterior (2.1.2), Open Shortest Path First (OSPF) es un protocolo de enrutamiento de **estado de enlace**, estandarizado y ampliamente utilizado dentro de la familia de los IGPs. Su diseño robusto y abierto lo ha convertido en una opción predilecta para redes empresariales y de proveedores de servicios. Existen dos versiones principales: **OSPFv2 (RFC 2328)** para redes IPv4 y **OSPFv3 (RFC 5340)**, que extiende el soporte a IPv6 y puede manejar múltiples familias de direcciones.

A diferencia de los protocolos de vector distancia que dependen de la información fragmentada de los vecinos, la filosofía de OSPF se basa en que cada router obtenga una visión completa y sincronizada de la topología de la red (o al menos, del área a la que pertenece) antes de tomar decisiones de enrutamiento. Esto se logra mediante el intercambio organizado de información detallada sobre la conectividad (LSAs), la construcción de un mapa interno de la red (LSDB) y la ejecución de un algoritmo para calcular las mejores rutas (SPF).

#### 2.2.1. Modelo Operativo del OSPF

El corazón de OSPF reside en su naturaleza de estado de enlace, siguiendo un proceso lógico:

1.  **Descubrimiento de Vecinos**: Los routers OSPF envían paquetes periódicos llamados "Hello" por sus interfaces habilitadas (GigabitEthernet0/0, etc.). Estos mensajes permiten a los routers descubrir otros routers OSPF en los mismos enlaces y establecer relaciones de vecindad (conocidas como *adjacencies*). Esta es la base para poder intercambiar información más detallada.
2.  **Intercambio de Información Topológica (LSAs)**: Una vez establecida la adyacencia, los routers comienzan a intercambiar mensajes detallados sobre el estado de sus propios enlaces y conexiones, denominados **Link-State Advertisements (LSAs)**. Cada router genera LSAs describiendo sus interfaces activas, a qué redes están conectadas, qué vecinos ha alcanzado por esas interfaces y el costo asociado a cada enlace. Estos anuncios son distribuidos (inundados o *flooded*) a todos los demás routers dentro de la misma zona de la red (área).
3.  **Construcción del Mapa de Red (LSDB)**: Cada router recopila todos los LSAs válidos recibidos de los demás routers dentro de su área y los organiza en su propia **base de datos de estado de enlace (Link-State Database - LSDB)**. Idealmente, todos los routers en la misma área construirán LSDBs idénticas, las cuales representan un mapa completo y sincronizado de esa porción de la red.
4.  **Cálculo de las Mejores Rutas (Algoritmo SPF)**: Con este mapa completo (la LSDB) ya construido, cada router ejecuta independientemente el algoritmo **Shortest Path First (SPF)**. Tratándose a sí mismo como el punto de partida, calcula la ruta de menor costo acumulado hacia cada destino (otras redes o routers) basándose en la información del mapa.
5.  **Poblar la Tabla de Enrutamiento (RIB)**: Los resultados del algoritmo SPF (las rutas óptimas calculadas) se instalan en la **Tabla de Información de Enrutamiento (Routing Information Base - RIB)** del router, que es la tabla que el router consulta para reenviar el tráfico de datos.

Este proceso, basado en que todos los routers comparten y calculan sobre la misma visión completa de la topología, asegura que las decisiones de enrutamiento sean consistentes y elimina inherentemente los bucles de enrutamiento dentro del área.

#### 2.2.2. Anuncios de Estado de Enlace (LSAs)

Los **Link-State Advertisements (LSAs)** son las unidades fundamentales de intercambio de información en OSPF. Corresponden a los "mensajes detallados sobre el estado de los propios enlaces" mencionados anteriormente. Cada LSA es un paquete de datos estructurado que describe un aspecto específico de la topología de la red desde la perspectiva del router que lo originó. La distribución controlada (*flooding*) de estos LSAs permite que todos los routers construyan su visión de la red.

Cada LSA tiene un propósito específico, identificado por su **número de Tipo**, y contribuye a la construcción de la LSDB. Los tipos de LSA más fundamentales en OSPFv2 para el enrutamiento unicast son:

*   **LSA Tipo 1 (Router LSA):**
    *   **Generado por:** Cada router OSPF.
    *   **Describe:** Los enlaces (interfaces) directamente conectados del router, su estado (activo/inactivo), su dirección IP, la máscara de subred y el costo OSPF asociado. También indica si el router es un ABR (Router de Borde de Área) o ASBR (Router de Borde de Sistema Autónomo).
    *   **Ámbito:** Se inunda (*flooded*) únicamente dentro del área OSPF a la que pertenece el router que lo originó.

*   **LSA Tipo 2 (Network LSA):**
    *   **Generado por:** El Router Designado (DR) en redes multiacceso (Broadcast o NBMA).
    *   **Describe:** El segmento de red multiacceso en sí y la lista de routers (incluido el DR) conectados a ese segmento.
    *   **Ámbito:** Se inunda únicamente dentro del área donde reside el segmento multiacceso.

*   **LSA Tipo 3 (Summary LSA):**
    *   **Generado por:** Los Routers de Borde de Área (ABRs).
    *   **Describe:** Rutas hacia redes que se encuentran en *otras* áreas (rutas inter-área). Anuncia la dirección de red, la máscara y el costo acumulado desde el ABR hasta esa red. Permite el resumen de rutas entre áreas.
    *   **Ámbito:** Se inunda desde el ABR hacia las áreas conectadas, incluyendo el backbone (Área 0), pero *no* entra en las áreas Stub (y sus variantes, excepto NSSA para rutas internas resumidas).

*   **LSA Tipo 5 (AS External LSA):**
    *   **Generado por:** Los Routers de Borde de Sistema Autónomo (ASBRs).
    *   **Describe:** Rutas hacia destinos *externos* al dominio OSPF (por ejemplo, rutas aprendidas de otro protocolo de enrutamiento como BGP o EIGRP, o rutas estáticas redistribuidas). Anuncia la red externa, máscara, métrica externa y tipo de métrica (E1 o E2).
    *   **Ámbito:** Se inunda a través de *todo* el dominio OSPF (todas las áreas estándar y backbone), excepto las áreas Stub y sus variantes (Stub, Totally Stubby, NSSA).

*   **LSA Tipo 7 (NSSA External LSA):**
    *   **Generado por:** Los ASBRs ubicados *dentro* de un área NSSA (Not-So-Stubby Area).
    *   **Describe:** Rutas externas, de manera similar al LSA Tipo 5, pero específicamente para ser originadas dentro de una NSSA.
    *   **Ámbito:** Se inunda únicamente *dentro* del área NSSA donde se originó. El ABR de esa NSSA es responsable de traducir (si es necesario) estos LSAs Tipo 7 en LSAs Tipo 5 para propagarlos al resto del dominio OSPF (Área 0 y otras áreas).

#### 2.2.3. Base de Datos de Estado de Enlace (LSDB)

La **Link-State Database (LSDB)** es la colección organizada de todos los LSAs válidos que un router OSPF ha recibido y almacenado para un área determinada. Corresponde a la "base de datos topológica" o el "mapa completo de la red" descrito en la sección 2.2.1.

La LSDB se construye a partir de la recepción y validación de los LSAs (Tipo 1, Tipo 2, etc.) inundados dentro del área. Cada router dentro de la misma área OSPF se esfuerza por mantener una LSDB idéntica a la de sus vecinos en esa área, asegurando una visión consistente de la topología. Es precisamente sobre esta base de datos compilada que cada router ejecutará el algoritmo SPF para calcular las rutas más cortas. La LSDB es, por tanto, la representación interna, detallada y sincronizada que tiene el router sobre la topología de su área OSPF.

#### 2.2.4. Cálculo de Rutas: Algoritmo SPF y Teoría de Grafos

El mecanismo de OSPF para determinar las mejores rutas se basa en el algoritmo **Shortest Path First (SPF)**, una implementación del clásico **algoritmo de Dijkstra**, y está intrínsecamente ligado a la teoría de grafos.

OSPF clasifica las interfaces y redes en diferentes tipos (como Broadcast, Point-to-Point, Non-Broadcast Multi-Access - NBMA, Point-to-Multipoint). Esta clasificación influye en cómo los routers descubren vecinos (usando paquetes Hello) y cómo se disemina la información de estado de enlace (LSAs). Por ejemplo, en redes broadcast (como Ethernet), como se detallará más adelante (sección 2.2.7), se eligen un Router Designado (DR) y un Router Designado de Respaldo (BDR) para optimizar el intercambio de LSAs (específicamente, el DR genera el LSA Tipo 2) y reducir el tráfico del protocolo.

Debido a que OSPF se apoya en mecanismos de *path-finding* estrechamente ligados a estructuras de tipo grafo, la relación con la **teoría de grafos** resulta más que evidente. La topología de red dentro de un área OSPF se modela como un **grafo dirigido y ponderado**:

*   **Vértices (Nodos):** Representan los routers OSPF y, en algunos casos (como los LSAs Tipo 2), los segmentos de red multiacceso.
*   **Aristas (Enlaces):** Representan las conexiones (interfaces) entre los routers o entre un router y un segmento de red. Cada conexión bidireccional se representa típicamente como dos aristas dirigidas con su respectivo costo.
*   **Pesos:** Cada arista tiene asociado un peso numérico, que es el **costo OSPF** de esa interfaz o conexión. Este costo, como se verá en la sección 2.2.5, es fundamental para la selección de rutas.

Cada router construye este grafo de forma independiente basándose en la información contenida en su **LSDB**. La LSDB es, esencialmente, una representación distribuida y sincronizada del grafo de la red del área.

Una vez que el router ha construido el grafo a partir de su LSDB, ejecuta el **algoritmo SPF (Dijkstra)** sobre esta estructura. Considerándose a sí mismo como la **raíz del árbol**, el algoritmo calcula las rutas de **menor costo acumulado** hacia todos los demás nodos (routers y redes representadas en el grafo) dentro del área. El resultado es un **árbol de caminos más cortos (*shortest-path tree*)** desde la perspectiva de ese router. Las rutas obtenidas de este árbol son las que finalmente se utilizan para poblar la tabla de enrutamiento del router (Routing Information Base - RIB). La ejecución de este algoritmo por parte de cada router sobre una LSDB idéntica garantiza rutas óptimas (según la métrica de costo) y coherentes en toda el área.

#### 2.2.5. Métrica de Costo en OSPF

OSPF no utiliza el número de saltos como métrica principal (como RIP). En su lugar, utiliza un concepto de **costo**. Cada interfaz habilitada para OSPF tiene un valor de costo asociado. El costo total de una ruta es la **suma de los costos** de todas las interfaces de *salida* a lo largo del camino desde el origen hasta el destino. OSPF siempre preferirá la ruta con el **menor costo acumulado**.

*   **Cálculo por Defecto**: Por defecto, el costo se calcula inversamente proporcional al **ancho de banda** de la interfaz (Costo = Ancho de Banda de Referencia / Ancho de Banda de la Interfaz). El ancho de banda de referencia es configurable (comúnmente 100 Mbps o 1 Gbps por defecto, dependiendo del fabricante y versión). Esto significa que enlaces más rápidos tienen costos más bajos y son preferidos.
*   **Ajuste Manual**: El costo puede ser configurado manually por el administrador en cada interfaz. Esto es crucial para influir en la selección de rutas según políticas específicas, más allá del simple ancho de banda (ej., preferir un enlace de fibra óptica sobre uno satelital, aunque ambos tengan gran ancho de banda, debido a la latencia, o preferir un enlace primario sobre uno de respaldo).

#### 2.2.6. Jerarquía y Escalabilidad en OSPF: El Concepto de Área

Para mejorar la escalabilidad y reducir la sobrecarga en redes OSPF de gran tamaño, el protocolo introduce un concepto de diseño jerárquico basado en **áreas**. Dividir la red OSPF en múltiples áreas interconectadas ofrece beneficios significativos:

*   Reduce el tamaño de la base de datos topológica (LSDB), ya que cada router solo necesita mantener los detalles completos de su propia área.
*   Disminuye la carga computacional del algoritmo SPF, dado que este se ejecuta de forma independiente dentro de cada área.
*   Contiene la distribución ("inundación") de la mayoría de los anuncios de estado de enlace (LSAs) dentro de los límites del área donde se originan, optimizando el uso del ancho de banda y los recursos del router.

Esta estructura jerárquica se articula en torno a un componente central: el **Área Backbone (designada siempre como Área 0)**. Esta área actúa como el núcleo de tránsito principal de la red OSPF; toda la comunicación entre áreas diferentes debe, directa o indirectamente, pasar a través del Área 0. Es el pilar que une toda la estructura OSPF.

Los routers que conectan el Área 0 con otras áreas, o que conectan múltiples áreas entre sí, desempeñan un papel crucial y se denominan **Routers de Borde de Área (ABR - Area Border Routers)**. Estos ABRs son responsables no solo de participar en el enrutamiento de sus áreas conectadas, sino también de **resumir la información topológica** de un área y anunciarla a las otras. Este resumen se realiza mediante anuncios específicos (principalmente LSAs de Tipo 3), permitiendo que los routers conozcan las redes en otras áreas sin necesidad de tener todos los detalles topológicos de ellas.

Las áreas que se conectan al backbone y que no tienen restricciones especiales se consideran **Áreas Estándar** (o normales). Estas áreas mantienen una LSDB completa de su topología interna y también reciben información resumida sobre otras áreas (LSAs Tipo 3) y sobre rutas externas (LSAs Tipo 5, si existen en el dominio OSPF) a través de sus ABRs. Representan el tipo de área OSPF por defecto.

Sin embargo, para optimizar aún más y simplificar la operación en ciertas partes de la red, especialmente en aquellas que se encuentran en la periferia, OSPF define **tipos de Áreas Especiales**. La idea fundamental detrás de estas áreas (como las *Stub Areas*, *Totally Stubby Areas*, o *Not-So-Stubby Areas - NSSA*) es **reducir la cantidad de información de enrutamiento (LSAs)** que necesitan procesar y almacenar. Logran esto filtrando ciertos tipos de LSAs (típicamente los LSAs Tipo 5 que anuncian rutas externas, o incluso los LSAs Tipo 3 en variantes "Totally Stubby") y, a menudo, utilizando una ruta por defecto inyectada por el ABR para alcanzar destinos fuera del área. La elección del tipo de área especial adecuado depende de los requisitos de conectividad específicos de esa sección de la red.

#### 2.2.7. Optimización en Redes Multiacceso: El Rol del DR y BDR

Como se mencionó brevemente en la sección 2.2.4, OSPF implementa optimizaciones para redes donde múltiples routers comparten el mismo medio, conocidas como **redes multiacceso** (ej., Ethernet). En estos entornos, si cada router formara una adyacencia completa con todos los demás, el número de adyacencias (`n*(n-1)/2` para `n` routers) y el tráfico OSPF asociado crecerían cuadráticamente, volviéndose ineficientes.

Para evitar esto, OSPF elige un **Router Designado (DR)** y un **Router Designado de Respaldo (BDR)** en cada segmento multiacceso:

*   **DR (Router Designado):** Actúa como coordinador central. Los demás routers (DROthers) solo forman adyacencia completa con él y con el BDR. Recibe los LSAs de los DROthers y es el responsable de distribuirlos al resto del segmento. Genera el LSA Tipo 2 (Network LSA) para representar al segmento.
*   **BDR (Router Designado de Respaldo):** Es un respaldo activo. Mantiene adyacencias completas y una LSDB sincronizada. Si el DR falla, el BDR asume su rol inmediatamente, asegurando resiliencia y rápida convergencia.

Este mecanismo DR/BDR reduce drásticamente el número de adyacencias y el tráfico OSPF en redes multiacceso, siendo crucial para la escalabilidad del protocolo en topologías LAN comunes.

### 2.3. Objetivos del Trabajo Práctico

Este trabajo práctico tiene como finalidad la aplicación concreta de los conceptos teóricos de OSPF en un entorno controlado. Los objetivos específicos son:

1.  Implementar y gestionar tablas de enrutamiento, incluyendo rutas estáticas y de host.
2.  Aplicar el protocolo de enrutamiento dinámico OSPF de manera criteriosa, comprendiendo sus mecanismos y parámetros fundamentales desde una perspectiva de ingeniería.
3.  Desarrollar habilidades prácticas mediante la implementación y verificación de casos de uso de OSPF en un entorno de red virtualizado.
4.  Analizar el comportamiento del protocolo, incluyendo la estructura de mensajes, la formación de adyacencias, el cálculo de rutas, el impacto de la configuración de áreas y costos, y la resiliencia ante fallos.

### 2.4. Metodología y Entorno de Simulación

Para alcanzar los objetivos propuestos, se empleará un software de simulación o virtualización de redes. La elección recae en Cisco Packet Tracer. Esta herramienta permite simular la topología de red especificada en la consigna, que consta de múltiples routers con conexiones redundantes, varios hosts y switches, proporcionando un entorno realista para la configuración, prueba y análisis del protocolo OSPF. Se configurarán las direcciones IP según un esquema predefinido y se implementará OSPF siguiendo los pasos detallados en la sección de desarrollo, verificando cada etapa mediante comandos de diagnóstico y pruebas de conectividad.

## 3. Desarrollo: Implementación y Análisis de OSPF

### 3.1. Diseño del Esquema de Direccionamiento IP

Para la configuración inicial de la red, se estableció un plan de direccionamiento IP lógico y escalable. Este plan se basa en el uso de direcciones IP privadas (RFC 1918) y distingue entre las necesidades de direccionamiento de las redes de usuarios finales y las conexiones de infraestructura entre routers.

#### 3.1.1. Fundamentos de la Elección de Rangos Base

La selección de los bloques de direcciones IP iniciales se realizó considerando las características generales de los rangos privados disponibles y la naturaleza de los segmentos a direccionar:

*   **Uso de Rangos Privados (RFC 1918):** Se decidió utilizar exclusivamente direcciones IP de los rangos privados para evitar conflictos con el espacio de direccionamiento público de Internet y seguir las convenciones estándar. Los rangos privados disponibles son:
    *   `10.0.0.0` a `10.255.255.255` (Asociado a Clase A)
    *   `172.16.0.0` a `172.31.255.255` (Asociado a Clase B)
    *   `192.168.0.0` a `192.168.255.255` (Asociado a Clase C)

*   **Rango Base para Redes de Hosts:** Se eligió el bloque `172.16.0.0` como punto de partida para las redes que conectan a los dispositivos finales (hosts h1-h5). Este rango, perteneciente al espacio privado asociado a la Clase B, ofrece un número considerable de direcciones, proporcionando flexibilidad para futuras expansiones o segmentaciones adicionales si fuesen necesarias.

*   **Rango Base para Enlaces Inter-Router:** Para las conexiones directas entre los routers (R1-R2, R2-R3, etc.), se seleccionó el bloque `192.168.0.0`. Este rango, asociado al espacio privado de Clase C, es comúnmente utilizado para redes de menor tamaño o segmentos de infraestructura.

*   **Dirección para Interfaz Loopback (R1):** Se decidió asignar la dirección `1.1.1.1` a la interfaz loopback de R1. Aunque pertenece a un rango público, su uso es frecuente en entornos controlados de laboratorio para proporcionar un identificador único y estable al router, útil para protocolos de enrutamiento y gestión.

#### 3.1.2. Estrategia de Subred Aplicada

Una vez seleccionados los rangos base, se aplicó una estrategia de desiganción de subredes para dividir estos bloques en redes más pequeñas y adecuadas para cada segmento específico de la topología:

*   **Subredes para Redes de Hosts:** A partir del rango base `172.16.0.0`, se optó por aplicar una máscara de subred `255.255.255.0` (`/24`). Esta decisión se basa en la necesidad de crear segmentos de red (dominios de broadcast) separados para cada grupo de hosts (h1-h3, h4, h5). La máscara `/24` divide el rango `172.16.x.x` en múltiples subredes, cada una con capacidad para 254 hosts. Este tamaño es considerado estándar y práctico para redes de área local (LAN), permitiendo una gestión clara y conteniendo el tráfico de broadcast. Las subredes específicas asignadas son:
    *   `172.16.1.0/24` (para h1, h2, h3)
    *   `172.16.2.0/24` (para h4)
    *   `172.16.3.0/24` (para h5)

*   **Subredes para Enlaces Inter-Router:** Para los enlaces punto a punto que conectan directamente pares de routers, se aplicó una máscara `255.255.255.252` (`/30`) sobre el rango base `192.168.0.0`. Esta máscara es la más eficiente para este tipo de conexión, ya que crea subredes que contienen solo 4 direcciones IP en total: la dirección de red, la dirección de broadcast y dos direcciones utilizables, exactamente una para cada interfaz del router en el enlace. Esto evita el desperdicio de direcciones IP que ocurriría si se usara una máscara más grande (como /24) en un enlace que solo necesita dos direcciones. Las subredes `/30` asignadas son:
    *   `192.168.1.0/30` (R1-R2)
    *   `192.168.2.0/30` (R2-R3)
    *   `192.168.3.0/30` (R3-R4)
    *   `192.168.4.0/30` (R3-R5)
    *   `192.168.5.0/30` (R4-R5)

*   **Máscara para Interfaz Loopback:** A la dirección `1.1.1.1` de la interfaz loopback de R1 se le asignó la máscara `255.255.255.255` (`/32`). Esta máscara indica que la dirección representa a un único host (el propio router en este caso) y no a una red.

#### 3.1.3. Tabla de Direccionamiento IP

La siguiente tabla resume la asignación específica de direcciones IP a cada interfaz y host, de acuerdo con el esquema de direccionamiento y la estrategia de subneteo definidos previamente.

| Dispositivo | Interfaz             | Dirección IP      | Máscara de Subred | Gateway por Defecto | Red              |
| :---------- | :------------------- | :---------------- | :---------------- | :------------------ | :--------------- |
| **Hosts**   |                      |                   |                   |                     |                  |
| h1          | FastEthernet0        | 172.16.1.10       | 255.255.255.0     | 172.16.1.1          | 172.16.1.0/24    |
| h2          | FastEthernet0        | 172.16.1.11       | 255.255.255.0     | 172.16.1.1          | 172.16.1.0/24    |
| h3          | FastEthernet0        | 172.16.1.12       | 255.255.255.0     | 172.16.1.1          | 172.16.1.0/24    |
| h4          | FastEthernet0        | 172.16.2.10       | 255.255.255.0     | 172.16.2.1          | 172.16.2.0/24    |
| h5          | FastEthernet0        | 172.16.3.10       | 255.255.255.0     | 172.16.3.1          | 172.16.3.0/24    |
| **Routers** |                      |                   |                   |                     |                  |
| **R1**      | Loopback0            | 1.1.1.1           | 255.255.255.255   | N/A                 | 1.1.1.1/32       |
|             | `Gi0/0` *(a R2)*     | 192.168.1.1       | 255.255.255.252   | N/A                 | 192.168.1.0/30   |
|             | `Gi0/1` *(a R3)*     | 192.168.6.1       | 255.255.255.252   | N/A                 | 192.168.6.0/30   |
| **R2**      | `Gi0/0` *(a S1)*     | 172.16.1.1        | 255.255.255.0     | N/A                 | 172.16.1.0/24    |
|             | `Gi0/1` *(a R1)*     | 192.168.1.2       | 255.255.255.252   | N/A                 | 192.168.1.0/30   |
|             | `Gi0/2` *(a R3)*     | 192.168.2.1       | 255.255.255.252   | N/A                 | 192.168.2.0/30   |
| **R3**      | `Gi0/0` *(a R2)*     | 192.168.2.2       | 255.255.255.252   | N/A                 | 192.168.2.0/30   |
|             | `Gi0/1` *(a R1)*     | 192.168.6.2       | 255.255.255.252   | N/A                 | 192.168.6.0/30   |
|             | `Gi0/2` *(a R4)*     | 192.168.3.1       | 255.255.255.252   | N/A                 | 192.168.3.0/30   |
|             | `Gi0/3/0` *(a R5)*   | 192.168.4.1       | 255.255.255.252   | N/A                 | 192.168.4.0/30   |
| **R4**      | `Gi0/0` *(a R3)*     | 192.168.3.2       | 255.255.255.252   | N/A                 | 192.168.3.0/30   |
|             | `Gi0/1` *(a h4)*     | 172.16.2.1        | 255.255.255.0     | N/A                 | 172.16.2.0/24    |
|             | `Gi0/2` *(a R5)*     | 192.168.5.1       | 255.255.255.252   | N/A                 | 192.168.5.0/30   |
| **R5**      | `Gi0/0` *(a h5)*     | 172.16.3.1        | 255.255.255.0     | N/A                 | 172.16.3.0/24    |
|             | `Gi0/2` *(a R4)*     | 192.168.5.2       | 255.255.255.252   | N/A                 | 192.168.5.0/30   |
|             | `Gi0/3/0` *(a R3)*   | 192.168.4.2       | 255.255.255.252   | N/A                 | 192.168.4.0/30   |

<center>
Tabla 3.1. Tabla de Direccionamiento IP
</center>


### 3.2. Implementación de la Topología y Configuraciones Iniciales
Una vez diseñado el esquema de direccionamiento IP, el siguiente paso consiste en implementar la topología de red en el entorno de simulación y configurar las direcciones IP en cada dispositivo. Posteriormente, se realiza una verificación fundamental de la conectividad de Capa 3 para asegurar que la infraestructura base está operativa antes de introducir protocolos de enrutamiento dinámico.

#### 3.2.1. Implementación de la Topología en Packet Tracer
La topología de red descrita en los requisitos se implementó utilizando el software Cisco Packet Tracer (Figura 3.1). Se dispusieron los siguientes dispositivos en el espacio de trabajo lógico:
*   Cinco routers (nombrados R1, R2, R3, R4, R5), todos de modelo 2911.
*   Un switch (nombrado S1), modelo 2960-24TT.
*   Cinco hosts (nombrados h1, h2, h3, h4, h5).

Se utilizaron las herramientas de conexión de Packet Tracer (seleccionando el tipo de cable apropiado, típicamente Cobre Directo, excepto para el Router que debió usar cuatro interfaces, que se verá en la sección de Observaciones)
*   h1, h2, h3 conectados a S1.
*   S1 conectado a una interfaz de R2.
*   R2 conectado a R1 y R3.
*   R1 conectado a R3 (completando el triángulo R1-R2-R3).
*   R3 conectado a R4 y R5.
*   R4 conectado a R5 (completando el triángulo R3-R4-R5).
*   h4 conectado directamente a R4.
*   h5 conectado directamente a R5.

<center>

![Topología de red](img/net_topology.png)\
Figura 3.1. Topología de Red

</center>

#### 3.2.2. Configuración de IPs Iniciales
Mediante el uso de la pestaña de IP Configuration dentro de las opciones de cada host, se configuró tanto la IP como la máscara de subred y el Default Gateway de cada uno, como se muestra en la Figura 3.2.

<center>

![IP Config de h3](img/h3_ip_config.png)\
Figura 3.2. Configuración para el Host 3

</center>

Luego, y a través de la CLI de cada Router, se procedió con la configuración de las interfaces. El código empleado para el Router 1 se encuentra a continuación. Se aplicaron comandos similares para el resto de dispositivos, con evidentes cambios para configurar exactamente las IPs presentadas en la sección anterior.

```
Router>en
Router#conf t
Router(config)#interface Loopback0
Router(config-if)#ip address 1.1.1.1 255.255.255.255
Router(config-if)#no shutdown
Router(config-if)#exit
Router(config)#interface GigabitEthernet0/0
Router(config-if)#description Enlace a R2
Router(config-if)#ip address 192.168.1.1 255.255.255.252
Router(config-if)#no shutdown
Router(config-if)#exit
Router(config)#interface GigabitEthernet0/1
Router(config-if)#description Enlace a R3
Router(config-if)#ip address 192.168.6.1 255.255.255.252
Router(config-if)#exit
```

Una vez configurado, se verificó de manera teórica que las interfaces estén bien configuradas.

```
Router#show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0 192.168.1.1 YES manual up up
GigabitEthernet0/1 192.168.6.1 YES manual up up
GigabitEthernet0/2 unassigned YES unset administratively down down
Loopback0 1.1.1.1 YES manual up up
Vlan1 unassigned YES unset administratively down down

```

#### 3.2.3. Verificación de las Configuraciones
Por último, se llevó a cabo un régimen exhaustivo de verificación mediante el uso de comandos ping, con el objetivo de afirmar si efectivamente las redes fueron configuradas correctamente.
- **Ping entre Routers:** Se adjunta el resultado exitoso de realizar ping entre los Routers 3 y 4.
    ```
    
    Router>ping 192.168.3.2

    Type escape sequence to abort.
    Sending 5, 100-byte ICMP Echos to 192.168.3.2, timeout is 2 seconds:
    !!!!!
    Success rate is 100 percent (5/5), round-trip min/avg/max = 0/5/10 ms
    
    ```
- **Ping de host a Gateway**: Se adjunta el resultado exitoso de realizar ping entre el Host 1 y el Router 2.
    ```
    C:\>ping 172.16.1.1

    Pinging 172.16.1.1 with 32 bytes of data:

    Reply from 172.16.1.1: bytes=32 time<1ms TTL=255
    Reply from 172.16.1.1: bytes=32 time<1ms TTL=255
    Reply from 172.16.1.1: bytes=32 time<1ms TTL=255
    Reply from 172.16.1.1: bytes=32 time<1ms TTL=255

    Ping statistics for 172.16.1.1:
        Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
    Approximate round trip times in milli-seconds:
        Minimum = 0ms, Maximum = 0ms, Average = 0ms
    
    ```

### 3.3. Configuración de OSPF y Verificación Inicial

Con la configuración IP base y la conectividad directa verificada, el siguiente paso es habilitar el enrutamiento dinámico OSPF en todos los routers. Esto permitirá que los routers intercambien información sobre las redes conectadas y calculen las mejores rutas hacia destinos remotos dentro del dominio OSPF. Inicialmente, configuraremos todos los routers dentro de una única área OSPF (Área 0, el área backbone), como preparación para la posterior división en áreas requerida en consignas futuras.

#### 3.3.1. Habilitación del Proceso OSPF y Anuncio de Redes

En cada router, se debe iniciar el proceso OSPF y especificar qué redes conectadas directamente participarán en OSPF y serán anunciadas a los vecinos.

El comando principal para iniciar OSPF es `router ospf <process-id>`, donde `<process-id>` es un número localmente significativo (entre 1 y 65535) que identifica la instancia del proceso OSPF en ese router. Se utilizará el ID de proceso `1` en todos los routers por simplicidad.

Luego, se utiliza el comando `network <network-address> <wildcard-mask> area <area-id>` para habilitar OSPF en las interfaces cuyas direcciones IP coincidan con el rango especificado y anunciar la red especificada a otros routers OSPF en la misma área.

La `<wildcard-mask>` es la inversa de la máscara de subred y se usa para determinar qué bits de la dirección IP deben coincidir. Para el `<area-id>`, comenzaremos usando `0` para todos los routers.

**Configuración para R1:**
```
Router#conf t
Enter configuration commands, one per line. End with CNTL/Z.
Router(config)#router ospf 1
Router(config-router)#router-id 1.1.1.1  
Router(config-router)#network 1.1.1.1 0.0.0.0 area 0     
Router(config-router)#network 192.168.1.0 0.0.0.3 area 0  
Router(config-router)#network 192.168.6.0 0.0.0.3 area 0  
Router(config-router)#end
Router#
```

Se aplicaron configuraciones análogas en los routers `R2`, `R3`, `R4` y `R5`, asegurándose de incluir todas sus redes conectadas directamente (tanto las redes de host como los enlaces inter-router) dentro del area 0 del proceso ospf 1, utilizando router IDs correspondientes a su nombre (`R2` como `2.2.2.2`, etc.).

#### 3.3.2. Verificación de Vecindades y Proceso OSPF en R2

Una vez configurado OSPF, es crucial verificar que los routers establezcan relaciones de vecindad (estado `FULL`) y que el proceso OSPF general funcione correctamente. Se examinan específicamente las operaciones en R2.

**Verificación de Vecinos en R2:**

Se verifica la información de los vecinos R1 y R3 desde R2 utilizando el comando `show ip ospf neighbor`. La salida esperada se genera con el comando detallado en el *Snippet A* a continuación.

```
Router>show ip ospf neighbor


Neighbor ID     Pri   State           Dead Time   Address         Interface
1.1.1.1           1   FULL/DR         00:00:37    192.168.1.1     GigabitEthernet0/1
3.3.3.3           1   FULL/DR         00:00:30    192.168.2.2     GigabitEthernet0/2
```

El análisis de la salida confirma que R2 ha establecido exitosamente las adyacencias esperadas con R1 (`1.1.1.1`) y R3 (`3.3.3.3`), ambas en estado `FULL`, indicando LSDBs sincronizadas.

**Verificación del Proceso OSPF General en R2:**

Se consulta información general sobre las operaciones del protocolo en R2 utilizando el comando `show ip ospf`. La salida esperada se genera con el comando detallado en el snippet a continuación.

```
Router>show ip ospf
 Routing Process "ospf 1" with ID 2.2.2.2
 Supports only single TOS(TOS0) routes
 Supports opaque LSA
 SPF schedule delay 5 secs, Hold time between two SPFs 10 secs
 Minimum LSA interval 5 secs. Minimum LSA arrival 1 secs
 Number of external LSA 0. Checksum Sum 0x000000
 Number of opaque AS LSA 0. Checksum Sum 0x000000
 Number of DCbitless external and opaque AS LSA 0
 Number of DoNotAge external and opaque AS LSA 0
 Number of areas in this router is 1. 1 normal 0 stub 0 nssa
 External flood list length 0
    Area BACKBONE(0)
        Number of interfaces in this area is 3
        Area has no authentication
        SPF algorithm executed 17 times
        Area ranges are
        Number of LSA 11. Checksum Sum 0x070388
        Number of opaque link LSA 0. Checksum Sum 0x000000
        Number of DCbitless LSA 0
        Number of indication LSA 0
        Number of DoNotAge LSA 0
        Flood list length 0
```

La salida de este comando confirma varios puntos clave sobre el estado de OSPF en R2:
*   El **Router ID** del proceso OSPF 1 está correctamente establecido en `2.2.2.2`.
*   R2 participa actualmente en **una sola área**, identificada como **Área BACKBONE(0)**, que es una "normal area" (no stub ni NSSA).
*   Dentro del Área 0, R2 tiene **3 interfaces** participando activamente en OSPF, lo cual coincide con sus conexiones a S1, R1 y R3.
*   El **algoritmo SPF** se ha ejecutado 17 veces, indicando que el router ha calculado (y potencialmente recalculado) las rutas basadas en la información topológica recibida.
*   La base de datos para el Área 0 contiene **11 LSAs** (`Number of LSA 11`), lo cual es consistente con la cantidad de LSAs Tipo 1 (uno por cada router) y Tipo 2 (uno por cada segmento inter-router tratado como broadcast) esperada en esta topología y configuración inicial.

#### 3.3.3. Verificación de la Base de Datos de Estado de Enlace (LSDB)

Una vez que los routers establecen vecindades, intercambian información sobre la topología mediante LSAs (Link State Advertisements). Cada router almacena los LSAs recibidos para su área en la Base de Datos de Estado de Enlace (LSDB), que representa el "mapa" completo de la red desde la perspectiva de OSPF. Antes de calcular las rutas, es fundamental verificar que esta LSDB se haya construido correctamente y sea consistente entre los routers del área.

Se utiliza el comando `show ip ospf database` para inspeccionar el contenido de la LSDB.

**Verificación en R1:**
```
Router>show ip ospf database
            OSPF Router with ID (1.1.1.1) (Process ID 1)

                Router Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum Link count
1.1.1.1         1.1.1.1         272         0x80000008 0x005513 3
2.2.2.2         2.2.2.2         271         0x80000008 0x002a83 3
4.4.4.4         4.4.4.4         86          0x80000010 0x00cfb9 3
3.3.3.3         3.3.3.3         78          0x80000012 0x00f58e 4
5.5.5.5         5.5.5.5         78          0x8000000f 0x00e29b 3

                Net Link States (Area 0)
Link ID         ADV Router      Age         Seq#       Checksum
192.168.1.1     1.1.1.1         916         0x80000003 0x00af1f
192.168.6.2     3.3.3.3         272         0x80000005 0x00e106
192.168.2.2     3.3.3.3         271         0x80000005 0x0069ea
192.168.3.2     4.4.4.4         107         0x80000003 0x0051fa
192.168.5.2     5.5.5.5         86          0x80000003 0x00ad9f
192.168.4.2     5.5.5.5         78          0x80000003 0x0098a4
```


**Verificación en R3:**
```
Router>show ip ospf database
            OSPF Router with ID (3.3.3.3) (Process ID 1)

                Router Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum Link count
1.1.1.1         1.1.1.1         382         0x80000008 0x005513 3
2.2.2.2         2.2.2.2         381         0x80000008 0x002a83 3
4.4.4.4         4.4.4.4         197         0x80000010 0x00cfb9 3
3.3.3.3         3.3.3.3         188         0x80000012 0x00f58e 4
5.5.5.5         5.5.5.5         188         0x8000000f 0x00e29b 3

                Net Link States (Area 0)
Link ID         ADV Router      Age         Seq#       Checksum
192.168.1.1     1.1.1.1         1027        0x80000003 0x00af1f
192.168.6.2     3.3.3.3         382         0x80000005 0x00e106
192.168.2.2     3.3.3.3         381         0x80000005 0x0069ea
192.168.3.2     4.4.4.4         217         0x80000003 0x0051fa
192.168.5.2     5.5.5.5         197         0x80000003 0x00ad9f
192.168.4.2     5.5.5.5         188         0x80000003 0x0098a4
```

En la salida anterior, se pueden identificar los diferentes tipos de LSAs:
*   **Router Link States (Tipo 1):** Cada router en el Área 0 (R1 a R5) genera un LSA de este tipo, identificado por su propio Router ID (`Link ID` y `ADV Router`). Describe los enlaces directos de ese router. Se espera ver 5 LSAs Tipo 1.
*   **Net Link States (Tipo 2):** Son generados por el Router Designado (DR) en segmentos donde se realiza una elección DR/BDR. Esto se debe a que las interfaces Ethernet, por defecto, son tratadas por OSPF como tipo de red 'BROADCAST', lo que fuerza una elección de DR y la consiguiente generación de un LSA Tipo 2 por parte del DR en cada uno de esos enlaces punto a punto simulados. El `Link ID` en cada caso corresponde a la IP del DR en ese segmento específico.

La consistencia de la LSDB entre R1 y R3 (y los demás routers del área) confirma que la información topológica se ha distribuido correctamente, proporcionando la base necesaria para que el algoritmo SPF calcule las rutas óptimas.

#### 3.3.4. Verificación de Rutas OSPF en la Tabla de Enrutamiento
Debido a que el objetivo final, como se describió en la sección introductoria, es poblar la tabla de enrutamiento (RIB) con las mejores rutas, es crucial verificar que esto se cumpla. Esta verificación se puede realizar mediante el comando `show ip route`.

**Verficación para R5**

```
Router>show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

     1.0.0.0/32 is subnetted, 1 subnets
O       1.1.1.1/32 [110/3] via 192.168.4.1, 00:14:44, GigabitEthernet0/3/0
     172.16.0.0/16 is variably subnetted, 4 subnets, 2 masks
O       172.16.1.0/24 [110/3] via 192.168.4.1, 00:14:44, GigabitEthernet0/3/0
O       172.16.2.0/24 [110/2] via 192.168.5.1, 00:14:44, GigabitEthernet0/2
C       172.16.3.0/24 is directly connected, GigabitEthernet0/0
L       172.16.3.1/32 is directly connected, GigabitEthernet0/0
     192.168.1.0/30 is subnetted, 1 subnets
O       192.168.1.0/30 [110/3] via 192.168.4.1, 00:14:44, GigabitEthernet0/3/0
     192.168.2.0/30 is subnetted, 1 subnets
O       192.168.2.0/30 [110/2] via 192.168.4.1, 00:14:44, GigabitEthernet0/3/0
     192.168.3.0/30 is subnetted, 1 subnets
```

De esta forma, se verifica que para el Router 5 el protocolo permitió *"aprender"* lo siguiente acerca de cómo hallar a sus pares y otras redes remotas:

*   Para llegar a la dirección loopback de R1 (`1.1.1.1/32`), el costo es 3 (por la ruta `R5->R3->R1`, asumiendo un costo de 1 por cada enlace GigabitEthernet) y el siguiente salto es `192.168.4.1` (la interfaz de R3 conectada a R5).
*   Para llegar a la subred `172.16.1.0/24` (donde residen los hosts h1 a h3, conectados a R2), el costo también es 3 (siguiendo la ruta `R5->R3->R2`) y el siguiente salto es, nuevamente, hacia R3 (`192.168.4.1`).
*   Para alcanzar la subred `172.16.2.0/24` (la red del host h4, conectado a R4), el costo es menor, 2 (indicando una ruta más directa: `R5->R4`), y el siguiente salto es `192.168.5.1` (la interfaz de R4 conectada a R5).
*   Para llegar a la red del enlace entre R1 y R2 (`192.168.1.0/30`), el costo es 3 (por la ruta `R5->R3->R1` o `R5->R3->R2`) con el siguiente salto hacia R3 (`192.168.4.1`).
*   Finalmente, para alcanzar la red del enlace entre R2 y R3 (`192.168.2.0/30`), el costo es 2 (ruta `R5->R3`) y el siguiente salto es hacia R3 (`192.168.4.1`).

Así, se demuestra que OSPF ha convergido, permitiendo a R5 conocer las rutas óptimas (basadas en el costo acumulado) hacia todas las demás subredes dentro del dominio OSPF configurado.

#### 3.3.5. Verificación Específica en R2 (Consigna 7)

Complementando las verificaciones anteriores, se examina con más detalle el estado de OSPF específicamente en el Router R2, consultando el estado de sus vecinos directos (R1 y R3) y los parámetros generales del proceso OSPF en ejecución.

**Información de Vecinos OSPF en R2 (Consigna 7a):**

Se utiliza `show ip ospf neighbor` para confirmar el estado de las adyacencias que R2 ha formado.

**Salida del Comando en R2:**

[SNIPPET_NEIGHBOR_R2_AQUI]

*(Nota: Reemplazar el placeholder con la salida real del comando `show ip ospf neighbor` ejecutado en R2).*

El análisis de la salida confirma que R2 ha establecido exitosamente las adyacencias esperadas con R1 (`1.1.1.1`) y R3 (`3.3.3.3`), ambas en estado `FULL`, indicando LSDBs sincronizadas.

**Información General del Proceso OSPF en R2 (Consigna 7b):**

Se utiliza `show ip ospf` para obtener una visión general del proceso OSPF en R2.

**Salida del Comando en R2:**

[SNIPPET_OSPF_R2_AQUI]

*(Nota: Reemplazar el placeholder con la salida real del comando `show ip ospf` ejecutado en R2).*

La salida de este comando confirma el Router ID (`2.2.2.2`), las áreas activas (Área 0), las interfaces participantes y estadísticas sobre la ejecución del algoritmo SPF, proporcionando una visión completa del estado del proceso OSPF en R2 en esta configuración inicial de área única.

### 3.4. Ciclo de Mensajes OSPF: Análisis de la Re-convergencia

En su funcionamiento normal y estable, OSPF es bastante silencioso. Los routers que ya han alcanzado una adyacencia completa (estado `FULL`) simplemente se envían **Paquetes Hello** periódicos para confirmar que siguen activos, como se muestra en las Figuras 3.3 y 3.4, que ilustran un Hello típico en esta fase estable.

<center>

![Paquete Hello Vista General](img/OSPFHello1.png)\
Figura 3.3. Vista General de un Paquete OSPF Hello (Estado Estable)

</center>

<center>

![Paquete Hello PDU](img/OSPFHello2.png)\
Figura 3.4. PDU de un Paquete OSPF Hello (Estado Estable)

</center>

Para observar cómo OSPF maneja la dinámica de establecimiento y sincronización, provocamos una re-convergencia. Esto se hizo ejecutando `clear ip ospf process` específicamente en R5. Este comando borra el estado OSPF activo de R5 (vecinos, LSDB), forzándolo a empezar de nuevo con sus vecinos R3 y R4. Analizamos la secuencia de mensajes resultante en el modo **Simulación** de Packet Tracer, filtrando por **OSPF**.

La secuencia observada tras el reinicio de OSPF en R5 se desarrolló en las siguientes fases:

