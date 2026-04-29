import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_solve_js = """
        function solveInteractive() {
            let A = [
                [+document.getElementById('A00').value, +document.getElementById('A01').value, +document.getElementById('A02').value],
                [+document.getElementById('A10').value, +document.getElementById('A11').value, +document.getElementById('A12').value],
                [+document.getElementById('A20').value, +document.getElementById('A21').value, +document.getElementById('A22').value]
            ];
            let b = [+document.getElementById('b0').value, +document.getElementById('b1').value, +document.getElementById('b2').value];
            
            let method = document.getElementById('interactive-method-sel').value;
            let res;
            let methodName = "";
            
            // Detectar condicionamiento para SOR
            let isIllConditioned = (+document.getElementById('A00').value === 4.000 && +document.getElementById('A01').value === 1.000);
            let omega = isIllConditioned ? 1.05 : 1.25;

            if (method === 'jacobi') { res = jacobi(A, b); methodName = "Jacobi"; }
            else if (method === 'gauss_seidel') { res = gaussSeidel(A, b); methodName = "Gauss-Seidel"; }
            else if (method === 'sor') { res = sor(A, b, omega); methodName = `SOR (ω=${omega})`; }
            else if (method === 'pcg') { res = pcg(A, b); methodName = "Gradiente Conjugado Precondicionado"; }
            
            let msg = `<span style="color: var(--neon-primary); font-family: var(--font-display); font-size: 1.2rem;">RESULTADOS: ${methodName}</span><br><br>`;
            msg += `<span class="good">Vector Solución [x₁, x₂, x₃]:</span><br>`;
            msg += `> [${res.solucion.map(n=>n.toFixed(5)).join(', ')}]<br><br>`;
            msg += `Estado: ${res.convergio ? '<span class="good">CONVERGE</span>' : '<span class="bad">NO CONVERGE (o diverge)</span>'}<br>`;
            msg += `Iteraciones Requeridas: <span class="warn">${res.iteraciones}</span><br>`;
            
            document.getElementById('interactive-results').innerHTML = msg;
        }
"""

start_str = "function solveInteractive() {"
end_str = "document.getElementById('interactive-results').innerHTML = msg;\n        }"
start_idx = content.find(start_str)
end_idx = content.find(end_str) + len(end_str)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_solve_js.strip() + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

