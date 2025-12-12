**Nombre Completo**: Machine Learning-Assisted Virtual Patching of Web Applications

# Resumen

**Propuesta**: WAF con ML basado en clasificación de una clase y análisis de N-grams, para mejorar las capacidades de detección y precisión, comparándose con ModSecurity.

**Resultados**: Supera a ModSecurity cuando se configura el modelo propuesto con el conjunto de reglas básicas de OWASP. Este modelo permite implementar un WAF cuando no hay datos de entrenamiento disponibles para la aplicación (usando una clasificación de una clase), y uno mejorado usando N-grams cuando hay datos de entrenamiento disponibles.

**Index Terms**: WAF, ML, Detección de Anomalías, Clasificación de una Clase, N-Grams

# Insights

- **Limitaciones de los WAF basados en Reglas**: Los WAF Tradicionales como ModSecurity, configurados con el OWASP Core Rule Set (CRS), tienen limitaciones significativas, como la generación de una alta tasa de falsos positivos, que en algunos casos puede acercarse al $40\%$. Las reglas son estáticas, rígidas y necesitan un ajuste manual (rule tuning) por lo cual necesitan mucho tiempo y es propenso a errores para cada aplicación específica
- **Potencia de WAF basados en Modelos de ML**: El enfoque basado únicamente en reglas puede complementarse con modelos de ML, detección de anomalías y enfoques estadísticos para ofrecer mayores niveles de flexibilidad y adaptabilidad
- **Detección de Ataques mediante Anomalías**: El enfoque de detección de anomalías es valioso porque puede detectar potencialmente ataques de día cero (zero-day-attacks) y solo requiere una colección de solicitudes HTTP válidas (tráfico normal) para el entrenamiento, eliminando la necesidad de datos etiquetados de ataques
- **Combinación de Expertos**: Se propone un enfoque combinado de modelos de ML para mejorar las capacidades de detección y precisión de ModSecurity. Esta composición de enfoques permite reconocer una clase más amplia de ataques a aplicaciones web.
- **Presentación de Escenarios Complementarios**: La solución propuesta ofrece dos modelos de aprendizaje complementarios, cada uno diseñado para un escenario operativo distinto.
  - _Escenario I_ (_Clasificación de Una Clase_ o _One-Class Classification_): Es ideal para el despliegue rápido cuando no hay un conjunto de datos de entrenamiento específico de la aplicación disponible (por ejemplo, sitios públicos que cambian constantemente). Se puede entrenar usando datos genéricos recopilados de otras aplicaciones
  - _Escenario II_ (_Análisis de N-Gramas_): Es adecuado para aplicaciones de misión crítica donde se requieren altos niveles de seguridad y los cambios están controlados. Este enfoque requiere un conjunto de datos específico de la aplicación para modelar la firma de lenguaje de cada campo de entrada.
- **Resultados y Experimentos**: La solución propuesta supera el rendimiento de ModSecurity configurado con OWASP CRS. En particular, el enfoque de $N$-Gramas supera claramente los resultados de ModSecurity en los conjuntos de datos probados

# Análisis: Problema | Solución

- **Alta Tasa de Falsos Positivos (FP) y Rigidez de Reglas** $\to$ **Combinación de Clasificadores**: Se propone una estrategia de integración simple: si el enfoque de una clase (one-class) clasifica una solución como válida y ModSecurity la clasifica como ataque, se da prioridad al resultado de la clasificación de una clase. Esto reduce la cantidad de falsos positivos generados por el CRS.
- **Vulnerabilidad a Ataques Desconocidos (Zero Day)** $\to$ **Detección de Anomalías**: Al enfocarse en caracterizar el comportamiento de entrada válido (enfoque positivo), cualquier desviación (anomalía) se considera un ataque potencial, lo que permite detectar ataques de día cero

# Análisis de ModSecurity

ModSecurity es un WAF open-source y ampliamente utilizado que permite el monitoreo, registro y control de acceso de aplicaciones web en tiempo real. El core de este implementa un motor de reglas (rule engine) que puede configurarse en cada transacción de la aplicación. Las acciones que lleva a cabo ModSecurity están impulsadas por reglas que especifican, mediante expresiones regulares, el contenido de los paquetes HTTP que deben ser identificados

ModSecurity tiene dos modos de operación: detección y prevención.

- _Detección_: En este modo, se generan registros de cada ataque potencial detectado y se utilizan para monitorear reglas específicas. Este modo se utiliza normalmente en lo que se denomina la fase de aprendizaje
- _Prevención_: Este es el modo en el que el WAF es realmente útil. Mediante la configuración correcta de reglas y directivas. ModSecurity es capaz de bloquear el tráfico web potencialmente malicioso

