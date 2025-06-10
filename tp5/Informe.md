# Trabajo Práctico N° 5

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
*26/05/2025*

### Información de los Autores

**Fernando E. Stefanovic Carroza:** [*fernando.stefanovic@mi.unc.edu.ar*](mailto:fernando.stefanovic@mi.unc.edu.ar)  
**Sofia Viale:** [*sofia.viale@mi.unc.edu.ar*](mailto:sofia.viale@mi.unc.edu.ar)  
**Francisco J. Vásquez:** [*javier.vasquez@mi.unc.edu.ar*](mailto:javier.vasquez@mi.unc.edu.ar)  
**Tomas G. Daniel:** [*tomas.daniel@mi.unc.edu.ar*](mailto:tomas.daniel@mi.unc.edu.ar)  
**Sofía Aldana Ávalos:** [*aldana.avalos@mi.unc.edu.ar*](mailto:aldana.avalos@mi.unc.edu.ar)

## 1. Resumen

Este trabajo práctico se centró en la manipulación de librerías de networking en Python para la transmisión de datos utilizando los protocolos TCP y UDP, y el análisis de sus características a través de la captura de tráfico con Wireshark. Se desarrollaron scripts cliente-servidor para enviar secuencias de paquetes, registrar eventos con timestamps y calcular métricas de rendimiento como latencia, jitter y pérdida de paquetes. Adicionalmente, se implementó la encriptación simétrica de la carga útil utilizando la librería `cryptography` con Fernet, demostrando la protección de los datos en tránsito. Finalmente, se exploraron conceptualmente las diferencias entre encriptación simétrica y asimétrica, y cómo se abordaría un intercambio seguro de claves en un escenario sin conocimiento previo entre las partes.

## 2. Introducción

La comunicación en redes de computadoras se sustenta en una variedad de protocolos, cada uno con sus propias características y casos de uso. Entre los más fundamentales a nivel de transporte se encuentran el Protocolo de Control de Transmisión (TCP) y el Protocolo de Datagramas de Usuario (UDP). Comprender sus diferencias operativas, ventajas y desventajas es crucial para el diseño y análisis de aplicaciones en red. Asimismo, la seguridad de la información transmitida es una preocupación primordial, donde las técnicas de encriptación juegan un rol vital.

El presente trabajo práctico tiene como objetivo principal proporcionar una experiencia práctica en:
1.  El desarrollo de aplicaciones cliente-servidor capaces de enviar y recibir datos secuencialmente sobre TCP y UDP.
2.  La utilización de herramientas de análisis de red como Wireshark para inspeccionar el tráfico generado, identificar la estructura de los paquetes y verificar la correcta transmisión de la carga útil.
3.  La implementación de mecanismos de logging para registrar eventos de comunicación y la posterior utilización de estos datos para calcular métricas de rendimiento clave (latencia, jitter, pérdida de paquetes).
4.  La aplicación de técnicas de encriptación simétrica para asegurar la confidencialidad de la carga útil de los paquetes.
5.  La comprensión teórica de los fundamentos de la encriptación simétrica, asimétrica y los mecanismos para el establecimiento seguro de comunicaciones.

A través de la implementación y experimentación con estos conceptos, se busca consolidar el entendimiento de la capa de transporte y los principios básicos de seguridad en redes. Este informe detallará la metodología seguida, los scripts desarrollados, los resultados obtenidos en las pruebas de comunicación y encriptación, y las conclusiones derivadas del análisis.

## 3. Desarrollo

### 3.1 Envío de datos mediante TCP

Como primera instancia para abordar el envío de datos utilizando el Protocolo de Control de Transmisión (TCP), se desarrollaron dos scripts principales en Python: `tcp_server.py` destinado a actuar como el receptor de las conexiones y los datos, y `tcp_client.py` diseñado para iniciar la conexión y transmitir la información.

La configuración del entorno de prueba consistió en ejecutar el script `tcp_server.py` en una máquina con sistema operativo Windows. Esta misma máquina se utilizó para la captura y análisis del tráfico de red mediante la herramienta Wireshark. Por otro lado, el script `tcp_client.py` se ejecutó en una segunda máquina con sistema operativo Linux Mint. Ambas computadoras se encontraban conectadas a la misma red local para facilitar la comunicación directa. La configuración específica de red, como las direcciones IP y los puertos utilizados, se gestionó a través de los archivos `config_server.py` y `config_client.py` respectivamente, asegurando que el cliente apuntara correctamente a la dirección IP del servidor y al puerto TCP designado (`12345`).

#### 3.1.1 Funcionalidad y Estructura de los Scripts TCP

El script `tcp_server.py` se programó para realizar las siguientes acciones:
1.  Crear un socket TCP.
2.  Vincular el socket a una dirección IP y un puerto TCP específico.
3.  Poner el socket en modo escucha para aceptar conexiones entrantes.
4.  Al recibir una conexión, establecer un canal de comunicación con el cliente.
5.  Entrar en un bucle para recibir datos del cliente, decodificarlos, registrar la recepción en un archivo de log y enviar un mensaje de acuse de recibo (ACK) al cliente.

Por su parte, el script `tcp_client.py` fue diseñado para:
1.  Crear un socket TCP.
2.  Conectarse al servidor utilizando la dirección IP y el puerto especificados en su archivo de configuración.
3.  Una vez conectado, enviar una secuencia de `N` paquetes al servidor a intervalos regulares.
4.  Cada paquete contiene un identificador único y una carga útil de texto.
5.  Después de enviar cada paquete, el cliente espera recibir un ACK del servidor.
6.  Registrar tanto el envío de paquetes como la recepción de ACKs, junto con timestamps, en un archivo de log.
7.  Calcular y mostrar métricas de rendimiento (latencia y jitter) al finalizar la transmisión.


#### 3.1.2 Pruebas, Captura de Tráfico e Identificación de Carga Útil (Punto 1a)

Para verificar el correcto funcionamiento, se ejecutaron los scripts como se describió anteriormente. Se utilizó Wireshark en la máquina servidor para capturar el tráfico TCP, aplicando un filtro de visualización `tcp port 12345` para aislar la comunicación relevante.

Se observó el establecimiento de la conexión TCP mediante el handshake de tres vías (SYN, SYN-ACK, ACK). Posteriormente, se visualizaron los paquetes de datos transmitidos desde el cliente (Linux, IP: `192.168.100.36`) hacia el servidor (Windows, IP: `192.168.100.2`), seguidos de los paquetes ACK en dirección opuesta.

