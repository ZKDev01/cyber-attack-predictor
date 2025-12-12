**Nombre Completo**: Adaptively Detecting Malicious Queries in Web Attacks

# Resumen

El documento aborda el problema de la detección de consultas (queries) maliciosas en ataques web, especialmente aquellos que utilizan Code Injection. Los ataques web, que utilizan exclusivamente el protocolo HTTP/HTTPS, han aumentado explosivamente. Los enfoques de detección existentes, ya sean basados en firmas o en anomalías, utilizan modelos constantes o estáticos que se vuelven obsoletos e incapaces de detectar los ataques desconocidos más recientes debido a la sofisticación de los atacantes.

- **Desafío**: _Deficiencia_: Incapacidad de identificar ataques desconocidos más recientes debido a que los modelos son estáticos/constantes
- **Desafío**: _Proceso Altamente Costoso de Etiquetado Manual del Tráfico_ $\to$ Se busca construir un sistema de detección de consultas maliciosas que pueda incorporar de forma adaptativa las últimas consultas importantes para actualizar el modelo de detección

Para solucionar esta deficiencia, se propone **AMODS** (**Adaptive Malicious Query Detection System**), un sistema adaptativo diseñado para actualizar periódicamente su modelo de detección. El núcleo de AMODS es una estrategia de aprendizaje adaptativo llamada **SVM HYBRID** que combina la **Selección de Sospechas** (**Suspicion Selection**, **SS**) y la **Selección de Ejemplares** (**Exemplar Selection**, **ES**). Esta estrategia permite seleccionar una cantidad trivial de "consultas importantes" para el etiquetado manual, reduciendo drásticamente el trabajo necesario para mantener el modelo actualizado.

- _Solución a Deficiencia_: Primer sistema de aprendizaje adaptativo en la detección de ataques web

El modelo de detección es un clasificador de conjunto basado en _stacking_ (generalización apilada), que utiliza SVM como su meta-clasificador, lo que permite a SVM HYBRID funcionar eficazmente. El sistema fue evaluado con un conjunto de datos real de consultas de 10 días recogido de los registros de un servidor web académico.

- **Inexistencia de Dataset para Implementación**: No hay datos públicos disponibles para la detección de ataques web, y que los trabajos existentes utilizaron sus propios conjuntos de datos para la evaluación

Los resultados de AMODS muestran un rendimiento superior a los métodos existentes, logrando un F-value del $94.79\%$ y una tasa de falsos positivos (False Positive Rate) del $0.09\%$. Además, la estrategia SVM HYBRID obtuvo un número total de consultas maliciosas $2.78$ veces mayor que el método popular SVM AL, lo que demuestra su capacidad para obtener ataques desconocidos y actualizar la biblioteca de firmas del Web Application Firewall (WAF)

El documento busca detectar consultas (queries) maliciosas en ataques web, especialmente aquellos que utilizan inyección de código (como Cross-Site Scripting (XSS), SQL Injection (SQLI), Directory Traversal (DT), Remote File Inclusion (RFI)). Existen diferentes enfoques de detección, ya sea basados en firmas (signature-based) o en anomalías (anomaly-based), los cuales presentan modelos de detección constantes que se vuelven obsoletos rápidamente frente a la sofisticación de los atacantes y los continuos cambios en los ataques.

# Análisis: AMODS

**Contribución (Adaptive Learning)**:

- Sistema de aprendizaje adaptativo a partir de la selección de consultas importantes que permiten actualizar de forma periódica el modelo de detección interno, logrando así identificar los ataques desconocidos más recientes.
- Representa la primera investigación conocida en la detección adaptativa de ataques web.

**Concepto Central**: Superar la obsolescencia de los modelos de detección constantes. Esta propuesta logra esto al:

- Incorporar consultas importantes (informativas benignas y maliciosas representativas) para mantener el modelo de detección actualizado
- Utilizar SVM HYBRID para obtener estas consultas de manera eficiente, minimizando el etiquetado manual necesario

