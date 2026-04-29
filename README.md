# Proyecto: Sincronización de Semáforos en una Red Vial Urbana

Este repositorio contiene la resolución del "Desafío Académico: Modelado y Resolución de Sistemas Lineales Complejos" de la materia **Métodos Numéricos** (UMSA, 2026).

Se abordan 3 escenarios de tráfico en un sistema de semáforos, modelados como sistemas de ecuaciones lineales, y se resuelven mediante métodos numéricos iterativos.

## Estructura del repositorio

- `solver.py`: Script en Python encargado de implementar los algoritmos (LU, Jacobi, Gauss-Seidel, SOR y PCG) y exportar los resultados.
- `results.json`: Archivo con las soluciones y el historial de errores (generado automáticamente por el script).
- `index.html`: Una página web interactiva e independiente que permite analizar la convergencia, ver planos de comportamiento en 3D, y re-ejecutar el análisis directamente en tu navegador.

## Cómo ejecutar `solver.py` localmente

1. Debes tener instalado Python y las dependencias estandar de análisis matemático:
   ```bash
   pip install numpy scipy
   ```
2. Ejecuta el script principal:
   ```bash
   python solver.py
   ```
3. El archivo `results.json` se sobreescribirá en el directorio actual con los nuevos resultados.

## Cómo publicar a GitHub Pages

1. Sube los archivos `index.html` y `results.json` a tu rama `main` en GitHub.
2. Ve a la pestaña **Settings** (Configuraciones) del repositorio y navega a **Pages** (Páginas).
3. Selecciona la rama `main` (y opcionalmente la carpeta raíz `/` o `/docs`) como la fuente.
4. Tu sitio se publicará en una URL similar a:
   `https://sebastiandhyaz.github.io/Metodos.Numericos/`