# Virtual Patching

**Security Virtual Patching** (**Parcheo Virtual de Seguridad**): Técnica de remediación. Se utiliza como solución cuando la inspección y corrección del código fuente de una aplicación web no es siempre factible, especialmente si se trata de aplicaciones críticas que no pueden ser desconectadas (off-line) hasta que se corrija un error, o si el código fuente ya no es accesible o parchable.

El documento se enfoca en mejorar el funcionamiento del FAW, ModSecurity, el cual actúa como este parcheador virtual. Virtual Patching puede aplicarse a cualquiera de las capas principales de las aplicaciones web: cliente, lógica de negocio y base de datos

# Definiciones Importantes

**Web Apps**: Software basado en una arquitectura Server-Client, que incorpora un conjunto coordinado de funciones. La información que fluye entre el cliente, que se ejecuta en el navegador web del usuario, y el servidor de aplicaciones se transmite mediante el protocolo HTTP.

**WAF**: Software que intercepta e inspecciona todo el tráfico entre el servidor web y sus clientes, buscando ataques dentro del contenido del paquete HTTP. Una vez reconocidos, los paquetes sospechosos pueden procesarse de una manera diferente y segura.

**ModSecurity**: WAF open-source y ampliamente utilizado que permite la supervisión, el registro y el control de acceso de aplicaciones web en tiempo real. Las acciones que emprende este firewall están impulsadas por reglas que especifican mediante expresiones regulares el contenido de los paquetes HTTP que se van a detectar. ModSecurity ofrece un conjunto de reglas predeterminado, conocido como OWASP Core Rule Set (OWASP CRS), para abordar las diferentes vulnerabilidades más comunes y peligrosas.

- **Limitaciones**: Enfoque basado únicamente en reglas las cuales son estáticas y rígidas por naturaleza, por lo que suele producir falsos positivos, que incluso llegan a acercarse al $40\%$. El ajuste de reglas es una tarea que requiere mucho tiempo y es propensa a errores y que debe realizarse manualmente para cada aplicación web específica $\implies$ En los firewalls de redes tradicionales e IDS, el enfoque basado en reglas se ha completado con éxito con otras herramientas basadas en aprendizaje automático, detección de anomalías y otros enfoques estadísticos que proporcionan mayores niveles de flexibilidad y adaptabilidad. Estos enfoques aprovechan datos de muestra, a partir de los cuales se puede conocer el comportamiento normal de la aplicación web, para detectar situaciones sospechosas que quedan fuera de este uso nominal (anomalías) y que podrían corresponder a ataques en curo.

# Escenarios

**Escenario I**: **Implementación sin Datos de Entrenamiento Específicos**: Este escenario aborda la necesidad de proteger una aplicación cuando no se tiene un conjunto de datos (dataset) específico de la aplicación para entrenar el modelo de seguridad.

- _Contexto de Aplicación_: Es adecuado para aplicaciones web que cambian constantemente, como sitios web públicos que funcionan con un gestor de contenidos (content manager)
- _Enfoque de Seguridad_: Se propone utilizar el método de Clasificación de una Sola Clase (One-Class Classification). Este enfoque aprende el comportamiento de las solicitudes válidas e identifica los ataques como desviaciones o anomalías del comportamiento normal aprendido
- _Datos de Entrenamiento_: La principal ventaja es que el clasificador puede entrenarse utilizando una mezcla de conjuntos de datos de otras aplicaciones web
- _Objetivos Principales_:
  1.  Determinar si es posible construir un sistema de detección de ataques aprendiendo de datos de entrenamiento genéricos, recopilados de otras aplicaciones web.
  2.  Mejorar los resultados de ModSecurity (configurado con OWASP CRS) reduciendo la alta tasa de falsos positivos (FP) que genera
- _Datasets Genéricos_: CSIC2010, DRUPAL
- _Resultados_:
  - Es fácil de implementar y tiene la capacidad de adaptarse a los cambios en la aplicación web.
  - Supera a ModSecurity, con una degradación de rendimiento no crítica en comparación con el entrenamiento con datos específicos

---

**Escenario II**: **Alta Seguridad con Datos de Entrenamiento Específicos**: Escenario está diseñado para situaciones que requieren el más alto nivel de seguridad y donde se dispone de datos específicos de la aplicación

