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