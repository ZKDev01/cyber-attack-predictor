**Nombre Completo**: Adaptive Dual-Layer Web Application Firewall (ADL-WAF) Leveraging Machine Learning for Enhanced Anomaly and Threat Detection

# Insights

**Limitaciones de WAF Tradicionales**: Muchos modelos tradicionales se basan en la inspección y el control del tráfico HTTP, utilizando Application Learning (AL) para aprender el comportamiento normal e identificar lo sospecho, pero poseen deficiencias significativas:

- Ineficiencia contra amenazas emergentes
- Altas tasas de falsos positivos
- Proceso de Fine-Tuning consumen mucho tiempo
- Naturaleza estática que limita su respuesta a los cambios en las amenazas y el comportamiento de las aplicaciones
- Inexactos: las fluctuaciones en el tráfico legítimo pueden ser reconocidas como amenazas, mientras que las amenazas pueden considerarse benignas
  - Distinguir efectivamente entre tráfico malicioso y legítimo $\to$ Necesidad de que la seguridad de las aplicaciones web sea más dinámica y auto-consciente

**ADL-WAF** (**Adaptive Dual-Layer Web Application Firewall**): Decision Tree (DT) $+$ Support Vector Machines (SVM)

- Integración de Técnicas de ML en un enfoque de doble capa puede mejorar sustancialmente la seguridad de las aplicaciones web al proporcionar una detección de amenazas más precisa y eficiente
- Solución a Limitaciones de WAF Tradicionales:
  - Capa de Detección de Anomalías: DT para identificar desviaciones del patrón normal en el tráfico web entrante, utilizando funciones extraídas de solicitudes HTTP.
    - (Feature Selection/Extraction) Diseño de Características Primarias a través de Solicitudes HTTP (como Método, URL, cuerpo y encabezados): Relación de Caracteres Alfanuméricos, Relación de Palabras Malas (Badwords Ratio), Relación de Caracteres Especiales, Relación de Caracteres Especiales Ilegales. Estas permiten reflejar la presencia de patrones típicos del tráfico anormal
  - Capa de Detección de Amenazas: SVM para clasificar esas anomalías como amenazas benignas (errores tipográficos)
    - Vectorización TF-IDF para obtener vectores de características numéricas, permitiendo la detección de ataques conocidos basados en texto como SQLi y XSS, utilizando tokenización y análisis $N$-grams
- Supera a los WAF tradicionales: reduce los falsos positivos y mejora la tasa de detección
- Este marco de ML de Dual-Layer puede aliviar la carga de trabajo de los equipos de seguridad, lo que resulta en una protección más eficiente de las aplicaciones web
- _Lógica de Decisión por Capa_: siendo $L_{1}$ y $L_{2}$ las capas de detección de anomalías y detección de amenazas respectivamente:
  - $L_1 = 0$: Tráfico normal
  - $L_{1} = 1$ y $L_{2} = 0$: Anomalía, pero NO Ataque
  - $L_{1} = 1$ y $L_{2} = 1$: Anomalía y Ataque

**Evaluación**: Comprobación con 5 Datasets y se logró una Precisión de Detección del $99.88\%$ y Precisión del $100\%$ $\to$ Mejora significativa en la detección de anomalías y la reducción de falsos positivos

**Datasets**: XSS, ECML, CSIC2010, HTTPParams, Hybrid Dataset; donde:

- **Capa 1** $+$ **Capa 2**: HTTPParams, CSIC2010, Hybrid Dataset
- **Only Capa 1 (Capa de Detección de Anomalías)**: CSIC2010, HTTPParams
- **Only Capa 2 (Capa de Detección de Amenazas)**: HTTPParams, ECML, XSS

**Desafíos Futuros**:

- Problemas al identificar ataques que imitan solicitudes normales, como DoS y Fuerza Bruta $\to$ Desarrollo de Conjuntos de Datos Especializados y a gran escala durante períodos prolongados
- Explorar la integración de Reinforcement Learning para permitir que el modelo se adapte basándose en la retroalimentación en tiempo real, mejorando su dinamismo y precisión en aplicaciones online
- Optimizar el rendimiento del modelo para asegurar que pueda procesar el tráfico entrante en tiempo real sin introducir latencia significativa
- Adaptabilidad del modelo para aplicaciones web con características dinámicas

# Feature Engineering

## Capa de Detección de Anomalías

Características que extrae el modelo para calcular métricas específicas según las cuales clasifica el modelo:

- **Alphanumeric Character Ratio**: Característica que cuenta la proporción de caracteres alfanuméricos en una carga útil. Las solicitudes regulares tienen una mayor proporción de caracteres numéricos y alfabéticos en comparación con los símbolos especiales. Como resultado, esta característica tiende a tener más valor en solicitudes normales que en las de un ataque
- **Badwords Ratio**: Representa la relación entre el número de malas palabras (términos comúnmente utilizados como partes de consultas de ataque) y la longitud de los caracteres alfanuméricos. Las consultas normales no tienen malas palabras, pero las solicitudes anómalas suelen tener una proporción mayor
- **Special Character Ratio**: Característica que cuantifica la proporción de caracteres especiales (no alfanuméricos) con respecto a la longitud total de entrada. A menudo, las solicitudes anómalas tienen más caracteres especiales, como símbolos, numéricos y alfabéticos. Por tanto, esta propiedad tendrá un valor superior en solicitudes anómalas a lo normal
- **Illegal Special Character Ratio**: Característica que representa la proporción de caracteres especiales ilegales con respecto al número total de caracteres especiales en la carga útil. Las solicitudes normales tienen una proporción baja o ausencia de caracteres especiales ilegales, mientras que las solicitudes anómalas exhiben una proporción más alta

