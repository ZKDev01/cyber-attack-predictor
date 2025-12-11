# Resumen

ModSecurity es un reconocido WAF de open-source, mantenido por la fundación OWASP. Es capaz de detectar solicitudes maliciosas comparándolas con el conjunto de reglas básica (CRS), identificando patrones de ataque conocidos. A cada regla se le asigna manualmente un peso según la gravedad del ataque correspondiente y se bloquea una solicitud si la suma de los pesos de las reglas coincidentes excede un umbral determinado. Sin embargo, esta estrategia es ineficaz contra los ataques web, ya que la detección se basa únicamente en heurísticas.

**Propuesta**: ModSec-Learn es un modelo que toma como características de entrada las reglas CRS y ajusta la contribución de cada regla CRS a las predicciones, adaptando así el nivel de gravedad a las aplicaciones web a proteger. Este enfoque logra un equilibrio significativo entre detección y tasas de falsos positivos.

**Observaciones**:

- A pesar de que el modelo de prueba esta centrado en reglas dirigidas a ataques SQLi, esta representación de características se puede aplicar a cualquier regla dentro del CRS.

# Insights

- **Fallo del Modelo Heurístico Tradicional**: ModSecurity, que utiliza el Core Rule Set (CRS), es capaz ineficaz contra los ataques web porque su detección se basa en heurísticas y no se adapta a la aplicación web específica que debe proteger. Sus tres principales deficientes son: la severidad de las reglas es puramente heurística; no considera el tráfico legítimo, lo que puede causar altas tasas de falsos positivos (FPR); y las reglas pueden ser redundantes o interferir entre sí
- **Adaptación mediante ML**: El modelo ModSec-Learn supera estas limitaciones al usar las reglas CRS como características de entrada para un modelo de ML. El entrenamiento permite que el modelo ajuste la contribución (peso) de cada regla CRS de manera óptima, adaptando así de nivel de severidad al comportamiento de los servicios web a proteger
- **Sustitución de Puntuación Heurística**: El entrenamiento permite que el modelo sintonice la relevancia de cada regla. La puntuación de severidad heurística de cada regla es sustituida por el peso que el modelo de ML le atribuye. Esto permite al sistema adaptarse a los servicios web que protege
- **Mejora de Rendimiento Drástica**: Los experimentos demostraron que ModSec-Learn logra un mejor trade-off entre la masa de detección y la tasa de falsos positivos. ModSec-Learn mejora la tasa de verdaderos positivos (TPR) en más del $45\%$ en comparación con el ModSecurity estándar a una tasa de falsos positivos (FPR) del $1\%$
- **Reducción de Reglas** (**Sparsity**): El uso de la regularización dispersa ($\mathcal{l}1$) permite una selección automática de características (reglas). Este enfoque demostró que se puede descartar más del $30\%$ de las reglas CRS (18 de las 60 reglas de SQLi examinadas) porque el modelo les asignó una relevancia nula o peso de 0 sin afectar el rendimiento. Esto proporciona un método menos arbitrario para seleccionar reglas de seguridad
- **Modelos y Entrenamiento**: Modelos lineales como SVM y Regresión Logística; Modelos No-Lineales como Random Forest. El modelo elegido se entrena en un conjunto de datos equilibrado que incluye tanto muestras legítimas (tráfico real) como una amplia colección de payloads de ataque (como SQLi)

# Limitaciones

**Limitaciones del Algoritmo de Detección de ModSecurity**:

- La severidad de cada regla es puramente heurística y podría no reflejar el comportamiento real de la red a proteger
- Las reglas solo apuntan a patrones de ataque, pero no tienen en cuenta el tráfico de red legítimo, lo que potencialmente genera una alta tasa de falsos positivos
- Diferentes reglas podrían interferir entre sí o ser redundantes

> El documento se enfoca únicamente en las ventajas que posee ModSec-Learn, no en la limitaciones

# Análisis de ModSecurity

**ModSecurity**: Solución WAF open-source establecida que construye su defensa sobre firmas de ataques bien conocidas, recopilados por OWASP y conocidos como Core Rule Set (CRS). El funcionamiento de este WAF es: se tiene un dataset de reglas (CRS) y cada una de estas reglas se les asigna un nivel de gravedad heurístico que se utiliza para evaluar si una solicitud HTTP es maliciosa o no. Por lo tanto, la detección se logra mediante la suma de las puntuaciones de las reglas coincidentes, bloqueando la solicitud entrante si se excede un umbral.

# Definiciones y Antecedentes

**Reglas de Detección**: Diseñados para detectar tipos específicos de ataque web. Cada regla se indica mediante un identificador único que representa la clase específica de ataque que pretende identificar. Las reglas también están asociadas con dos parámetros notables: Nivel de Paranoia (PL, Paranoia Level) y Nivel de Gravedad

**Paranoia Level**: Se utiliza para seleccionar qué reglas están habilitadas para analizar las solicitudes HTTP. El CRS incluye 4 PL y cada regla está asignada a un PL específico. Además, las reglas se agrupan por PL de forma anidada: establecer un determinado PL habilita todas las reglas asignadas a ese PL, así como aquellas asignadas a PL inferiores.

**Puntuación de Anomalías**: A cada regla de detección se le asigna heurísticamente un nivel de gravedad, un valor entero positivo que cuantifica qué tan amenazante es una solicitud capturada. Para calcular una decisión, ModSecurity aplica las reglas a las solicitudes entrantes y suma todos los niveles de gravedad de todas las coincidencias. Si dicha suma supera un umbral, la solicitud entrante se marca como maliciosa. En CRS existen 4 niveles de gravedad: crítico (5), error (4), advertencia (3) y aviso (2)