**Tipos de Ataque que Detecta**: Inyección de Código basados en web como: XSS, SQLi, DT, RFI

- El sistema también incluye la Ejecución Remota de Código (RCE) dentro del ataque XSS, ya que RCE es esencialmente un tipo especial de ataque XSS

**Componentes**:

- **Modelo de Detección Subyacente**: Clasificador de conjuntos basado en _stacking_ (generalización apilada)
  - Stacking-based ensemble classifier, compuesto por 3 clasificadores base (seleccionados para obtener diversidad de aprendizaje) y un meta-clasificador
  - SVM con RBF Kernel como meta-clasificador
- **Estrategia de Aprendizaje Adaptativo** (**SVM Hybrid**): Estrategia híbrida que aprovecha la función del meta-clasificador SVM para obtener las "consultas importantes":
  - **Suspicion Selection** (**SS**):
    - _Función_: Adquiere las consultas más importantes e informativas (llamadas suspicions)
    - _Ubicación_: Se encuentra dentro de la región de confusión (confusing region), cerca del hiperplano de SVM
    - _Contribución_: Mejorar el rendimiento de la detección
  - **Exemplar Selection** (**ES**):
    - _Función_: Se especializa en la recolección de consultas maliciosas representativas (llamadas exemplars)
    - _Ubicación_: Se encuentran en el lado malicioso (parte superior del hiperplano) y lejos del hiperplano
    - _Contribución_: Conserva consultas verdaderamente maliciosas

**Ventajas**:

- _Adaptabilidad_: Primer sistema conocido para la detección adaptativa de ataques web, capaz de detectar los últimos ataques desconocidos
- _Eficiencia en Etiquetado Manual_: SVM HYBRID selecciona una cantidad mínima de consultas importantes, reduciendo el trabajo manual al mínimo ($0.15\%$ de las consultas desconocidas)
- _Alto Rendimiento_: Supera a los métodos de detección existentes con una alta tasa de verdaderos positivos (True Positive Rate) y una baja tasa de falsos positivos (False Positive Rate)
- _Capacidad de Recolección_: Obtiene un número significativamente mayor de consultas maliciosas ($2.78$ veces más que SVM AL), que pueden usarse para actualizar la biblioteca de firmas del WAF
- _Precisión Mejorada_: La combinación de SS (mejora de rendimiento) y ES (recolección de consultas maliciosas) hace que AMODS sea superior a los métodos que solo se enfocan en la incertidumbre (como SVM AL)
- _Nuevo Concepto y Aplicación en el Modelo_: "**Importance Queries**" $\to$ Consultas normales más informativas y consultas maliciosas más informativas

**Limitaciones**:

- _Labeling Unknow Queries_: AMODS requiere una cantidad trivial de etiquetado manual para las consultas importantes seleccionadas. Para abordar esto se sugiere aplicar Aprendizaje No-Supervisado para evitar el mantenimiento humano
- _Code Obfuscation_: Metodología de etiquetado inicial puede ser eludida por ataques que utilizan code obfuscation, aunque el sistema asume que las consultas ofuscadas son maliciosas; esto es racional porque: este en la web busca evitar la detección y es inútil ofuscar solicitudes web benignas
- _Concept Drift_: Los cambios en la aplicación web (web application concept drift) pueden llevar a la clasificación errónea de comportamientos normales como falsos positivos si el modelo no está al tanto del cambio
- _Dependencia de N-Grams_: El uso de características basadas en $N$-grams puede ser limitado para interpretar patrones de ataque más complejos, por lo que se propone usar Deep Learning en el futuro
- _Problemas relacionados NO abarcados_: Explotación de vulnerabilidades y generación de firmas
  - El sistema guarda los ataques pero no construye una base de datos de firmas
  - Detecta amenazas pero no recopila cuales son las vulnerabilidades del sistema para trabajos futuros

**Observaciones**:

- El modelo parece crecer a medida que detecta nuevas amenazas, debido a que debe almacenar las consultas maliciosas
- El documento no muestra el crecimiento de la tasa de detección ya que debería aumentar a medida que el modelo recolecta datos cada día