- _Contexto de Aplicación_: Se utiliza para proteger una aplicación web crítica para el negocio donde los cambios están controlados.
- _Condición Requerida_: Se requiere que haya un dataset específico de la aplicación con solicitudes válidas para entrenar el modelo
- _Limitación Existente_: Las capacidades de detección proporcionadas por el enfoque de una clase no se adaptan tan bien para prevenir tanto los ataques de día zero como los ataques que explotan vulnerabilidades específicas de una aplicación, en particular aquellas que involucran entradas sospechosas
- _Metodología Propuesta_ / _Solución_: Se propone utilizar el enfoque de **Detección de Anomalías basado en Análisis de N-Gramas**.
  - Técnicas que utilizan $N$-Grams de alto orden hasta algunos $n$ para proporcionar capacidades de detección de anomalías basadas en la firma de lenguaje esperada de los campos de entrada de la aplicación. El enfoque de $N$-Grams requiere tener un conjunto de datos específico de la aplicación con una solicitud válida para entrenar el modelo. Al modelar la firma del lenguaje de cada atributo de la aplicación web, es posible reconocer ataques conocidos con buena precisión y también detectar ataques de día cero (Zero-Day Attack).
- _Ventajas Clave_: Este método se basa en la característica positiva de la normalidad. Al modelar la firma lingüística de cada atributo, permite detectar ataques de día cero (Zero-Day Attack) y ataques que explotan vulnerabilidades específicas, además de reconocer ataques conocidos con buena precisión
- _Objetivo Primario_: Entender el rendimiento que pueden alcanzar los métodos de aprendizaje automático en comparación con ModSecurity
- _Resultados Clave_: Los resultados indican que el enfoque de $N$-gramas es una buena solución si se dispone de un conjunto de datos específico de la aplicación para el entrenamiento, ya que supera claramente los resultados de ModSecurity en términos de tasas de verdaderos positivos (TPR) y tasas de verdaderos negativos (TNR)

# Modelos de ML

## Análisis Básico

**Training Set**: El modelo se construye a partir de un conjunto de entrenamiento $T$ de solicitudes HTTP normales que han sido grabadas previamente. Se asume que este conjunto es representativo del tráfico legítimo. Dado que la comunicación se realiza mediante el protocolo HTTP, las solicitudes son mensajes de texto plano (ASCII) que contienen un encabezado de solicitud, una colección de campos de encabezado (en formato `field=value`) y, posiblemente, un cuerpo de solicitud.

---

**Pre-Processing**: En esta fase, antes de construir el modelo estadístico, las solicitudes son pre-procesadas para decodificar la información que contienen (por ejemplo, decodificación URL). Esto también puede implicar el análisis de parte de la estructura de la solicitud HTTP o la eliminación de partes consideradas inútiles para el modelo. El grado de granularidad del análisis de la estructura de la solicitud constituye una elección fundamental en el diseño del modelo.

---

**Feature Extraction**: Se extrae una colección de características (features) de la solicitud. Estas características están relacionadas con las ocurrencias de una colección $A$ de subcadenas o TOKENS dentro de la solicitud. Se experimenta con dos criterios para seleccionar estos tokens, lo que da lugar a los dos modelos propuestos:

1. Utilizar una colección fija de palabras determinada por un experto en seguridad
2. Computar automáticamente los tokens a partir del conjunto de entrenamiento (n-grams)

La representación interna de las solicitudes resultantes se concibe como un vector de números o un bag-of-words, donde cada posición contiene el número asociado a un token dado.

---

**Model Computation** (**Cómputo del Modelo**): El modelo $M$ es una distribución probabilística para los elementos de la representación interna, estimada a partir de los datos calculados para las solicitudes en el conjunto de entrenamiento $T$. Esta distribución proporciona la firma que caracteriza las solicitudes HTTP normales. Desde una perspectiva geométrica, el modelo puede verse como un hipervolumen que contiene todos los puntos (vectores) correspondientes a la representación interna de una solicitud HTTP normal

---

**Request Classification** (**Clasificación de Solicitudes**): El WAF utiliza el modelo $M$ para analizar las solicitudes HTTP entrantes en línea, clasificándolas en dos clases: normales o anormales (potenciales ataques).

1. Se calcula la representación interna de la solicitud entrante ($r$)
2. Se computa un score $s_{r} = \text{dist}(r,M)$, utilizando una función de distancia que mide qué tan lejos está la firma real de $r$ de la firma esperada proporcionada por el modelo $M$
3. Un puntaje de 0 significa que el contenido coincide perfectamente con la firma esperada; cuanto mayor sea el score, menos se ajusta a la distribución de frecuencia esperada
4. Finalmente, se aplica un criterio $C(M,r)$ para decidir si la distancia es suficiente para considerar la solicitud $r$ como anómala

