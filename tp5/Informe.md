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