# Insights

- **Deficiencia de Modelos Constantes**: Los enfoques de detección existentes no pueden hacer frente a la evolución de los ataques web con modelos de detección estáticos
- **Propuesta de Adaptabilidad**: Se propone AMODS, primer sistema adaptativo conocido para la detección de ataques web, que actualiza periódicamente el modelo
- **Estrategia de Etiquetado Eficiente**: Se utiliza SVM HYBRID para minimizar el trabajo manual al seleccionar solo una cantidad trivial de "consultas importantes"
- **Doble Función de SVM HYBRID**: Se compone de: _Suspicion Selection_ (SS), que mejora el rendimiento de detección, y _Exemplar Selection_ (ES), que cosecha consultas maliciosas representativas
- **Rendimiento de Detección**: AMODS supera a otros métodos con un F-value del $94.79\%$ y una tasa de falsos positivos (FP) del $0.09\%$
- **Recolección de Ataques Desconocidos**: AMODS obtuvo 2.78 veces más consultas maliciosas que el método SVM AL, lo que permite actualizar la biblioteca de firmas del WAF
- **Enfoque en Consultas**: La detección de consultas maliciosas (queries) es fundamental, ya que contienen la mayoría de las entradas de usuario, que son vectores de ataque para XSS, SQLi, DT y RFI
- **Relación con Meta-Learning**: La capacidad de aprender de diferentes sesgos de aprendizaje hace que el Meta-Learning sea un enfoque apropiado para la detección de consultas maliciosas, debido a la naturaleza compleja, dinámica y conflictiva de su dominio problemático

# HTTP Attack Detection y Web Attack Detection

**¿Qué diferencia existe entre HTTP Attack Detection y Web Attack Detection?**: La diferencia principal radica en el nivel de la pila de red en el que operan y el tipo específico de datos que analizan:

- **Detección de Ataques HTTP**
  - _Protocolo_/_Fuente_: Estos métodos toman el tráfico de red del puerto 80 (tráfico HTTP) como fuente de datos
  - _Capa de Operación_: Modelan la carga útil del paquete HTTP (HTTP packet payloads) y operan en la capa de paquete (packet layer)
  - _Métodos Comunes_: Incluyen técnicas como modelos de Markov, análisis de $N$-gram y clasificadores de una sola clase
- **Detección de Ataques Web**
  - _Protocolo_/_Fuente_: Se enfoca en ataques que usan exclusivamente el protocolo HTTP/HTTPS. La fuente de datos suele ser los registros del servidor web
  - _Capa de Operación_: Analizan las consultas (queries) en el tráfico web (es decir, las cadenas de consulta de la solicitudes) y operan en la capa de aplicación (application layer)
  - _Propósito Específico_: El objetivo es detectar ataques de Code Injection (como SQLi, DT, RFI), ya que la mayoría de los datos de entrada del usuario existen en las consultas
  - _Novedad_: El sistema AMODS propuesto cae en la categoría de métodos adaptativos para la detección de ataques web.

Mientras que los métodos de Detección de Ataques HTTP operan en la capa de paquete y se centran en la carga útil general del paquete, los métodos de Detección de Ataques Web, como AMODS, operan en la capa de aplicación y se centran específicamente en el contenido de las cadenas de consulta para detectar ataques como Code Injection

# Proceso de Construcción y Operación de AMODS

![[Adaptively Detecting Malicious Queries in Web Attacks. Image 1.png]]
El proceso de construcción consiste en los siguientes pasos sobre una iteración para cada lote de consultas desconocidas:

1. **Inicialización del Sistema**:
   1. _Recopilación del Conjunto de Entrenamiento Inicial_: Se comienza con un training pool compuesto por un pequeño conjunto de consultas etiquetadas. En los experimentos se utilizó un conjunto inicial de 100 consultas (80 benignas y 20 maliciosas)
   2. _Entrenamiento del Modelo Inicial_: Se entrena el modelo de detección inicial (el clasificador _stacking_ con SVM como meta-clasificador)