Para identificar la carga útil, se seleccionó un paquete de datos representativo enviado por el cliente. La siguiente captura de pantalla muestra la lista de paquetes en Wireshark y el paquete seleccionado:
<center>

![Lista de Paquetes TCP](<img/Paquetes TCP.png>)


*Figura 3.1. Inspección de paquetes mediante Wireshark.*

</center>

Al inspeccionar los detalles del paquete seleccionado, se expandió la sección de datos TCP. Como se evidencia en la Figura, la carga útil es visible en formato de texto plano, correspondiendo al mensaje esperado.

<center>

![Payload TCP Legible](<img/Data TCP.png>)

*Figura 3.2. Inspección de paquete específico mediante Wireshark.*

</center>

Específicamente, mapeando la codificación hexadecimal hacia un mensaje legible, se tiene según la tabla 3.1:

| Hex | 4e | 6f | 4c | 6f | 53 | 6f | 6e | 49 | 45 | 45 | 2d | 31 | 38 | 3a | 45 | 73 | 74 | 65 | 20 | 65 | 73 | 20 | 65 | 6c | 20 | 70 | 61 | 79 | 6c | 6f | 61 | 64 | 20 | 64 | 65 | 6c | 20 | 70 | 61 | 71 | 75 | 65 | 74 | 65 | 20 | 54 | 43 | 50 | 20 | 31 | 38 |
|:---:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Char| N  | o  | L  | o  | S  | o  | n  | I  | E  | E  | -  | 1  | 8  | :  | E  | s  | t  | e  |    | e  | s  |    | e  | l  |    | p  | a  | y  | l  | o  | a  | d  |    | d  | e  | l  |    | p  | a  | q  | u  | e  | t  | e  |    | T  | C  | P  |    | 1  | 8  |

<center>
*Tabla 3.1. Mapeo de caracteres de la carga útil de un paquete TCP.*
</center>

Esto confirma que los paquetes transitaron correctamente y que la carga útil fue identificada según lo requerido.

#### 3.1.3 Registro de Paquetes con Timestamp (Punto 1b)

Ambos scripts implementaron una función `log_message` para registrar los eventos de envío y recepción en archivos de texto. El `tcp_client_log.txt` almacenó cada paquete enviado y cada ACK recibido, incluyendo el timestamp exacto y la latencia calculada para cada par paquete/ACK. El `tcp_server_log.txt` registró cada paquete recibido con su respectivo timestamp y contenido.

A continuación, se muestra un extracto del archivo `tcp_client_log.txt`:

```
Timestamp,Direction,MessageID,Data,Latency(s)
1748567731.845952,SENT,NoLoSonIEEE-1,Este es el payload del paquete TCP 1,
1748567731.847887,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-1,,0.001935
1748567732.848438,SENT,NoLoSonIEEE-2,Este es el payload del paquete TCP 2,
1748567732.870101,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-2,,0.021663
1748567733.871089,SENT,NoLoSonIEEE-3,Este es el payload del paquete TCP 3,
1748567733.893876,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-3,,0.022787
1748567734.894459,SENT,NoLoSonIEEE-4,Este es el payload del paquete TCP 4,
1748567734.919055,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-4,,0.024596
1748567735.919981,SENT,NoLoSonIEEE-5,Este es el payload del paquete TCP 5,
1748567735.941965,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-5,,0.021983
1748567736.942663,SENT,NoLoSonIEEE-6,Este es el payload del paquete TCP 6,
1748567736.965894,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-6,,0.023231
1748567737.966908,SENT,NoLoSonIEEE-7,Este es el payload del paquete TCP 7,
1748567737.989587,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-7,,0.022679
1748567738.990126,SENT,NoLoSonIEEE-8,Este es el payload del paquete TCP 8,
1748567739.013825,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-8,,0.023699
1748567740.014421,SENT,NoLoSonIEEE-9,Este es el payload del paquete TCP 9,
1748567740.038053,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-9,,0.023632
1748567741.038563,SENT,NoLoSonIEEE-10,Este es el payload del paquete TCP 10,
1748567741.063805,ACK_RECEIVED,ACK_FOR_NoLoSonIEEE-10,,0.025242
```

Y un extracto del `tcp_server_log.txt`:

```
Timestamp,Direction,MessageID,Data
1748567731.240975,RECEIVED,NoLoSonIEEE-1,Este es el payload del paquete TCP 1
1748567732.262774,RECEIVED,NoLoSonIEEE-2,Este es el payload del paquete TCP 2
1748567733.287052,RECEIVED,NoLoSonIEEE-3,Este es el payload del paquete TCP 3
1748567734.311216,RECEIVED,NoLoSonIEEE-4,Este es el payload del paquete TCP 4
1748567735.335325,RECEIVED,NoLoSonIEEE-5,Este es el payload del paquete TCP 5
1748567736.359185,RECEIVED,NoLoSonIEEE-6,Este es el payload del paquete TCP 6
1748567737.383105,RECEIVED,NoLoSonIEEE-7,Este es el payload del paquete TCP 7
1748567738.406848,RECEIVED,NoLoSonIEEE-8,Este es el payload del paquete TCP 8
1748567739.431267,RECEIVED,NoLoSonIEEE-9,Este es el payload del paquete TCP 9
1748567740.455866,RECEIVED,NoLoSonIEEE-10,Este es el payload del paquete TCP 10
```

Estos logs permitieron una trazabilidad detallada de la comunicación. 

#### 3.1.4 Cálculo de Métricas de Conexión (Punto 1c)

Utilizando los timestamps registrados para el envío de cada paquete y la recepción de su correspondiente ACK, el script `tcp_client.py` calculó una serie de métricas clave para la secuencia de 100 paquetes enviados. Estas métricas ofrecen una visión cuantitativa del rendimiento de la comunicación TCP en el entorno de prueba configurado. A continuación, se detallan las métricas obtenidas, su significado, la fórmula matemática empleada para su cálculo y su correspondencia con el código Python implementado.

*   **Latencia Promedio (Average Latency):**
    Representa el Tiempo de Ida y Vuelta (RTT) promedio para los paquetes de la prueba. Es un indicador general de cuán rápido es el enlace de comunicación. Un valor más bajo indica una mejor respuesta de la red.
    *   **Fórmula Matemática:**
        $\text{Latencia Promedio} = \frac{\sum_{i=1}^{N} \text{Latencia}_i}{N}$
        Donde $Latencia_i$ es la latencia individual del paquete $i$ (tiempo de recepción del ACK - tiempo de envío del paquete), y $N$ es el número total de latencias registradas.
    *   **Paralelismo con el Código:** En el script `tcp_client.py`, dentro de la función `calculate_metrics`, esta métrica se calcula utilizando `statistics.mean(latencies)`, donde `latencies` es una lista que contiene todas las latencias individuales (`ack_receive_timestamp - send_timestamp`) recolectadas durante la prueba.

