import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix init sequence so init3D is called before updateChart
init_old = """            buildTable();
            loadScenario('ideal');
            updateChart();
            init3D();"""

init_new = """            buildTable();
            loadScenario('ideal');
            init3D();
            updateChart();"""
content = content.replace(init_old, init_new)


# 2. Add full robust grid system for the calculator instead of flex rows
style_old = """.matrix-row {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 15px;
        }

        .matrix-row input {
            width: 70px;
            text-align: center;
            font-size: 1.1rem;
        }
        
        .matrix-row span {
            font-weight: bold;
            width: 50px;
            text-align: center;
            color: var(--neon-secondary);
        }"""

style_new = """.matrix-grid {
            display: grid;
            grid-template-columns: minmax(50px, 80px) minmax(50px, 80px) minmax(50px, 80px) 40px minmax(50px, 80px);
            gap: 10px;
            justify-content: center;
            align-items: center;
        }

        .matrix-grid input {
            width: 100%;
            text-align: center;
            font-size: 1.1rem;
            padding: 8px 0;
            box-sizing: border-box;
        }
        
        .matrix-grid span {
            font-weight: bold;
            text-align: center;
            color: var(--neon-secondary);
            font-size: 1.2rem;
        }"""

content = content.replace(style_old, style_new)

# 3. Replace the matrix div container to use the new grid
html_old = """            <div class="matrix-container" style="background: rgba(0,0,0,0.5); padding: 20px; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 15px;">
                <div class="matrix-row">
                    <input type="number" id="A00" step="any"> <input type="number" id="A01" step="any"> <input type="number" id="A02" step="any"> <span>x₁ =</span> <input type="number" id="b0" step="any">
                </div>
                <div class="matrix-row">
                    <input type="number" id="A10" step="any"> <input type="number" id="A11" step="any"> <input type="number" id="A12" step="any"> <span>x₂ =</span> <input type="number" id="b1" step="any">
                </div>
                <div class="matrix-row">
                    <input type="number" id="A20" step="any"> <input type="number" id="A21" step="any"> <input type="number" id="A22" step="any"> <span>x₃ =</span> <input type="number" id="b2" step="any">
                </div>
            </div>"""

html_new = """            <div class="matrix-container" style="background: rgba(0,0,0,0.5); padding: 20px; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 15px;">
                <div class="matrix-grid">
                    <input type="number" id="A00" step="any"> <input type="number" id="A01" step="any"> <input type="number" id="A02" step="any"> <span>x₁ =</span> <input type="number" id="b0" step="any">
                    
                    <input type="number" id="A10" step="any"> <input type="number" id="A11" step="any"> <input type="number" id="A12" step="any"> <span>x₂ =</span> <input type="number" id="b1" step="any">
                    
                    <input type="number" id="A20" step="any"> <input type="number" id="A21" step="any"> <input type="number" id="A22" step="any"> <span>x₃ =</span> <input type="number" id="b2" step="any">
                </div>
            </div>"""

content = content.replace(html_old, html_new)

# 4. Enlarge Interpretation text
interp_old = """function updateInterpretation(sc) {
            let exact = resultData.casos[sc].solucion_exacta;
            let text = "";
            if (sc === 'ideal') {
                text = `En el Caso Ideal, bajo condiciones normales, la sincronización óptima indica que el semáforo 1 debe tener <span>${exact[0].toFixed(2)}</span>s, el semáforo 2 <span>${exact[1].toFixed(2)}</span>s y el semáforo 3 <span>${exact[2].toFixed(2)}</span>s. El sistema fluye sin retenciones significativas.`;
            } else if (sc === 'estres') {
                text = `Bajo Estrés (hora pico), la demanda se multiplica por 10. Curiosamente, la proporción de tiempo requerida es similar: <span>${exact[0].toFixed(2)}</span>s, <span>${exact[1].toFixed(2)}</span>s, <span>${exact[2].toFixed(2)}</span>s. La convergencia se mantiene gracias a la diagonal dominante.`;
            } else {
                text = `En este escenario caótico (Mal Condicionado), los semáforos compiten casi idénticamente. Los métodos clásicos fallan en converger a los tiempos óptimos de <span>${exact[0].toFixed(2)}</span>s, <span>${exact[1].toFixed(2)}</span>s, <span>${exact[2].toFixed(2)}</span>s porque el sistema carece de dominancia diagonal clara.`;
            }
            document.getElementById('interpretation').innerHTML = text;
        }"""