2. **Proceso Iterativo** (**Detección Adaptativa Diaria**):
   1. _Recolección de Consultas Desconocidas_: Se recolectan las consultas (unknown queries) de los registros del servidor web (por lotes, por ejemplo, diariamente)
   2. _Preprocesamiento de Datos_: Las consultas sin procesar se transforman en vectores de características (mediante preparación, construcción de características N-grams de frecuencia y reducción de características)
   3. _Clasificación_: Las consultas desconocidas (en el primer día de un lote) se clasifican utilizando el modelo de detección actual
   4. _Selección de Consultas Importantes_: Se aplica la estrategia SVM HYBRID a las consultas clasificadas para obtener un número fijo de "consultas importantes". Para el caso óptimo C, la proporción $\theta$ se fija en 7:3 ($70\%$ para SS, $30\%$ para ES)
      1. **SS**: Identificacion de sospechas mediante _K-medoids clustering_ en la región de confusión
      2. **ES**: Identificación de ejemplares utilizando el _algoritmo Kernel Farthest-First_ (**KFF**) en el lado malicioso del hiperplano
   5. _Etiquetado Manual_: Las consultas importantes obtenidas (sospechosas y ejemplares) se etiquetan manualmente
   6. _Actualización de Signature Library_: Las consultas etiquetadas como maliciosas se utilizan para actualizar la biblioteca de firmas del WAF
   7. _Actualización del Modelo de Detección_: Todas las consultas importantes recién etiquetadas se añaden al training pool (conjunto de entrenamiento) y el modelo de detección se actualiza (reentrenamiento)
   8. _Iteración_: Los pasos 3 a 7 se repiten para el resto de las consultas desconocidas en el lote

## SVM HYBRID

SVM HYBRID: Estrategia de aprendizaje adaptativo propuesta que obtiene consultas importantes para actualizar el modelo de detección de consultas maliciosas. Opera en el espacio de características del kernel de SVM y se basa en las posiciones de las muestras de consulta en el espacio de características del kernel de SVM para decidir las consultas para el etiquetado. SVM se ha desempeñado extremadamente bien en muchos dominios, particularmente aquellos que involucran clasificación de texto.
![[Pasted image 20251202050732.png]]

# SVM HYBRID

**SVM HYBRID**: Estrategia de aprendizaje adaptativo que aprovecha el sistema adaptativo de AMODS, que es un híbrido de Suspicion Selection (SS) y Exemplar Selection (ES).

- El Modelo de Detección Subyacente (Clasificadores Base y Meta Clasificador) opera después de la fase de preprocesamiento, tomando los vectores de características $N$-grams (que representan las consultas) y clasificándolos como benignos o maliciosos
- Esta estrategia opera después de la clasificación. Toma las consultas desconocidas ya clasificadas del primer día de un lote y utiliza el modelo SVM entrenado para proyectarlas en su espacio de kernel para determinar su proximidad al hiperplano o a los ejemplares maliciosos, seleccionando así las consultas importantes para el etiquetado manual

## Definición de SVM

**SVM** (**Support Vector Machines**) es un clasificador lineal utilizado para separar muestras positivas y negativas mediante un hiperplano ($w^Tx + b = 0$). El objetivo de este clasificador es encontrar el hiperplano óptimo que maximice el margen, definido como la máxima distancia perpendicular entre las muestras de las dos clases. Si las muestras de entrada originales no son linealmente separables, pueden mapearse a un nuevo espacio de características de kernel donde son linealmente separables. El parámetro de penalización $C$ controla el equilibrio entre un margen grande y una tasa baja de clasificación errónea de los datos de entrenamiento: un $C$ pequeño favorece un margen grande (clasificador de margen suave)

## Desarrollo de SS y ES

SVM HYBRID opera en el espacio de características de kernel de SVM y utiliza la posición de las muestras de consulta en ese espacio para decidir qué consultas etiquetar. Las consultas importantes son las sospechas (suspicions) y los ejemplares (exemplars).

