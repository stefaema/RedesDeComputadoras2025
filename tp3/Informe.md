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