## Análisis Detallado: One-Class Classification

Este enfoque se utiliza en el Escenario I y busca reducir la alta tasa de falsos positivos de ModSecurity.

- _Concepto_: Se asume que la información de entrenamiento solo esta disponible para una clase (solicitudes válidas), un concepto también llamado detección de novedad (novelty detection). El objetivo es aprender el comportamiento de las solicitudes válidas e identificar los ataques como desviaciones de ese comportamiento aprendido
- _Pre-Processing_: Además de la decodificación, se filtran los headers de la solicitud, que se utilizan para intercambiar información contextual entre el agente de usuario y el servidor. Se eliminan los datos específicos del protocolo (cookies, proxies e IP) que no representan el comportamiento del usuario y no deben usarse para inferir el comportamiento de la aplicación
- _Feature Extraction_: Se basa en el conocimiento de un experto en seguridad para capturar las propiedades de ataques comunes (SQLi, XSS). Se utiliza un modelo de BoW donde los tokens son características especiales y subcadenas (como `select`, `alert`, `$`, `<`, `>`). El vector de características cuenta la aparición de cada una de estas palabras en la cadena de consulta de la URL, el cuerpo de la solicitud y los headers
- _Model Computation_: Se utiliza un Modelo de Mezcla Gaussiana (GMM) para estimar la función de densidad de probabilidad (PDF) de los datos de entrenamiento válidos. El algoritmo Expectation Maximization (EM) se usa para estimar los parámetros del GMM, donde cada componente constituye un clúster que captura la distribución de las solicitudes válidas
- _Request Classification_: Se utiliza la Distancia de Mahalanobis para medir la distancia de un vector de características a la distribución capturada por un componente del GMM. La distancia mide cuántas desviaciones estándar está la solicitud de la media de la distribución. El umbral $t_{C_{k}}$ para cada clúster se define como $t_{C_{k}} = \lambda[ \text{dist}_{k} + 10 \times \text{std}_{k} ]$, donde $\lambda$ permite variar la precisión del modelo. Si la distancia a cualquier clúster es inferior al umbral, la solicitud se clasifica como normal; de lo contrario, se clasifica como ataque.

## Análisis Detallado: N-Grams

Este enfoque se utiliza en el Escenario II y busca alta seguridad en aplicaciones críticas.

- _Concepto_: Caracteriza positivamente el comportamiento normal de cada aplicación. Utiliza n-grams (secuencia de $n$ símbolos, que pueden ser caracteres o palabras) para modelar la firma lingüística esperada de los campos de entrada. Es capaz de reconocer ataques conocidos y detectar ataques de día cero (Zero-Day Attack)
- _Pre-Processing_: Implica un procesamiento de tokenización para dividir el texto en subcadenas separadas por delimitadores, como `/` o `&`. A diferencia del OCC, este método parsea la estructura HTTP, conservando el contenido de los campos modelo (campos de header o parámetros de la aplicación web) y descartando sus nombres. Se aplica una función de abstracción que, por ejemplo, convierte las letras a minúsculas, elimina acentos y reemplaza los dígitos por la letra mayúscula "N" para evitar el overfitting
- _Feature Extraction_: Los atributos básicos son pares $(x,z)$, donde $x$ es el campo modelo y $z$ es el n-grama. Se asocia una variable aleatoria a cada atributo para medir el número de ocurrencias o la frecuencia del n-grama en el campo. También se añade un atributo para medir la longitud (número de caracteres) de cada campo modelo, un indicador útil para ataques de inyección de código
- _Model Computation_: Se asume que las variables aleatorias de cada atributo son independientes. El modelo construye una distribución independiente para cada atributo, proporcionando una firma lingüística específica para cad acampo. Se utiliza el algoritmo de Welford para aproximar incrementalmente la media y la varianza de la distribución
- _Request Classification_: La solicitud se prueba calculando un mapa de valores concretos para cada atributo. Si un campo modelo ($x$) no está definido en el modelo $M$ (es decir, no fue visto durante el entrenamiento), la solicitud se rechaza como anómala. El score se calcula sumando las distancias de Mahalanobis, que mide cuántas desviaciones estándar está la firma de la solicitud de la firma lingüística del campo. Si el score de cualquier campo no satisface el criterio (cae fuera del rango de valores mínimo y máximo de la distribución del entrenamiento), la solicitud se considera anómala
