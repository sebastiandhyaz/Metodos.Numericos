import numpy as np
import scipy.linalg as la
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def exact_solution(A, b):
    try:
        sol = np.linalg.solve(A, b)
        return sol.tolist()
    except np.linalg.LinAlgError:
        return None

def lu_solution(A, b):
    try:
        lu, piv = la.lu_factor(A)
        sol = la.lu_solve((lu, piv), b)
        return {"iters": "Directo", "solucion": sol.tolist(), "error": 0.0, "convergio": True}
    except Exception as e:
        return {"iters": "Directo", "solucion": None, "error": None, "convergio": False}

def jacobi(A, b, exact, tol=1e-6, max_iter=1000):
    n = len(b)
    x = np.zeros(n)
    D = np.diag(A)
    R = A - np.diagflat(D)
    
    historial = []
    convergio = False
    
    for i in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        error = np.linalg.norm(x_new - x, ord=np.inf)
        # Using exact relative error if available
        rel_error = np.linalg.norm(x_new - exact) / np.linalg.norm(exact) if exact is not None else error
        historial.append(float(rel_error))
        
        if error < tol:
            convergio = True
            x = x_new
            break
        x = x_new
        
    return {"iters": len(historial), "solucion": x.tolist(), "error": historial[-1], "historial": historial, "convergio": convergio}

def gauss_seidel(A, b, exact, tol=1e-6, max_iter=1000):
    n = len(b)
    x = np.zeros(n)
    
    historial = []
    convergio = False
    
    for it in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (b[i] - s1 - s2) / A[i][i]
            
        error = np.linalg.norm(x_new - x, ord=np.inf)
        rel_error = np.linalg.norm(x_new - exact) / np.linalg.norm(exact) if exact is not None else error
        historial.append(float(rel_error))
        
        if error < tol:
            convergio = True
            x = x_new
            break
        x = x_new
        
    return {"iters": len(historial), "solucion": x.tolist(), "error": historial[-1], "historial": historial, "convergio": convergio}

def sor(A, b, exact, omega=1.25, tol=1e-6, max_iter=1000):
    n = len(b)
    x = np.zeros(n)
    
    historial = []
    convergio = False
    
    for it in range(max_iter):
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x_new[i] = (1 - omega) * x[i] + (omega / A[i][i]) * (b[i] - s1 - s2)
            
        error = np.linalg.norm(x_new - x, ord=np.inf)
        rel_error = np.linalg.norm(x_new - exact) / np.linalg.norm(exact) if exact is not None else error
        historial.append(float(rel_error))
        
        if error < tol:
            convergio = True
            x = x_new
            break
        x = x_new
        
    return {"iters": len(historial), "solucion": x.tolist(), "error": historial[-1], "historial": historial, "convergio": convergio}

def pcg(A, b, exact, tol=1e-6, max_iter=1000):
    n = len(b)
    x = np.zeros(n)
    
    # Precondicionador diagonal (Algoritmo 2 Suñagua)
    M_inv = 1.0 / np.diag(A)
    
    r = b - np.dot(A, x)
    z = M_inv * r
    p = np.copy(z)
    
    rz_old = np.dot(r, z)
    
    historial = []
    convergio = False
    
    for i in range(max_iter):
        Ap = np.dot(A, p)
        alpha = rz_old / np.dot(p, Ap)
        
        x_new = x + alpha * p
        r_new = r - alpha * Ap
        
        error = np.linalg.norm(x_new - x, ord=np.inf)
        rel_error = np.linalg.norm(x_new - exact) / np.linalg.norm(exact) if exact is not None else error
        historial.append(float(rel_error))
        
        if np.linalg.norm(r_new) < tol:
            convergio = True
            x = x_new
            break
            
        z_new = M_inv * r_new
        rz_new = np.dot(r_new, z_new)
        beta = rz_new / rz_old
        
        p = z_new + beta * p
        
        x = x_new
        r = r_new
        rz_old = rz_new
        
    return {"iters": len(historial), "solucion": x.tolist(), "error": historial[-1] if historial else 0, "historial": historial, "convergio": convergio}


def main():
    casos = {
        "ideal": {
            "A": [[4, 1, 0], [1, 3, 1], [0, 1, 4]],
            "b": [15, 18, 14],
            "omega": 1.25
        },
        "estres": {
            "A": [[40, 10, 0], [10, 35, 10], [0, 10, 40]],
            "b": [150, 200, 140],
            "omega": 1.25
        },
        "mal_condicionado": {
            "A": [[4.000, 1.000, 1.000], [1.000, 4.000, 1.001], [1.000, 1.001, 4.000]],
            "b": [10, 10, 10],
            "omega": 1.05
        }
    }
    
    resultados_json = {"casos": {}}
    
    for key, data in casos.items():
        logging.info(f"Procesando caso: {key}")
        A = np.array(data["A"])
        b = np.array(data["b"])
        omega = data["omega"]
        
        exact = exact_solution(A, b)
        
        resultados_json["casos"][key] = {
            "A": data["A"],
            "b": data["b"],
            "solucion_exacta": exact,
            "metodos": {
                "lu": lu_solution(A, b),
                "jacobi": jacobi(A, b, exact),
                "gauss_seidel": gauss_seidel(A, b, exact),
                "sor": sor(A, b, exact, omega=omega),
                "pcg": pcg(A, b, exact)
            }
        }
        
    with open("results.json", "w") as f:
        json.dump(resultados_json, f, indent=2)
    logging.info("Archivo results.json generado exitosamente.")

if __name__ == "__main__":
    main()