*   **Latencia Máxima (Maximum Latency):**
    Indica el valor más alto de RTT observado durante toda la prueba. Esta métrica es útil para entender el peor caso de retardo que un paquete experimentó, lo cual puede ser crítico para aplicaciones sensibles al tiempo.
    *   **Fórmula Matemática:**
        $\text{Latencia Máxima} = \max(\text{Latencia}_1, \text{Latencia}_2, \dots, \text{Latencia}_N)$
    *   **Paralelismo con el Código:** Se calcula mediante `max(latencies)` en la función `calculate_metrics`.

*   **Latencia Mínima (Minimum Latency):**
    Refleja el valor más bajo de RTT observado. Representa el mejor caso de retardo, a menudo limitado por la velocidad de propagación física y el overhead mínimo de procesamiento.
    *   **Fórmula Matemática:**
        $\text{Latencia Mínima} = \min(\text{Latencia}_1, \text{Latencia}_2, \dots, \text{Latencia}_N)$
    *   **Paralelismo con el Código:** Se obtiene con `min(latencies)` en la función `calculate_metrics`.

*   **Jitter Promedio (Average Jitter):**
    El jitter mide la variación en el retardo (latencia) de los paquetes sucesivos. Un jitter alto puede ser problemático para aplicaciones de streaming de audio/video o VoIP, ya que implica una llegada irregular de los paquetes.
    *   **Fórmula Matemática:**
        Primero, se calcula el jitter individual entre paquetes consecutivos `i` e `i-1`:
        $\text{Jitter}_i = |\text{Latencia}_i - \text{Latencia}_{i-1}|$
        Luego, el jitter promedio se calcula como la media de estos jitters individuales:
        $\text{Jitter Promedio} = \frac{\sum_{k=1}^{M} \text{Jitter}_k}{M}$
        Donde $M$ es el número de valores de jitter calculados (que sería $N-1$ si $N$ es el número de latencias).
    *   **Paralelismo con el Código:** En `calculate_metrics`, primero se genera una lista de jitters individuales: `jitters = [abs(latencies[i] - latencies[i-1]) for i in range(1, len(latencies))]`. Posteriormente, se calcula el promedio de esta lista con `statistics.mean(jitters)`.

Las métricas obtenidas para TCP fueron:
*   **Latencia Promedio:** `24.05 ms`
*   **Latencia Máxima:** `128.79 ms`
*   **Latencia Mínima:** `1.93 ms`
*   **Jitter Promedio:** `10.58 ms`

Estas métricas reflejan el comportamiento de la comunicación TCP en la red local bajo las condiciones de la prueba.

### 3.2 Envío de datos mediante UDP

Siguiendo una metodología similar a la empleada para TCP, se procedió a desarrollar y probar la comunicación utilizando el Protocolo de Datagramas de Usuario (UDP). Para ello, se crearon los scripts `udp_server.py` y `udp_client.py`, manteniendo el mismo entorno de prueba: el servidor UDP en la máquina Windows y el cliente UDP en la máquina Linux Mint. El puerto UDP designado para esta comunicación fue el `12346`, configurado en los respectivos archivos `config_server.py` y `config_client.py`.

#### 3.2.1 Funcionalidad y Estructura de los Scripts UDP

El protocolo UDP, al ser no orientado a conexión y no garantizar la entrega, presenta diferencias fundamentales con TCP que se reflejaron en el diseño de los scripts:

El script `udp_server.py` fue implementado para:
1.  Crear un socket UDP.
2.  Vincular el socket a la dirección IP del servidor y el puerto UDP especificado.
3.  Entrar en un bucle para recibir datagramas UDP. Esta función también proporciona la dirección IP y el puerto del remitente.
4.  Al recibir un datagrama, decodificar su contenido, registrar el evento en `logs/udp_server_log.txt` y enviar un ACK UDP al remitente utilizando la dirección obtenida.
5.  El servidor fue diseñado para terminar su ejecución tras recibir una señal de "finalización de métricas" por parte del cliente.

El script `udp_client.py` se desarrolló con las siguientes capacidades:
1.  Crear un socket UDP.
2.  Definir la dirección del servidor a la cual se enviarán los datagramas.
3.  Implementar un timeout en el socket para las operaciones de recepción, permitiendo así detectar la posible pérdida de ACKs.
4.  Enviar una secuencia de `N` datagramas al servidor, con identificador y carga útil similar a la prueba TCP.
5.  Después de enviar cada datagrama con `sendto()`, esperar un ACK del servidor utilizando `recvfrom()`.
6.  Registrar los envíos, ACKs recibidos o timeouts en `logs/udp_client_log.txt`.
7.  Calcular métricas de rendimiento basadas en los ACKs recibidos y estimar el porcentaje de pérdida de paquetes.
8.  Al finalizar el envío de paquetes de métricas, enviar un mensaje de control al servidor para indicar el fin de la prueba.

#### 3.2.2 Pruebas, Captura de Tráfico e Identificación de Carga Útil (Punto 2a)

Se ejecutaron los scripts UDP, y se utilizó Wireshark en la máquina servidor para capturar el tráfico, esta vez con el filtro de visualización `udp.port == 12346`. A diferencia de TCP, no se observa un handshake de establecimiento de conexión, ya que UDP es un protocolo sin conexión. Los paquetes de datos comenzaron a fluir directamente entre el cliente (Linux, IP: `192.168.100.36`) y el servidor (Windows, IP: `192.168.100.2`).

<center>

![Lista de Paquetes UDP](<img/Paquetes UDP.png>)

*Figura 3.3. Inspección Wireshark de paquetes.*

</center>

Al analizar los detalles del datagrama UDP seleccionado, se expandió la sección de datos. La carga útil, con el formato "NoLoSonIEEE-X:Este es el payload del paquete UDP X", fue visible en texto plano, como se muestra en la Figura 3.4.

<center>

![Payload UDP Legible](<img/Data UDP.png>)

*Figura 3.4. Inspección de un paquete UDP enviado.*

</center>



