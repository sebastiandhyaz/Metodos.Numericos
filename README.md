DOCUMENTO DE CONTEXTO TEORICO Y EXPLICATIVO DEL PROYECTO
PROYECTO: Modelado y Resolución de Sistemas Lineales Complejos 
TEMA: Sincronización de Semáforos en una Red Vial Urbana
MATERIA: Métodos Numéricos (UMSA 2026)

Este documento es un resumen completo en texto plano diseñado para ser procesado por una inteligencia artificial (como Claude) para la generación de un PDF, informe o reporte académico detallado. Contiene todo el marco teórico, desarrollo, análisis de resultados y justificación de los componentes del proyecto.

1. INTRODUCCION Y PLANTEAMIENTO DEL PROBLEMA
El proyecto resuelve la problemática de tráfico vehicular en una red de tres intersecciones críticas mediante el modelamiento matemático de ecuaciones lineales. El objetivo es encontrar el sistema de sincronización óptima, donde las variables representan el tiempo de luz verde (en segundos) que cada semáforo debe asignar para evacuar el volumen de tránsito sin generar colas infinitas.

Variables:
x1 = Tiempo de luz verde en la Intersección 1
x2 = Tiempo de luz verde en la Intersección 2
x3 = Tiempo de luz verde en la Intersección 3

Ecuación fundamental: Ax = b
Donde "A" es la matriz de pesos de influencia vehicular (cómo afecta el flujo de una calle a las adyacentes), "x" es el vector de tiempos a calcular, y "b" es la demanda de vehículos por minuto que ingresan y deben ser satisfechos en cada nodo.

2. ESCENARIOS ESTUDIADOS
Se plantearon rigurosamente tres escenarios para poner a prueba los solucionadores numéricos:

Caso 1: Ideal (Flujo Normal)
A = [[4, 1, 0], [1, 3, 1], [0, 1, 4]], b = [15, 18, 14]
Representa un día normal sin accidentes. La matriz es estrictamente diagonal dominante. Esto significa que cada semáforo gobierna fuertemente su propia esquina sin mucha inferencia destructiva del resto de la red. Converge fácil.

Caso 2: Bajo Estrés (Hora Pico)
A = [[40, 10, 0], [10, 35, 10], [0, 10, 40]], b = [150, 200, 140]
Representa una alta congestión. La demanda se dispara 10 veces. Sin embargo, matemáticamente se demuestra que al mantenerse la dominancia diagonal escalada, el sistema tiene solución estable. La proporción de tiempos requeridos es conservada.

Caso 3: Mal Condicionado (Colapso y Caos Geométrico)
A = [[4.000, 1.000, 1.000], [1.000, 4.000, 1.001], [1.000, 1.001, 4.000]], b = [10, 10, 10]
Es un escenario degenerado. Los conductores y flujos compiten por vías prácticamente superpuestas (hiperplanos casi paralelos). Un milisegundo de error genera divergencia total. Es la prueba de fuego geométrica donde fallan los métodos iterativos tradicionales.

3. METODOS MATEMATICOS EMPLEADOS Y MARCO TEORICO
Para resolver el sistema, analizamos múltiples heurísticas, iterativas y directas:

3.1. Métodos Directos: LU y Factorización de Cholesky
Descomponen la matriz del sistema en partes triangulares superiores e inferiores para hacer sustituciones rápidas hacia atrás y adelante. Producen la solución exacta (x1, x2, x3) en un tiempo predecible, pero para matrices masivas de tráfico con millones de cruces en toda una ciudad, saturan la memoria del servidor. Cholesky requiere estrictamente simetría y ser definida positiva.

3.2. Método de Jacobi
Es un método iterativo básico que despeja cada variable y asume que todas las demás se mantienen fijas en su valor anterior. Computa en paralelo. En el Caso Ideal y de Estrés tardó unas 25 iteraciones. En el Caso Mal Condicionado, aunque teóricamente convergente, en la práctica computacional oscila y fracasa ante el mal condicionamiento.

3.3. Método de Gauss-Seidel
Mejora de Jacobi. Usa la actualización más reciente de los semáforos contiguos en el mismo barrido iterativo. Por esto, su tasa de convergencia suele ser el doble de rápida. Tardó ~12 iteraciones en los casos favorables. Falla en el caso 3.

3.4. Sobrerelajación Sucesiva (SOR)
Se le inyecta un parámetro "omega" (ω) multiplicador para que prevea la dirección de convergencia y acelere el salto. Con un ω=1.25 para el Caso Ideal, convergimos en solo 9 iteraciones. Para el caso malo se intentó ser conservador con ω=1.05.

3.5. Gradiente Conjugado Precondicionado (PCG)
Método de subespacios de Krylov. Trata el problema de las calles como un problema geométrico de optimización buscando el valle más profundo a lo largo de vectores ortogonales mutuos. Al aplicarle un precondicionador diagonal, logramos resolver el sistema en su máximo esplendor, encontrando el punto exacto en la red en solamente 3 pasos repetitivos e infalibles.

3.6. Extensiones a Multiplicadores de Lagrange
Se incluyó teóricamente este modelado. Si nuestro ciclo de semaforización debe durar obligatoriamente, por ejemplo, 120 segundos en total (x1 + x2 + x3 = 120), el problema ya no es un simple sistema lineal, sino uno de Optimización con Restricciones. A través de los Multiplicadores de Lagrange, añadiríamos la restricción ecuacional penalizando la matriz de costos y obteniendo una nueva matriz extendida.

4. ASPECTO TECNICO Y HERRAMIENTAS
El ecosistema consta de:
- Un motor en Python (Numpy/Scipy) 'solver.py' que compila todos los casos de manera matricial dura y exporta un 'results.json'.
- Una interfaz web Frontend (index.html) sin servidores que actúa como simulador didáctico de bolsillo de tráfico, incluyendo una implementación manual en Vanilla JavaScript de los solvers (Jacobi, GS, PCG) construidos desde cero.

Este compendio de información está listo para que Claude o cualquier otro LLM pueda expandirlo, parafrasearlo a formato formal de paper, construir tablas de contenidos e imprimir un PDF final de reporte sin perder contexto técnico de Métodos Numéricos.