- **Suspicion Selection** (**SS**)
  - _Función_: Adquiere las consultas informativas más importantes (sospechas), que se sospecha que son maliciosas
  - _Ubicación_: Las sospechas se encuentran dentro de la región propensa a ser mal clasificada, denominada la **Región de Confusión**
  - _Metodología_: SS busca preservar la distribución de la densidad de datos utilizando el clustering K-medoids en las consultas desconocidas que caen en la región de confusión.
    1. **Determinación de la Región de Confusión**:
       1. Se utiliza un conjunto $Q$ de consultas mal clasificadas en el conjunto de entrenamiento que caen dentro del margen del SVM
       2. La consulta en $Q$ con la distancia kernel mínima (más cercana al hiperplano, lado malicioso) determina el límite inferior de la región de confusión ($f_{\text{lower}}$)
       3. La consulta en $Q$ con la distancia kernel máxima (más cercana del hiperplano, lado normal) determina el límite superior de la región de confusión ($f_{\text{upper}}$)
       4. Para que exista esta región de confusión, el meta clasificador SVM debe ser un clasificador de margen suave (soft margin classifier)
    2. **K-Medoids Clustering **:
       1. Se aplica el algoritmo de K-Medoids Clustering a las consultas desconocidas que caen en la región de confusión
       2. El agrupamiento se realizar para preservar la distribución de densidad de los datos y reducir la redundancia, evitando el sesgo de muestreo que afecta a métodos como SVM AL
       3. Los centros de los clusters finales son las sospechas
  - _Contribución_: Las sospechas contribuyen más a la mejora del rendimiento de detección en comparación con los ejemplares
- **Exemplar Selection** (**ES**)
  - _Función_: Obtiene las consultas maliciosas más representativas (ejemplares)
  - _Ubicación_: Los ejemplares se encuentran en el lado malicioso (lado positivo) y lejos del hiperplano de separación
  - _Metodología_: ES utiliza el algoritmo Kernel Farthest-First (KFF), una heurística greedy, para elegir la consulta no etiquetada que está más lejos de todas las consultas maliciosas en el conjunto etiquetado actual
  - _Contribución_: Los ejemplares son más propicios para la obtención de consultas verdaderamente maliciosas

## Meta-Clasificador SVM

**Espacio de Características del Kernel**: SVM HYBRID opera en el espacio de características del kernel de SVM. Esto permite que la estrategia dependa de las posiciones de las consultas respecto al hiperplano y los vectores de soporte

**Distancia Kernel**: Tanto SS como ES utilizan la distancia kernel $f(x)$ o la distancia kernel entre muestras para tomar sus decisiones:

- **SS** utiliza la distancia kernel al hiperplano ($f(x)$) para definir la región de confusión
- **ES** utiliza la distancia kernel a las consultas maliciosas ya etiquetadas para encontrar el ejemplar más distante

**Soft Margin Classifier**: Para garantizar la existencia de la "región de confusión" utilizada por SS, el meta-clasificador SVM debe ser un clasificador de margen suave, lo que se logra ajustando el parámetro de penalización $C$ del SVM

## Training y Classification

El modelo de detección subyacente empleado es la **Generalización Apilada** (**Stacked Generalization** o **Stacking**), una técnica de clasificador de conjunto basada en Meta-Learning

- _Stacking_: Se basa en la idea de entrenar un meta-clasificador a partir de los resultados de predicción de los clasificadores base. Este enfoque tiene como objetivo inducir qué clasificadores base con fiables y cuáles no durante el entrenamiento. El uso de stacking es apropiado para la detección de consultas maliciosas debido a la naturaleza compleja, dinámica y confrontación de problemas, ya que le permite al sistema aprender de diferentes sesgos de aprendizaje (learning biases)
- _Estructura_: El modelo se compone de tres clasificadores base diferentes, elegidos de diferentes familias (para obtener diversidad de aprendizaje), y un meta-clasificador.
  - _Experimentos_: Random Forest, Logistic y MLP (Multi-Layer Perceptron)