| Hex | 4e | 6f | 4c | 6f | 53 | 6f | 6e | 49 | 45 | 45 | 2d | 31 | 3a | 45 | 73 | 74 | 65 | 20 | 65 | 73 | 20 | 65 | 6c | 20 | 70 | 61 | 79 | 6c | 6f | 61 | 64 | 20 | 64 | 65 | 6c | 20 | 70 | 61 | 71 | 75 | 65 | 74 | 65 | 20 | 55 | 44 | 50 | 20 | 31 |
|:---:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Char| N  | o  | L  | o  | S  | o  | n  | I  | E  | E  | -  | 1  | :  | E  | s  | t  | e  |    | e  | s  |    | e  | l  |    | p  | a  | y  | l  | o  | a  | d  |    | d  | e  | l  |    | p  | a  | q  | u  | e  | t  | e  |    | U  | D  | P  |    | 1  |

<center>

*Tabla 3.2: Mapeo de Bytes Hexadecimales a Caracteres para Paquete UDP (Figura 3.4)*

</center>

Esto confirma la correcta transmisión e identificación del payload para UDP.

#### 3.2.3 Registro de Paquetes con Timestamp (Punto 2b)

De manera análoga a TCP, los scripts UDP registraron los eventos de comunicación. El archivo `udp_client_log.txt` documentó cada datagrama enviado, los ACKs recibidos (con su latencia) o los timeouts si el ACK no llegó. El `udp_server_log.txt` guardó cada datagrama recibido, su contenido y la dirección del cliente.

Extracto del `udp_client_log.txt`:

```
Timestamp,Direction,MessageID,Data,Latency(s)
1748568037.222008,SENT,NoLoSonIEEE-1,Este es el payload del paquete UDP 1,
1748568037.276524,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-1,,0.054516
1748568038.278185,SENT,NoLoSonIEEE-2,Este es el payload del paquete UDP 2,
1748568038.295967,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-2,,0.017782
1748568039.297701,SENT,NoLoSonIEEE-3,Este es el payload del paquete UDP 3,
1748568039.313160,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-3,,0.015459
1748568040.314893,SENT,NoLoSonIEEE-4,Este es el payload del paquete UDP 4,
1748568040.318333,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-4,,0.003439
1748568041.319689,SENT,NoLoSonIEEE-5,Este es el payload del paquete UDP 5,
1748568041.361693,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-5,,0.042004
1748568042.363651,SENT,NoLoSonIEEE-6,Este es el payload del paquete UDP 6,
1748568042.367851,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-6,,0.004200
1748568043.369331,SENT,NoLoSonIEEE-7,Este es el payload del paquete UDP 7,
1748568043.410073,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-7,,0.040742
1748568044.412118,SENT,NoLoSonIEEE-8,Este es el payload del paquete UDP 8,
1748568044.436735,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-8,,0.024618
1748568045.438972,SENT,NoLoSonIEEE-9,Este es el payload del paquete UDP 9,
1748568045.458177,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-9,,0.019204
1748568046.460001,SENT,NoLoSonIEEE-10,Este es el payload del paquete UDP 10,
1748568046.482211,ACK_RECEIVED,ACK_UDP_FOR_NoLoSonIEEE-10,,0.022210
```

Extracto del `udp_server_log.txt`:

```
Timestamp,Direction,MessageID,Data,ClientAddr
1748568036.607179,RECEIVED,NoLoSonIEEE-1,Este es el payload del paquete UDP 1,('192.168.100.36', 42360)
1748568037.629307,RECEIVED,NoLoSonIEEE-2,Este es el payload del paquete UDP 2,('192.168.100.36', 42360)
1748568038.647360,RECEIVED,NoLoSonIEEE-3,Este es el payload del paquete UDP 3,('192.168.100.36', 42360)
1748568039.651402,RECEIVED,NoLoSonIEEE-4,Este es el payload del paquete UDP 4,('192.168.100.36', 42360)
1748568040.695063,RECEIVED,NoLoSonIEEE-5,Este es el payload del paquete UDP 5,('192.168.100.36', 42360)
1748568041.701137,RECEIVED,NoLoSonIEEE-6,Este es el payload del paquete UDP 6,('192.168.100.36', 42360)
1748568042.743018,RECEIVED,NoLoSonIEEE-7,Este es el payload del paquete UDP 7,('192.168.100.36', 42360)
1748568043.767359,RECEIVED,NoLoSonIEEE-8,Este es el payload del paquete UDP 8,('192.168.100.36', 42360)
1748568044.791273,RECEIVED,NoLoSonIEEE-9,Este es el payload del paquete UDP 9,('192.168.100.36', 42360)
1748568045.814890,RECEIVED,NoLoSonIEEE-10,Este es el payload del paquete UDP 10,('192.168.100.36', 42360)
```

#### 3.2.4 Cálculo de Métricas de Conexión (Punto 2c)

Para la comunicación UDP, el script `udp_client.py` también calculó métricas de rendimiento. Es importante destacar que, dado que UDP es un protocolo no confiable y no incluye ACKs inherentes, las métricas de latencia y jitter se basan en los ACKs implementados a nivel de aplicación, es decir, el tiempo transcurrido entre el envío de un datagrama UDP y la recepción de su correspondiente ACK UDP enviado por el servidor. Además, se estima la pérdida de paquetes.

*   **Latencia Promedio (basada en ACKs recibidos):**
    Representa el tiempo promedio que tardó un datagrama UDP en llegar al servidor y su ACK (de aplicación) en retornar al cliente, considerando solo los paquetes para los cuales se recibió un ACK.
    *   **Fórmula Matemática:**
        $\text{Latencia Promedio} = \frac{\sum_{j=1}^{N_{ACK}} \text{Latencia}_j}{N_{ACK}}$
        Donde $Latencia_j$ es la latencia individual del datagrama $j$ cuyo ACK fue recibido, y $N_{ACK}$ es el número total de ACKs recibidos.
    *   **Paralelismo con el Código:** En el script `udp_client.py`, la función `calculate_metrics` opera sobre la lista `latencies`, que solo se puebla cuando se recibe un ACK (`latency = ack_receive_timestamp - send_timestamp`). El cálculo `statistics.mean(latencies)` entonces corresponde a esta fórmula.
*   **Latencia Máxima (basada en ACKs recibidos):**
    El valor más alto de RTT (basado en ACKs de aplicación) observado entre los datagramas que recibieron respuesta.
    *   **Fórmula Matemática:**
        $\text{Latencia Máxima} = \max(\text{Latencia}_1, \text{Latencia}_2, \dots, \text{Latencia}_{N_{ACK}})$
    *   **Paralelismo con el Código:** Calculado con `max(latencies)` en `calculate_metrics`.

*   **Latencia Mínima (basada en ACKs recibidos):**
    El valor más bajo de RTT (basado en ACKs de aplicación) observado.
    *   **Fórmula Matemática:**
        $\text{Latencia Mínima} = \min(\text{Latencia}_1, \text{Latencia}_2, \dots, \text{Latencia}_{N_{ACK}})$
    *   **Paralelismo con el Código:** Calculado con `min(latencies)` en `calculate_metrics`.
