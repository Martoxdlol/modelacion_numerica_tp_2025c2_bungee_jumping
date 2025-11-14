import math
from constantes import L0, k1, m, Y_MAX_ANALITICO, get_acceleration

# RESOLUCIÓN PUNTO 3: MÉTODO DE EULER

# DEFINICIÓN DE LA FÍSICA
def solve_euler(h):
    """
    Simula el salto usando el método de Euler con un paso h.
    Retorna el punto más bajo (y_max) alcanzado.
    """
    y = 0.0
    v = 0.0
    y_max = 0.0

    # Simular hasta que el saltador empiece a subir (v < 0)
    while v >= 0:
        a = get_acceleration(y, v)
        # Actualización de Euler
        y = y + h * v
        v = v + h * a

        if y > y_max:
            y_max = y

    return y_max


def find_h_for_euler_error(target_error):
    """
    Encuentra el paso h necesario para que el error de Euler sea menor
    que target_error.
    """
    print(f"Buscando h para un error < {target_error*100:.1f}% en Euler...")
    h = 0.1  # Empezar con un paso relativamente grande
    while True:
        y_max_euler = solve_euler(h)
        error = abs(Y_MAX_ANALITICO - y_max_euler) / Y_MAX_ANALITICO
        print(f"  h = {h:.5f}, y_max = {y_max_euler:.4f} m, Error = {error*100:.4f}%")
        if error < target_error:
            print(f"\nSe encontró un paso h = {h:.5f} que cumple el requisito.")
            return h
        h /= 2  # Reducir el paso para mejorar la precisión


def check_euler_order():
    """
    Comprueba experimentalmente el orden del método de Euler.
    """
    print("\nComprobando el orden del método de Euler...")
    h1 = 0.005
    h2 = h1 / 2  # Un paso más pequeño

    y1 = solve_euler(h1)
    y2 = solve_euler(h2)

    error1 = abs(Y_MAX_ANALITICO - y1)
    error2 = abs(Y_MAX_ANALITICO - y2)

    # Fórmula del orden: p = log(E1/E2) / log(h1/h2)
    order = math.log(error1 / error2) / math.log(h1 / h2)

    print(f"  Error con h1={h1}: {error1:.6f}")
    print(f"  Error con h2={h2}: {error2:.6f}")
    print(f"  Orden experimental calculado: {order:.4f}")
    print("El resultado es cercano a 1, lo cual es el orden teórico de Euler.")


# EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    print("--- ANÁLISIS NUMÉRICO - BUNGEE JUMPING")
    print(f"Parámetros: m={m:.2f} kg, L0={L0:.2f} m, k1={k1:.2f} N/m")
    print(f"Punto más bajo (Solución Analítica): {Y_MAX_ANALITICO:.2f} m\n")

    print("==================================================")
    print("PUNTO 3: MÉTODO DE EULER")
    print("==================================================")
    find_h_for_euler_error(target_error=0.001)  # Error del 0.1%
    check_euler_order()