- _Clasificador_: El SVM se utiliza como meta-clasificador para que SVM HYBRID pueda ejercer el modelo de detección para obtener consultas importantes
- _Proceso_: Durante la clasificación, una muestra de prueba es clasificada por cada clasificador base, y luego estas clasificaciones se introducen en el clasificador meta, que toma la decisión final. Las consultas importantes, tanto sospechas como ejemplares, se incorporan periódicamente al grupo de entrenamiento para actualizar el modelo de detección

## Data Collection y Preprocessing

El sistema utiliza registros de servidores web (en formato CLF) de un instituto académico como fuente de datos.

- _Data Collection_: Se recopilan consultas de solicitudes HTTP GET exitosas registradas en los logs. El conjunto de datos de evaluación se recopiló durante 10 días
- _Data Cleaning_:
  - Se examina los registros para recopilar solicitudes GET exitosas (código de retorno 200 a 299)
  - Se eliminan las solicitudes estáticas (por ejemplo, `.html`, `.jpg`)
  - Se extraen las consultas de las solicitudes GET restantes
- _Data Normalization_:
  - Se decodifican los caracteres ASCII imprimibles
  - Se realiza el proceso de un-escaping
  - Se transforma a minúsculas
  - Se eliminan las consultas cuya longitud sea inferior a cuatro caracteres
- _Character Filter_: Se propone un filtro de caracteres para eliminar las consultas consideradas maliciosas porque contiene caracteres inseguros definidos en RFC 2616, como caracteres de control ASCII (0-31, 127-255), DEL (127), SP(32), `"`, `#`, `%`, `<`, `>`
- _Feature Construction con N-Grams_:
  - Cada consulta se transforma en un vector de características numéricas utilizando $N$-grams
  - Los $N$-grams capturan la distribución de caracteres y las características de secuencia, lo que ayuda a distinguir las consultas maliciosas de las normales. El análisis es automático y no requiere conocimientos previos sobre la aplicación web objetivo ni sobre los ataques objetivo
  - Se elige $N=2$ para equilibrar el consumo computacional y el rendimiento de detección
    - Para $N > 2$, el número de $N-$grams aumenta exponencialmente con $N$. Debido al alto costo computacional para $N > 2$ ($N = 3 \to 63^3 \to 25.507$) se toma $N = 2$ para equilibrar el consumo computacional y el rendimiento de detección
  - Se aplica un modelo de $N$-gram basado en frecuencias, donde cada frecuencia de $N$-gram se divide por la frecuencia del $N$-gram que aparece con más frecuencia en esa misma consulta
- _Feature Reduction y Dimensionality Reduction_:
  - Primero se realiza la selección de características para eliminar los $N$-grams que no aparecen en todas las consultas e identificar los que son útiles para la clasificación
  - Después de la selección de características, se implementa la reducción de dimensionalidad para reducir la alta cantidad de características (alrededor de $1.000$ $N$-grams útiles) y mitigar la "maldición de la dimensionalidad", lo que mejora el rendimiento de la clasificación

**Observaciones**:

- Cuando se extraen las características $N$-grams ($N \geq 1$), el espacio de características de entrada del conjunto de consultas etiquetado se define como
  $$S = \left\{  N-\text{gram}_{i} | i = 1, \dots, 63^N \right\}$$
  donde el tamaño de $S$ es $63^N$ porque existe 63 caracteres únicos en todas las consultas después de la preparación de los datos

# Experimentos

**Experimento 1: Determinación de la Configuración Óptima de la Reducción de Características y Clasificadores Apilados (Stacked Classifiers)**: El objetivo de este experimento fue determinar la mejor combinación de métodos de selección y reducción de características, y la selección de clasificadores para el modelo de detección basada en stacking.