*   **Jitter Promedio (basado en ACKs recibidos):**
    La variación promedio en el retardo entre los ACKs de datagramas sucesivos que fueron recibidos.
    *   **Fórmula Matemática:**
        Similar a TCP, pero usando las latencias de los ACKs UDP recibidos:
        $\text{Jitter}_j = |\text{Latencia}_j - \text{Latencia}_{j-1}|$ (para ACKs consecutivos)
        $\text{Jitter Promedio} = \frac{\sum_{k=1}^{M_{ACK}} \text{Jitter}_k}{M_{ACK}}$
        Donde $M_{ACK}$ es el número de valores de jitter calculados a partir de los $N_{ACK}$ ACKs recibidos (sería $N_{ACK}-1$).
    *   **Paralelismo con el Código:** Similar a TCP, se calcula con `jitters = [abs(latencies[i] - latencies[i-1]) for i in range(1, len(latencies))]` y luego `statistics.mean(jitters)`, donde `latencies` solo contiene las latencias de los ACKs recibidos.

*   **Pérdida de Paquetes Estimada:**
    Dado que UDP no garantiza la entrega, es crucial estimar cuántos paquetes se perdieron. Esta estimación se basa en la diferencia entre los paquetes que el cliente intentó enviar (y registró como `sendto` exitoso) y los ACKs que recibió del servidor.
    *   **Fórmula Matemática:**
        $\text{Pérdida de Paquetes (\%)} = \left( \frac{\text{Paquetes Enviados Exitosamente} - \text{ACKs Recibidos}}{\text{Paquetes Enviados Exitosamente}} \right) \times 100$ (Si $\text{Paquetes Enviados Exitosamente}> 0$).
    *   **Paralelismo con el Código:** En `udp_client.py`, se calcula como:
      ```python
      packet_loss_percentage = 0.0
      if packets_sent_successfully > 0:
          packet_loss_percentage = ((packets_sent_successfully - acks_received) / packets_sent_successfully) * 100
      ```
      Donde `packets_sent_successfully` cuenta los `sendto()` que no fallaron y `acks_received` cuenta los ACKs obtenidos.

Las métricas obtenidas para UDP, basadas en 100 datagramas enviados y sus ACKs, fueron:
*   **Latencia Promedio (basada en ACKs recibidos):** `24.44 ms`
*   **Latencia Máxima:** `146.16 ms`
*   **Latencia Mínima:** `2.81 ms`
*   **Jitter Promedio:** `11.34 ms`
*   **Pérdida de Paquetes Estimada:** `0.00%` (en este entorno de prueba particular)

Estas métricas proporcionan una visión del rendimiento de UDP, destacando que, aunque en esta prueba no hubo pérdidas, la posibilidad inherente al protocolo debe considerarse.

### 3.3 Comparación entre TCP y UDP (Punto 3)

Tras analizar individualmente las comunicaciones TCP y UDP, se procedió a una comparación directa basada en las capturas de Wireshark y las métricas obtenidas.

#### 3.3.1 Diferencias en Encabezados de Paquete

Al observar los paquetes capturados en Wireshark, las diferencias estructurales entre los encabezados TCP y UDP son notables:

*   **Encabezado TCP:** El encabezado TCP es más complejo e incluye campos cruciales para la comunicación orientada a conexión y confiable, tales como:
    *   Puertos de Origen y Destino.
    *   Número de Secuencia: Para ordenar los segmentos.
    *   Número de Acuse de Recibo: Para confirmar la recepción de datos.
    *   Flags (SYN, ACK, FIN, RST, PSH, URG): Para controlar el estado de la conexión.
    *   Tamaño de Ventana: Para el control de flujo.
    *   Checksum: Para la detección de errores en el encabezado y los datos.
    *   Puntero Urgente y Opciones.

*   **Encabezado UDP:** El encabezado UDP es significativamente más simple, reflejando su naturaleza no orientada a conexión y de "mejor esfuerzo":
    *   Puerto de Origen y Destino.
    *   Longitud: Longitud total del datagrama.
    *   Checksum: Para la detección de errores.


#### 3.3.2 Tabla Comparativa de Métricas

La siguiente tabla resume las métricas de rendimiento obtenidas para TCP y UDP en las pruebas realizadas:

| Métrica                     | TCP  | UDP |
| :-------------------------- | :---------------------------- | :---------------------------- |
| Latencia Promedio           | `24.05 ms` | `24.44 ms` |
| Latencia Máxima             | `128.79 ms`      | `146.16 ms`      |
| Latencia Mínima             | `1.93 ms`      | `2.81 ms`      |
| Jitter Promedio             | `10.58 ms`       | `11.34 ms`       |

<center>

*Tabla 3.3. Tabla Comparativa de Rendimiento TCP vs UDP*
</center>

**Análisis de las Métricas:**

Al analizar los resultados obtenidos, se pueden extraer varias observaciones interesantes sobre el comportamiento de TCP y UDP en el entorno de prueba configurado:

1.  **Latencia Promedio:** Se observa que la latencia promedio para UDP (`24.44 ms`) fue ligeramente superior a la de TCP (`24.05 ms`). Aunque a menudo se espera que UDP tenga menor latencia debido a su menor overhead, en este caso la diferencia es mínima y podría estar influenciada por factores como la carga de la red local en el momento de la prueba o la forma en que se implementó el sistema de ACKs para UDP en nuestros scripts.

2.  **Latencias Máxima y Mínima:** TCP presentó tanto la latencia mínima más baja (`1.93 ms` vs `2.81 ms` de UDP) como una latencia máxima también ligeramente inferior (`128.79 ms` vs `146.16 ms` de UDP). Esto podría sugerir que, en esta prueba particular, la gestión de la conexión y el flujo de datos de TCP resultó en una variabilidad general un poco menor en los extremos, aunque las latencias máximas para ambos son considerablemente más altas que las promedio, indicando picos ocasionales de demora en la red.

3.  **Jitter Promedio:** El jitter promedio fue muy similar para ambos protocolos, con TCP registrando `10.58 ms` y UDP `11.34 ms`. Esto indica que la variación en el retardo entre paquetes sucesivos fue comparable en ambas pruebas.