# Mejora de ModSecurity con ML

ModSec-Learn se construye sobre dos componentes principales:

1. Una fase de extracción de características que codifica las reglas CRS en una representación vectorial
2. Un modelo de ML que aprende cómo combinar de manera óptima las reglas CRS.

**Objetivo**: Superar la deficiencia de ajustar manualmente los niveles de gravedad manteniendo al mismo tiempo el poder predictivo de las reglas CRS.

---

Se entrena un modelo de ML utilizando las reglas CRS como input features (52 features) para mejorar el equilibrio entre la tasa de detección y los falsos positivos. Esto equivale a aprender un modelo de tráfico entrante dirigido a los servicios web protegidos. La regularización dispersa también se puede utilizar para seleccionar un subconjunto de las reglas disponibles, en lugar de utilizar PL.

---

**Reglas de Detección como Features**: El espacio de entrada está representado por consultas SQL que un modelo de ML clasifica como maliciosas o benignas. Cada consulta SQL es una cadena de caracteres legibles, representada como $z \in Z$, siendo $Z$ el espacio de todos las consultas posibles. Sea $D$ el conjunto de reglas SQLi seleccionadas de CRS y $d = |D|$ su cardinalidad. Denotamos con $\phi : Z \to X$ una función que asigna una consulta SQL $z$ a un vector de características de dimensión $d$, $x = (x_{1},\dots,x_{d}) \in X = \{ 0,1 \}^d$, donde cada característica se establece en 1 si la regla SQLi correspondiente ha sido activada por la consulta SQL $z$, y 0 en caso contrario.

---

**Combinación Óptima de Reglas CRS con ML**: Entrenamiento de 3 modelos de ML diferentes en el conjunto de funciones: SVM (modelo lineal), Regresión Logística (modelo lineal) y Random Forest (modelo no-lineal). El objetivo es crear un conjunto de datos novedosos que consista en muestras legítimas basadas en el tráfico del mundo real, así como un conjunto completo de cargas útiles de SQLi

# Pasos para Construir ModSec-Learn

La arquitectura de ModSec-Learn se basa en dos componentes principales: Fase de Extracción de Características y Fase de Aprendizaje del Modelo.

1. **Recopilación y Preparación del Conjunto de Datos**: El modelo debe entrenarse con un conjunto de datos balanceado que representa tanto el tráfico legítimo como los ataques web
   1. _Recolección de Muestras Legítimas_. Obtener muestras legítimas basadas en tráfico real
   2. _Recolección de Muestras Maliciosas_ (_Ataques_): Crear un conjunto integral de payloads de ataque (por ejemplo, SQLi). Esto incluye aumentar conjuntos de datos existentes y utilizar herramientas de prueba como SQLmap para generar nuevos payloads ofuscados
   3. _Balance del Conjunto de Datos_: Es fundamental crear un conjunto de datos balanceado. En el estudio, se seleccionaron $25.000$ muestras benignas y $25.000$ muestras maliciosas (SQLi)
   4. _División de Datos_: Dividir el conjunto de datos balanceado en un conjunto de entrenamiento (train) (ej: $40.000$ muestras balanceadas) y un conjunto de prueba (test) (ej: $10.000$ muestras balanceadas)
2. **Extracción y Codificación de Características** (**Reglas CRS**): Esta fase codifica las reglas del CRS en una representación vectorial que el modelo de ML puede utilizar
   1. _Definición de Características_: Las reglas CRS (por ejemplo, las 60 reglas de SQLi o el subconjunto activo, como las 52 utilizadas en el estudio) se utilizan como el espacio de características de entrada
   2. _Mapeo Funcional_ ($\phi$): Se define una función $\phi$ que mapea cada consulta SQL ($z$) a un vector de características $x$ de $d$ dimensiones (donde $d$ es el número de reglas utilizadas)
   3. _Codificación Binaria_: Cada característica ($x_{i}$) se establece en 1 si la regla CRS correspondiente ha sido activada por la solicitud y en 0 en caso contrario.
3. **Selección y Entrenamiento del Modelo de Machine Learning**: El modelo de ML se entrena para aprender la combinación óptima de las reglas CRS.
   1. _Selección del Modelo_: Elegir un modelo de ML que permita asignar pesos directamente a las reglas
   2. _Aplicación de Regularización_ ($\mathcal{l}1$ y $\mathcal{l}2$): Aplicar términos de penalización. La norma $\mathcal{l}1$ (regularización dispersa) es especialmente importante, ya que impone dispersión (sparsity) el modelo, asignando pesos de cero a las reglas irrelevantes, lo que permite la selección automática de un subconjunto óptimo de reglas
   3. _Optimización de Hiperparámetros_: Ajustar el parámetro de regularización $C$ y otros hiperparámetros. En el estudio, se encontró que un valor de $C = 5 \cdot 10^{-1}$ era óptimo para SVM y LR
4. **Evaluación**:
   1. _Evaluación del Rendimiento_: Evaluar el modelo entrenado con el conjunto de prueba, utilizando métricas como la curva ROC para medir el trade-off entre la Tasa de Verdaderos Positivos (TPR) y la Tasa de Falsos Positivos (FPR)
   2. _Sustitución de la Puntuación_: Una vez entrenado, los pesos aprendidos por el modelo reemplazan las puntuaciones de severidad heurísticas manuales de ModSecurity