- Se utilizó un superconjunto de $100.100$ consultas y se implementó la validación: 10-fold-cross validation
- _Selección de Características_: Método de Ganancia de Información con las 800 mejores características se eligió como la configuración óptima
- _Reducción de Dimensionalidad_: Análisis de Componentes Principales (PCA) con 80 dimensionalidades reservadas fue la configuración óptima, ya que superó al conjunto completo de características
- _Selección de Clasificadores_: La mejor combinación de clasificadores fue Random Forest, Logistic y MLP, y el clasificador meta fue SVM con kernel RBF, con parámetros $C=0.05$ y $\gamma=2$

---

**Experimento 2: Evaluación de AMODS y SVM HYBRID (Caso Óptimo C)**: Este experimento evaluó la eficacia de SVM HYBRID, específicamente el impacto de ajustar $\theta$ (razón del tamaño del subconjunto de consultas para SS respecto ES)

- Se examinaron 5 casos (**A-E**) con diferentes valores de $\theta$, siendo $C$ el que utilizó $\theta$ de $7:3$. El número fijo de consultas importantes obtenidas cada día (M) se fijó en 150
- _Desarrollo del Caso C_: El subconjunto de consultas desconocidas para SS es de $7.000$ y para ES es de $3.000$. A lo largo de los 10 días de detección, el número de sospechas (suspicions) disminuye mientras que el número de ejemplares (exemplars) aumenta, lo que refleja que ES se vuelve cada vez más dominante
- _Resultados y Optimización del Caso C_: Logró el F-value más alto ($94.79\%$) en el último día. También obtuvo la tasa de verdaderos positivos más alta y la tasa de falsos positivos más baja, $98.91\%$ y $0.09\%$ respectivamente, entre todos los casos probados en el 10mo día
- _Caso Óptimo_: $C$ es elegido como porque, además de un rendimiento de detección deseable, obtuvo el mayor número total de consultas maliciosas a lo largo de los 10 días. Esto confirma que las sospechas ayudan a mejorar tanto la capacidad de detección como el número de ejemplares clasificados correctamente. La superioridad del Caso C se atribuyó a que obtuvo el mayor número total de sospechas mal clasificadas, las cuales son más informativas y contribuyen a un límite de decisión más preciso del modelo de detección

---

**Experimento 3: Comparaciones de Modelos Constantes y Modelos Adaptativos**: Este experimento comparó AMODS (Caso C) con modelos constantes (SVM constante y stacking constante) y otros modelos adaptativos (SVM AL, SS, ES, SVM adaptativo y selección aleatoria). AMODS superó a todos los demás métodos en ambos aspectos: la mejora del rendimiento y la obtención de más consultas maliciosas. Este experimento mostró que las consultas maliciosas obtenidas por AMODS ($715$) fue $2.78$ veces mayor que el obtenido por SVM AL ($257$). Se construyó que el aprendizaje adaptativo puede mejorar el rendimiento de detección de consultas maliciosas en comparación con los modelos constantes

---

**Experimento 4: Comparaciones con Trabajos Relacionados**: Este experimento comparó AMODS con métodos de detección de ataques web existentes que son constantes (Combinación Lineal, Transformada Wavelet y Reducción de Dimensionalidad), utilizando el mismo conjunto de datos. AMODS resultó ser el ganador general, superando significativamente a los otros métodos en métricas como F-value, TPR y FPR

# Consideraciones del Documento

- Las consultas web son a través de solicitudes HTTP GET
- Las cadenas de solicitud es una consulta que el sistema examina y se puede identificar con un carácter `?` que sigue al recurso al que se hace referencia y enumera partes de nombres y valores de parámetros
- _Enfoques de WAF_: Detección basadas en Firmas y Detección basada en Anomalías
- _Limitaciones de WAF basados en Firmas_:
  - Ineficiencia contra Amenazas Emergentes como Zero-Day Attack
  - Altas tasas de Falsos Positivos (False Positive Rate)
- _Métodos de Detección Adaptativos_: Diseñados para intrusiones en la red y no aplicables a ataques web $\to$ Solución: mantener el modelo de detección de ataques web constantemente actualizado es incorporar las consultas importantes más recientes, incluidas consultas informativas benignas y consultas maliciosas representativas