4.  **Pérdida de Paquetes:** Un punto crucial de diferencia es la pérdida de paquetes. En las pruebas realizadas, TCP no presentó pérdida de paquetes, lo cual es consistente con sus mecanismos de control de errores y retransmisión diseñados para garantizar una entrega confiable. Para UDP, el log del cliente (`udp_client_log.txt`) indicó una pérdida de paquetes estimada del `0.00%`. Si bien en esta instancia no hubo pérdidas, es fundamental recordar que UDP no garantiza la entrega, y este resultado podría variar significativamente en redes menos estables o más congestionadas. La ausencia de pérdidas en este caso particular en una red local es plausible.

En conclusión, si bien las diferencias en latencia y jitter fueron mínimas en este entorno controlado y con la implementación de ACKs para UDP, la principal distinción teórica y práctica sigue siendo la confiabilidad. TCP ofrece entrega garantizada y ordenada, ideal para aplicaciones donde la integridad de los datos es primordial (transferencia de archivos, navegación web). UDP, con su menor overhead, sigue siendo preferido para aplicaciones donde la velocidad es crítica y se puede tolerar o manejar a nivel de aplicación cierta pérdida de datos (streaming, juegos en tiempo real, DNS). Las métricas obtenidas en este entorno local no muestran una ventaja clara de latencia para UDP, probablemente debido al mecanismo de ACK implementado para la medición.

### 3.4 Encriptación de la Comunicación (Punto 4)

Para abordar la seguridad de los datos transmitidos, se exploró e implementó la encriptación de la carga útil.

#### 3.4.1 Diferencias entre Encriptado Simétrico y Asimétrico (Punto 4a)

La encriptación es un pilar fundamental de la seguridad informática, utilizada para proteger la confidencialidad de la información tanto en almacenamiento como en tránsito. Existen dos categorías principales de algoritmos de encriptación basados en el tipo de claves que utilizan: simétrica y asimétrica.

**Encriptación Simétrica:**
También conocida como encriptación de clave secreta o de clave única, la encriptación simétrica utiliza la **misma clave** para realizar tanto el proceso de cifrado como el de descifrado. Ambas partes comunicantes deben poseer esta clave secreta y mantenerla protegida.

*   **Ventajas:**
    *   **Velocidad y Eficiencia:** Los algoritmos simétricos son generalmente mucho más rápidos y menos exigentes computacionalmente que los asimétricos. Esto los hace ideales para cifrar grandes volúmenes de datos, como archivos completos o flujos continuos de información.
*   **Desventajas:**
    *   **Distribución Segura de la Clave:** El principal desafío de la encriptación simétrica radica en cómo compartir la clave secreta de forma segura entre las partes comunicantes. Si la clave se transmite por un canal inseguro, puede ser interceptada, comprometiendo toda la comunicación cifrada con ella.
    *   **Gestión de Claves:** En sistemas con muchos usuarios, la cantidad de claves únicas necesarias puede volverse difícil de gestionar.
    *   **No Repudio:** Por sí misma, la encriptación simétrica no proporciona no repudio. Dado que ambas partes conocen la misma clave, no se puede probar criptográficamente cuál de ellas originó un mensaje específico si la clave es compartida entre solo dos entidades.
*   **Ejemplos Comunes:** AES (Advanced Encryption Standard), DES (Data Encryption Standard), 3DES (Triple DES), Blowfish, RC4, y la especificación Fernet (utilizada en este trabajo práctico, que internamente usa AES).

**Encriptación Asimétrica:**
También denominada encriptación de clave pública, la encriptación asimétrica utiliza un **par de claves matemáticamente relacionadas**: una **clave pública** y una **clave privada**.
*   La clave pública puede ser distribuida libremente sin comprometer la seguridad.
*   La clave privada debe ser mantenida en secreto por su propietario.
Los datos cifrados con la clave pública solo pueden ser descifrados con la clave privada correspondiente, y viceversa (aunque este último caso se usa más comúnmente para firmas digitales que para confidencialidad).

*   **Ventajas:**
    *   **Resolución del Problema de Distribución de Claves:** Elimina la necesidad de compartir una clave secreta por un canal previo. Cualquiera puede obtener la clave pública de un destinatario para enviarle un mensaje cifrado que solo él podrá leer.
    *   **Autenticación y Firmas Digitales:** Permite verificar la identidad del remitente. Si un mensaje se cifra con la clave privada de alguien, cualquiera con la clave pública correspondiente puede verificar que el mensaje provino de esa persona y no ha sido alterado.
    *   **No Repudio:** Las firmas digitales proporcionan no repudio, ya que solo el poseedor de la clave privada pudo haber creado la firma.
*   **Desventajas:**
    *   **Lentitud y Costo Computacional:** Los algoritmos asimétricos son significativamente más lentos y consumen más recursos computacionales que los simétricos. No son prácticos para cifrar grandes cantidades de datos directamente.
*   **Ejemplos Comunes:** RSA (Rivest-Shamir-Adleman), ECC (Elliptic Curve Cryptography), Diffie-Hellman (aunque es un protocolo de acuerdo de claves, no de encriptación directa de mensajes, se basa en principios asimétricos), ElGamal.

**Sistemas Híbridos:**
En la práctica, muchas aplicaciones de seguridad utilizan un **enfoque híbrido** que combina las fortalezas de ambos tipos de encriptación.
Típicamente, la encriptación asimétrica se utiliza durante la fase inicial de establecimiento de la comunicación para:
1.  Autenticar a las partes.
2.  Intercambiar de forma segura una **clave de sesión simétrica** generada aleatoriamente.
Una vez que ambas partes comparten esta clave de sesión simétrica, toda la comunicación de datos subsiguiente se cifra utilizando un algoritmo simétrico, aprovechando su velocidad y eficiencia. Esto proporciona una solución robusta que es tanto segura en el intercambio de claves como eficiente para la transmisión de datos.

#### 3.4.2 Librería de Encriptación Implementada: Fernet (Punto 4b)

Para la encriptación de la carga útil en los scripts TCP y UDP, se seleccionó `Fernet`, una especificación de encriptación simétrica de alto nivel disponible en la librería `cryptography` de Python.

**Características Principales de Fernet:**
*   **Simétrica:** Utiliza la misma clave para encriptar y desencriptar.
*   **Seguridad "Sellada":** Está diseñada para ser fácil de usar correctamente y difícil de usar incorrectamente, proporcionando un buen nivel de seguridad por defecto.
*   **Algoritmos Subyacentes:** Utiliza AES de 128 bits en modo CBC (Cipher Block Chaining) para la encriptación de los datos.
*   **Autenticación e Integridad:** Emplea HMAC (Hash-based Message Authentication Code) con SHA256 para asegurar que los datos no solo estén encriptados, sino que también no hayan sido alterados.
*   **Prevención de Replay (Parcial):** Incluye un timestamp en el mensaje cifrado, lo que ayuda a mitigar algunos ataques de replay.
*   **Generación de Claves:** Proporciona una función `Fernet.generate_key()` para crear claves seguras y aleatorias en el formato correcto.