## Capa de Detección de Amenazas

Verifica si la anomalía detectada en la capa de detección de anomalías es una amenaza real o simplemente benigna. Para lograr esto: **Técnica de Vectorización TF-IDF** para obtener el vector de características numéricas que alimenta el lugar donde la capa de detección de amenazas hace su trabajo al identificar posibles amenazas

# Preprocessing Datasets

## Capa de Detección de Anomalías

1. _Decodificación_: Decodificar los datos codificados y limpiarlos eliminado valores faltantes, duplicados y valores atípicos para garantizar la integridad de los datos
2. _Feature Extraction_: Se extraen de las solicitudes HTTP entrantes las siguientes características: método HTTP, URL, carga y headers
3. _Feature Selection_: Se busca determinar y retener solo los features relevantes para el modelo
4. _Reducción de Dimensionalidad_: Refine el conjunto de datos para incluir solo características relevantes
5. _Equilibrio del Dataset_: Se equilibra el dataset para garantizar una distribución equitativa de muestras normales y anómalas, lo cual es crucial para la precisión y eficiencia del modelo

_Observaciones para la Implementación y Mejora_:

- Al eliminar valores atípicos es posible que se elimine información valiosa para la detección

## Capa de Detección de Amenazas

1. _Conversión del Dataset_: Se tiene la información de formato CSV a JSON, haciéndolo compatible con el algoritmo de ML empleado
2. _Integración de Datasets_: Combinación de los datasets en un solo archivo. Se puede realizar una mezcla aleatoria para aumentar la diversidad
3. _Limpieza de Datos_: Se busca eliminar los valores faltantes, duplicados y valores atípicos, lo que garantizaría la calidad del dataset
4. _Vectorización de Datos_: Los datos de texto sin formato se convierten en vectores de características numéricos
5. _Preprocesamiento de Características Numéricas_: Se busca que estas características sean compatibles como entrada para los modelos de ML.

_Observaciones para la Implementación y Mejora_:

-

# Independent Dual-Layer Training

**Evaluation Metrics**: Precision, Recall, Accuracy, referente a Detection Rate, False Positive Rate y Decision Rate. Métricas de conceptos específicos de True Positive, False Positive, True Negative y False Negative.

## Capa de Detección de Anomalías

- **Datasets**: CSIC2010, HTTPParams
- **Modelo**: Decision Tree mediante dos metodologías:
  1.  División Train-Test 80-20
  2.  Cross-Validation 100 veces
- **Técnica de Mitigación de Overfitting y Mejora de Generalización del Modelo**: Las filas de datos se mezclan durante el entrenamiento

## Capa de Detección de Amenazas

- **Datasets**: HTTPParams, ECML, XSS
  - Se aplicó una Síntesis sobre Datasets (Integración de Datasets)
- **Modelo**: SVM vectorizado utilizando TF-IDF
- **Técnica de Validación**: Grid-Search con Cross-Validation para encontrar la mejor configuración de hiperparámetros que produciría un mejor rendimiento para el modelo

# Experimentos y Resultados Finales

**Experimentos en Implementación-Evaluación por Capa**: Decision Tree y Naive Bayes para detección de anomalías y SVM para la detección de amenazas

- _Capa de Detección de Anomalías_: Decision Tree muestra mejores resultados en la puntuación de precisión utilizando la División Train-Test y k-folds junto con una tasa alta de sensibilidad y una baja tasa de False Positive.
- _Capa de Detección de Amenazas_: SVM con parámetros $\to$ Rangos de n-grams de $(1,1), (1,2), (1,4)$, así como kernels RBF y lineales, con valor de regularización $C$ de 10 $\to$ Mejores resultados: Kernel RBF con N-Grams de (1,4)

**Resultados de Combinación**:

- Se logró 0 False Positive con ADL-WAF, comparándose con la Capa 1 de Detección de Anomalías (Anomaly Detection Layer)
- Constante entre True Positive y True Negative en Anomaly Detection Layer y ADL-WAF, $22.625$ y $7.835$ respectivamente en cada métrica
- Anomaly Detection Layer obtuvo 1 en False Negative y 51 tuvo ADL-WAF

**Resultados por Datasets**:

| Dataset           | Precision | Recall |
| ----------------- | --------- | ------ |
| Command Injection | 0.99      | 0.98   |
| Path-Traversal    | 1.0       | 0.97   |
| SQLi              | 1.0       | 0.99   |
| Valid             | 1.0       | 1.0    |
| XSS               | 1.0       | 1.0    |

_Observaciones_:

- La integración de SVM con TF-IDF en la Segunda Capa proporciona efectividad y adaptabilidad al modelo $\to$ Reduce los Falsos Positivos y Aumenta la precisión debido a su alta capacidad para detectar ataques basados en texto-numéricos en Web Apps.

# Tablas de Ejemplo

**Vector de Características Numéricas para el Conjunto de Datos Tokenizados utilizando la técnica TF-IDF**

| Before Tokenization                      | After N-gram Tokenization                           | Vector (Simplified)                 | Label  |
| ---------------------------------------- | --------------------------------------------------- | ----------------------------------- | ------ |
| `<script>alert('XSS')</script>`          | `[<, script, alert, (, 'XSS', ), </, <script, ...]` | `[0.176, 0.477, 0.176, ..., 0.176]` | XSS    |
| `SELECT * FROM users WHERE id=1 OR 1=1;` | `[SELECT, *, FROM, users, WHERE, id=1, ...]`        | `[0.477, 0.477, 0.477, ..., 0.477]` | SQLi   |
| `GET /index.html HTTP/1.1`               | `["GET", "ET /", ..., "/1.1"]`                      | `[0.0, 0.0, 0.0, ..., 0.0]`         | Normal |
