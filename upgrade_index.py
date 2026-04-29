import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove Three.js CDNs
text = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/three\.js/r128/three\.min\.js"></script>\n\s*<script src="https://cdn\.jsdelivr\.net/npm/three@0\.128\.0/examples/js/controls/OrbitControls\.js"></script>', '', text)

# 2. Replace the 3D card with Theoretical Framework including Lagrange
theory_html = """
        <div class="card">
            <h2>Glosario y Marco Teórico de Métodos</h2>
            <div class="interpretation" style="font-size: 0.95rem; overflow-y: auto; height: 400px; padding-right: 15px;">
                <p><span>1. Métodos Directos (LU, Cholesky)</span><br>Descomponen la estructura vial original en matrices triangulares. Proveen solución exacta en un paso, pero son muy ineficientes en demanda de memoria para redes de tráfico masivas.</p>
                <p><span>2. Jacobi y Gauss-Seidel</span><br>Algoritmos iterativos base. <strong>Jacobi</strong> calcula los nuevos tiempos asumiendo el estado previo congelado. <strong>Gauss-Seidel</strong> usa la información más reciente de semáforos adyacentes casi al instante, lo que duplica su velocidad de convergencia en sistemas diagonalmente dominantes (tráfico normal).</p>
                <p><span>3. SOR (Sobrerelajación Sucesiva)</span><br>Acelera a Gauss-Seidel al extrapolar ("sobre-relajar") el vector de solución mediante un factor <i>ω</i>. En nuestro caso, ω=1.25 resulta óptimo para predecir colas de autos antes de que se formen.</p>
                <p><span>4. Gradiente Conjugado Precondicionado (PCG)</span><br>Una técnica magistral de Krylov. Visualiza el problema no como ecuaciones, sino como la búsqueda de la base de un "tazón" n-dimensional. El precondicionador alisa matemáticamente el terreno, resolviendo hasta los peores cuellos de botella en apenas ~3 saltos.</p>
                <p><span>5. Extensiones (Multiplicadores de Lagrange)</span><br>Para un modelo más real, si el "Ciclo Semafórico Total" está restringido rígidamente (ej. $x_1 + x_2 + x_3 = 120s$), el sistema pasaría a ser de Optimización Restringida y se resolvería usando <strong>Multiplicadores de Lagrange</strong> o métodos de Penalización, expandiendo la matriz a variables del sistema dual.</p>
            </div>
        </div>
"""

# Regex to safely find and replace the 3D card
text = re.sub(r'<div class="card">\s*<h2>Visualización Espacial \(3D\)</h2>.*?<div id="3d-container"></div>\s*</div>', theory_html.strip(), text, flags=re.DOTALL)

# 3. Remove 3D init and update calls
text = text.replace('init3D();\n', '')
text = text.replace('update3D(sc);\n', '')

# 4. Remove all Three.js code at the bottom
three_js_start = text.find('// THREE JS')
three_js_end = text.find('window.onload = init;')

if three_js_start != -1 and three_js_end != -1:
    text = text[:three_js_start] + text[three_js_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