La implementación consistió en:
1.  Generar una clave Fernet única utilizando el script `Codigos/code_gene.py`.
2.  Almacenar esta clave como bytes en los archivos `config_server.py` y `config_client.py`.
3.  En cada script, se añadió una variable booleana `ENCRYPT`. Si esta era `True`, se inicializaba un objeto `Fernet` con la clave compartida.
4.  Antes de enviar datos, la carga útil se codificaba a bytes y luego se encriptaba con `cipher_suite.encrypt()`.
5.  Al recibir datos, los bytes encriptados se desencriptaban con `cipher_suite.decrypt()` y luego se decodificaban a una cadena de texto.

#### 3.4.3 Verificación de Carga Útil Encriptada (Punto 4c)

Se ejecutaron nuevamente los scripts TCP y UDP, esta vez con la variable `ENCRYPT` establecida en `True` en todos ellos. Se utilizó Wireshark para capturar el tráfico, aplicando los mismos filtros de puerto que en las pruebas sin encriptación.

**Comparación para TCP**
Al seleccionar un paquete TCP de datos enviado por el cliente, la carga útil que antes era legible ahora se presenta como una secuencia de bytes aparentemente aleatorios, como se muestra en la Figura 3.5.
<center>

![Payload TCP Encriptado](<img/Data TCP_ENC.png>)

*Figura 3.5. Payload TCP Encriptado.*

</center>

Comparando la Figura 3.2 (payload no encriptado) y la Figura 3.5 (payload encriptado), es evidente que la información original ya no es visible directamente en la trama de red. A pesar de que los datos encriptados todavía son una secuencia de bytes, su interpretación como texto legible falla, demostrando la efectividad de la encriptación. Los logs de la aplicación, sin embargo, confirmaron que el servidor pudo desencriptar y procesar correctamente el mensaje original utilizando la clave Fernet compartida.

**Comparación para UDP**
De forma similar, para la comunicación UDP, la carga útil de los datagramas que antes era visible ahora aparece encriptada en Wireshark, como se observa en la Figura 3.6.

<center>

![Payload UDP Encriptado](<img/Data UDP_ENC.png>)

*Figura 3.6. Payload UDP Encriptado.*

</center>

La comparación entre la Figura 3.4 (payload no encriptado) y la Figura 3.6 (payload encriptado) nuevamente confirma que la carga útil ha sido protegida. Al igual que con TCP, los logs del servidor UDP indicaron la correcta desencriptación y procesamiento de los datos.

**Intento de Análisis Hexadecimal de Datos Encriptados**

Para reforzar la idea de que los datos están efectivamente encriptados y no son simplemente una codificación diferente de texto plano, se intentó decodificar los primeros bytes hexadecimales de las cargas útiles encriptadas (Figuras 3.5 y 3.6) como si fueran caracteres ASCII/UTF-8.

*   **Análisis del Payload TCP Encriptado (Figura 3.5):**
    La data hexadecimal visible en la Figura 3.5 comienza con: `674141414141426f4951...`
    Intentemos decodificar los primeros 10 bytes (20 caracteres hexadecimales):

    <center>

    | Hex | 67 | 41 | 41 | 41 | 41 | 41 | 42 | 6f | 49 | 51 |
    |:---:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
    | Char| g  | A  | A  | A  | A  | A  | B  | o  | I  | Q  |


    *Tabla 3.4: Intento de Mapeo Hexadecimal a Caracteres para Payload TCP Encriptado*
    </center>

    El resultado, "gAAAABoIQ", no corresponde a ninguna parte del mensaje original esperado (como "NoLoSonIEEE..."). Los primeros bytes de un token Fernet suelen ser `gAAAAA` (que es `0x674141414141` en hexadecimal, correspondiente a `gAAAAA` en Base64), indicando la versión y la estructura del token Fernet. El resto de los bytes no forman un patrón de texto legible y coherente.

*   **Análisis del Payload UDP Encriptado (Figura 3.6):**
    La data hexadecimal visible en la Figura 3.6 comienza con: `6741414141426f4f5166...`
    Intentemos decodificar los primeros 10 bytes (20 caracteres hexadecimales):

    <center>

    | Hex | 67 | 41 | 41 | 41 | 41 | 42 | 6f | 4f | 51 | 66 |
    |:---:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
    | Char| g  | A  | A  | A  | A  | B  | o  | O  | Q  | f  |

    
    *Tabla 3.5: Intento de Mapeo Hexadecimal a Caracteres para Payload UDP Encriptado*
    </center>

    Nuevamente, el resultado "gAAAABoOQf" no es texto plano significativo y es consistente con la estructura de un token Fernet.

Este análisis superficial de los primeros bytes de las cargas útiles encriptadas refuerza la conclusión de que la encriptación ha transformado los datos originales en una forma ininteligible sin la clave de desencriptación correcta, cumpliendo el objetivo de proteger la confidencialidad de la información.

#### 3.4.4 Encriptación sin Intercambio Previo de Información (Punto 4d)

En el escenario actual de nuestros scripts, la encriptación simétrica con Fernet se basó en la premisa de que tanto el cliente como el servidor ya poseían una clave secreta compartida (`ENCRYPTION_KEY`). Sin embargo, surge un desafío fundamental cuando dos entidades necesitan establecer una comunicación segura a través de una red insegura, especialmente si se encuentran a kilómetros de distancia y nunca han intercambiado información previamente. En tal caso, no existe un método trivial y seguro para compartir inicialmente una clave simétrica. Intentar enviar la clave simétrica sin protección la expondría a la interceptación.

La solución a este dilema se encuentra en el uso de la **encriptación asimétrica para facilitar el intercambio seguro de una clave de sesión simétrica.** Una vez que esta clave de sesión simétrica se ha establecido de forma segura, la comunicación de datos subsiguiente puede utilizar la encriptación simétrica, que es más eficiente. Este es el principio fundamental detrás de protocolos como TLS/SSL, que aseguran gran parte del tráfico web.

El proceso conceptual, similar a un handshake TLS simplificado, para que nuestros scripts establecieran una comunicación encriptada sin una clave precompartida sería el siguiente:

1.  **Generación de Pares de Claves por el Servidor:**
    *   El servidor, antes de aceptar conexiones o al iniciarse, generaría un par de claves asimétricas: una clave pública (`pub_S`) y una clave privada (`priv_S`) utilizando un algoritmo como RSA o ECC (Elliptic Curve Cryptography).
    *   La clave privada (`priv_S`) se mantendría en secreto por el servidor. La clave pública (`pub_S`) estaría destinada a ser compartida.

2.  **Obtención y Verificación de la Clave Pública del Servidor por el Cliente:**
    *   Cuando el cliente desea iniciar una comunicación segura, primero necesitaría obtener la clave pública (`pub_S`) del servidor.
    *   **El desafío crítico es la autenticidad de `pub_S`**. ¿Cómo sabe el cliente que la clave pública que recibe realmente pertenece al servidor legítimo y no a un atacante que se hace pasar por él, es decir un ataque "Man In the Middle"?
    *   Idealmente, este problema se resuelve mediante una **Infraestructura de Clave Pública**. El servidor tendría un **Certificado Digital** emitido por una **Autoridad Certificadora** de confianza. Este certificado vincula la identidad del servidor con su clave pública y está firmado digitalmente por la CA.
    *   El cliente, al recibir el certificado del servidor, verificaría su validez y la firma de la CA utilizando la clave pública de la CA. Si la validación es exitosa, el cliente puede confiar en la autenticidad de `pub_S`.

3.  **Generación y Encriptación de la Clave de Sesión Simétrica por el Cliente:**
    *   Una vez que el cliente confía en la clave pública del servidor (`pub_S`), el cliente generaría una nueva clave simétrica aleatoria, que llamaremos `key_sym_session`. Esta sería, por ejemplo, una clave adecuada para Fernet.
    *   El cliente luego encriptaría esta `key_sym_session` utilizando la clave pública del servidor (`pub_S`). Solo el poseedor de la clave privada correspondiente (`priv_S`) podrá desencriptar este mensaje.

4.  **Envío de la Clave de Sesión Encriptada al Servidor:**
    *   El cliente enviaría la `key_sym_session` al servidor.

5.  **Desencriptación de la Clave de Sesión por el Servidor:**
    *   El servidor recibiría la clave de sesión encriptada.
    *   Utilizando su propia clave privada (`priv_S`), el servidor desencriptaría el mensaje para obtener la `key_sym_session` original.

6.  **Establecimiento de la Comunicación Simétrica Segura:**
    *   En este punto, tanto el cliente como el servidor poseen la misma `key_sym_session` secreta, la cual fue transmitida de forma segura gracias a la encriptación asimétrica.
    *   Toda la comunicación de datos subsiguiente se encriptaría y desencriptaría utilizando esta `key_sym_session` y un algoritmo simétrico eficiente como Fernet.

**Implementación Conceptual en los Scripts:**

Aunque no se requiere programar esta funcionalidad para el presente trabajo práctico, su implementación conceptual en los scripts involucraría:
*   Utilizar módulos de la librería `cryptography` como `cryptography.hazmat.primitives.asymmetric.rsa` para la generación de claves públicas/privadas RSA/ECC, y para las operaciones de encriptación y desencriptación asimétrica.
*   Modificar el inicio de la comunicación:
    *   El servidor necesitaría una forma de enviar su clave pública (o certificado) al cliente cuando este se conecta.
    *   El cliente necesitaría recibir esta clave pública, generar la clave de sesión Fernet, encriptarla asimétricamente y enviarla al servidor.
    *   El servidor recibiría y desencriptaría esta clave de sesión.
*   Una vez establecida la `key_sym_session`, los mecanismos de encriptación/desencriptación simétrica con Fernet, ya implementados en los scripts para el Punto 4c, se utilizarían con esta nueva clave de sesión dinámica en lugar de una clave precompartida en los archivos de configuración.

Este enfoque híbrido aprovecha la seguridad de la criptografía asimétrica para el intercambio de claves y la eficiencia de la criptografía simétrica para la protección de los datos en tránsito.



## 4. Conclusiones

La realización de este trabajo práctico ha permitido consolidar de manera efectiva los conocimientos teóricos sobre los protocolos de transporte TCP y UDP, así como los fundamentos de la encriptación de datos en red, a través de su aplicación práctica mediante el desarrollo de scripts en Python y el análisis de tráfico con Wireshark.

Los principales aprendizajes y resultados obtenidos son:

1.  **Implementación y Funcionamiento de TCP y UDP:** Se logró desarrollar con éxito aplicaciones cliente-servidor funcionales para ambos protocolos. Se verificó la naturaleza orientada a conexión de TCP, evidenciada por el handshake de tres vías y la transmisión confiable de datos. En contraste, UDP demostró su simplicidad y menor overhead al no requerir establecimiento de conexión.

2.  **Análisis de Tráfico y Carga Útil:** La utilización de Wireshark fue fundamental para visualizar la estructura de los paquetes TCP y UDP, identificar sus respectivos encabezados y, crucialmente, verificar el contenido de la carga útil transmitida. Se pudo constatar cómo la carga útil viaja en texto plano en una comunicación no encriptada.

3.  **Métricas de Rendimiento:** El registro de timestamps y el cálculo de métricas como latencia y jitter proporcionaron una base cuantitativa para comparar el rendimiento de TCP y UDP. Estas métricas, aunque obtenidas en un entorno de red local, ilustran las compensaciones inherentes a cada protocolo.

4.  **Encriptación de la Carga Útil:** La implementación de la encriptación simétrica con Fernet demostró ser un método efectivo para proteger la confidencialidad de la información transmitida. Al analizar el tráfico encriptado con Wireshark, se confirmó que la carga útil original ya no era discernible, siendo reemplazada por una secuencia de bytes cifrados, mientras que la aplicación en el extremo receptor pudo desencriptarla correctamente. Esto subraya la importancia de la encriptación para la seguridad en las comunicaciones.

5.  **Intercambio Seguro de Claves:** La investigación teórica sobre encriptación simétrica y asimétrica reforzó la comprensión de sus respectivos roles y limitaciones, particularmente la necesidad de mecanismos como la encriptación asimétrica para el establecimiento seguro de claves de sesión simétricas en escenarios donde no existe un canal seguro preestablecido.

En resumen, este trabajo práctico ha proporcionado una valiosa experiencia en la programación de sockets, el análisis de protocolos de red y la aplicación de técnicas de seguridad básicas. Los objetivos propuestos fueron cumplidos, logrando no solo la implementación funcional de los scripts sino también una comprensión más profunda de los mecanismos subyacentes que rigen la comunicación y la protección de datos en las redes de computadoras. Las habilidades adquiridas son fundamentales para el posterior estudio y desarrollo en el campo de las redes y la ciberseguridad.
