import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the interactive editor buttons and layout to match requirement
# Add method selector
new_editor_html = """
            <h2>Editor Interactivo (JavaScript Solver)</h2>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">
                <button onclick="loadScenario('ideal')" style="flex:1">Caso Ideal</button>
                <button onclick="loadScenario('estres')" style="flex:1">Caso Estrés</button>
                <button onclick="loadScenario('mal_condicionado')" style="flex:1">Mal Cond.</button>
            </div>
            
            <div class="matrix-container" style="background: rgba(0,0,0,0.5); padding: 20px; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 15px;">
                <div class="matrix-row">
                    <input type="number" id="A00" step="any"> <input type="number" id="A01" step="any"> <input type="number" id="A02" step="any"> <span>x₁ =</span> <input type="number" id="b0" step="any">
                </div>
                <div class="matrix-row">
                    <input type="number" id="A10" step="any"> <input type="number" id="A11" step="any"> <input type="number" id="A12" step="any"> <span>x₂ =</span> <input type="number" id="b1" step="any">
                </div>
                <div class="matrix-row">
                    <input type="number" id="A20" step="any"> <input type="number" id="A21" step="any"> <input type="number" id="A22" step="any"> <span>x₃ =</span> <input type="number" id="b2" step="any">
                </div>
            </div>

            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                <select id="interactive-method-sel" style="flex: 1; font-size: 1.1rem; text-align: center;">
                    <option value="jacobi">Método: Jacobi</option>
                    <option value="gauss_seidel">Método: Gauss-Seidel</option>
                    <option value="sor">Método: SOR (ω=1.25/1.05)</option>
                    <option value="pcg">Método: Gradiente Conjugado (PCG)</option>
                </select>
                <button onclick="solveInteractive()" style="flex: 1; font-size: 1.1rem; background: var(--neon-primary); color: #000; font-weight: bold;">Calcular</button>
            </div>

            <div id="interactive-results" class="console-output">Esperando ejecución...</div>
"""

old_editor_start = "<h2>Editor Interactivo (JavaScript Solver)</h2>"
old_editor_end = "<div id=\"interactive-results\" class=\"console-output\">Esperando ejecución...</div>"

start_idx = content.find(old_editor_start)
end_idx = content.find(old_editor_end) + len(old_editor_end)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_editor_html.strip() + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