interp_new = """function updateInterpretation(sc) {
            let exact = resultData.casos[sc].solucion_exacta;
            let text = "";
            if (sc === 'ideal') {
                text = `<p><strong>Análisis — Escenario Controlado (Tráfico Fluido):</strong><br>
                Bajo condiciones normales de circulación, el modelo matricial detecta una fuerte dominancia diagonal, indicando que cada intersección prioriza sus propios volúmenes viales sin alterar bruscamente el resto de la red.</p>
                <p>La sincronización cronometrada sugiere dotar a la Intersección 1 con <span>${exact[0].toFixed(2)}</span> segundos de luz verde, <span>${exact[1].toFixed(2)}</span>s a la Intersección 2, y <span>${exact[2].toFixed(2)}</span>s a la Intersección 3.</p>
                <p>Al tener una matriz <i>A</i> bien condicionada, el solver alcanza el equilibrio rápidamente (Jacobi convege en ~25 iteraciones y PCG en solo 3). Estas condiciones garantizan un flujo continuo sin aglomeraciones, permitiendo transiciones seguras en los cuellos de botella de la red.</p>`;
            } else if (sc === 'estres') {
                text = `<p><strong>Análisis — Horario Pico (Sobrecruzamiento / Estrés Crítico):</strong><br>
                La demanda <i>b</i> se ha multiplicado drásticamente (10x), reflejando una avalancha local de automóviles. La matriz de ponderaciones también presenta coeficientes extremos frente al embotellamiento.</p>
                <p>Increíblemente, debido a la escalabilidad matemática de las intersecciones, las soluciones relativas requeridas mantienen estabilidad, proponiendo tiempos de <span>${exact[0].toFixed(2)}</span>s, <span>${exact[1].toFixed(2)}</span>s y <span>${exact[2].toFixed(2)}</span>s.</p>
                <p>Observamos robustez numérica: a pesar de los valores altísimos, la propiedad de "Diagonal Dominante" persiste. Esto permite que métodos iterativos simples sigan encontrando la solución en el mismo número de pasos que en flujo ideal, demostrando que la red puede absorber el impacto sin requerir re-agendamientos complejos o rediseños infraestructurales.</p>`;
            } else {
                text = `<p><strong>Análisis — Colapso y Mala Condición (Congestión Acoplada):</strong><br>
                Nos enfrentamos a una catástrofe de modelamiento. Los tres semáforos compiten casi por la misma traza vehicular y reaccionan de manera cuasi-idéntica. En geometría, esto significa que los hiperplanos están casi superpuestos y paralelos.</p>
                <p>El punto de intersección teórico existe en <span>${exact[0].toFixed(2)}</span>s, <span>${exact[1].toFixed(2)}</span>s y <span>${exact[2].toFixed(2)}</span>s, pero es extremadamente sensible. Un leve parpadeo (error de precisión) cambia el equilibrio global y provoca estancamiento total del cómputo.</p>
                <p>Como resultado directo, los solvers tradicionales (Jacobi, Gauss-Seidel y SOR regular) <strong>divergen rápidamente o rebotan indefinidamente sin hallar certidumbre</strong>, forzando la necesidad absoluta de métodos implícitos más agresivos como el Gradiente Conjugado Precondicionado o una eliminación directa de Gauss. En términos de tráfico, la intersección es inoperable y requerirá intervención humana u otro diseño físico para desenredar su geometría de paso.</p>`;
            }
            document.getElementById('interpretation').innerHTML = text;
        }"""

content = content.replace(interp_old, interp_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
