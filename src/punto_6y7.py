import numpy as np

# PARÁMETROS GLOBALES DEL PROBLEMA
NP = 107973
H = 150.0  # m
m = 40.0 / 10000.0 * (NP - 100000) + 50.0  # kg (81.89)
L0 = (0.1 / 10000.0 * (NP - 100000) + 0.25) * H  # m (49.46)
g = 9.81  # m/s^2

# Parámetros para la resistencia del aire (Punto 7)
c1 = 2.0 / 10000.0 * (NP - 100000) + 3.0  # N(s/m)^c2 (4.59)
c2 = 1.5

# CONDICIONES DEL PROBLEMA
Y_MIN_TARGET = 0.90 * H  # Debe superar el 90% de H (135 m)
Y_MAX_TARGET = 1.00 * H  # No debe superar el 100% de H (150 m)
A_MAX_LIMIT = 2.5 * g   # Aceleración máxima permitida (24.525 m/s^2)


# MOTOR DE SIMULACIÓN (RK4)

def get_acceleration(y, v, k1, k2, with_air_resistance):
    """
    Calcula la aceleración para un estado (y, v) y parámetros de cuerda
    dados. Puede incluir o no la resistencia del aire.
    """
    # Fuerza elástica (solo si la cuerda está tensa)
    f_elastica = 0.0
    if y > L0:
        f_elastica = k1 * (y - L0) ** k2

    # Fuerza viscosa (resistencia del aire)
    f_viscosa = 0.0
    if with_air_resistance:
        # Usamos -sign(v) para asegurar que la fuerza siempre se oponga al
        # movimiento. Esto resuelve el problema de v^c2 para v<0.
        f_viscosa = np.sign(v) * c1 * (abs(v) ** c2)

    # Segunda Ley de Newton: a = F_neta / m
    f_neta = m * g - f_elastica - f_viscosa
    return f_neta / m


def simulate_first_drop(k1, k2, with_air_resistance=False):
    """
    Simula solo la primera caída usando RK4.
    Retorna la profundidad máxima (y_max) y la aceleración en ese punto.
    """
    h = 0.01  # Paso de tiempo pequeño para una simulación precisa
    state = np.array([0.0, 0.0])  # [y, v]

    y_max = 0.0
    a_at_ymax = 0.0

    def state_derivative(current_state):
        y, v = current_state
        a = get_acceleration(y, v, k1, k2, with_air_resistance)
        return np.array([v, a])

    # Simular solo hasta que la velocidad se haga negativa (fin de la 1ra caída)
    while state[1] >= 0:
        k1_v = h * state_derivative(state)
        k2_v = h * state_derivative(state + 0.5 * k1_v)
        k3_v = h * state_derivative(state + 0.5 * k2_v)
        k4_v = h * state_derivative(state + k3_v)
        state += (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6.0

        if state[0] > y_max:
            y_max = state[0]
            # Guardamos la aceleración en el punto más bajo
            a_at_ymax = get_acceleration(state[0], state[1], k1, k2, with_air_resistance)
        
        # Condición de seguridad para evitar bucles infinitos si k1 es muy bajo
        if y_max > H + 10:
            break

    return y_max, a_at_ymax


def find_optimal_params(with_air_resistance):
    """
    Busca en una grilla de parámetros (k1, k2) una combinación que
    cumpla las condiciones del problema.
    """
    print("Iniciando búsqueda de parámetros...")
    print(f"Condiciones: {Y_MIN_TARGET:.1f}m < y_max < {Y_MAX_TARGET:.1f}m | |a_max| < {A_MAX_LIMIT:.2f} m/s^2")

    # Rangos de búsqueda para k1 y k2. Estos rangos se eligen por intuición
    # y pueden necesitar ajustes. Un k2 alto necesita un k1 muy bajo.
    k2_range = np.arange(0.5, 20, 0.25)
    k1_range = np.arange(0.5, 20, 0.25)

    for k2_val in k2_range:
        for k1_val in k1_range:
            print(f"  Probando: k1 = {k1_val:.3f}, k2 = {k2_val:.1f}...", end='\r')
            
            y_max, a_max = simulate_first_drop(k1_val, k2_val, with_air_resistance)

            # Verificar si los resultados cumplen las dos condiciones
            condicion_altura = Y_MIN_TARGET < y_max < Y_MAX_TARGET
            condicion_aceleracion = abs(a_max) < A_MAX_LIMIT

            if condicion_altura and condicion_aceleracion:
                print("\n¡Solución encontrada!                       ")
                return k1_val, k2_val, y_max, a_max

    print("\nNo se encontró una solución en los rangos de búsqueda definidos.")
    return None, None, None, None


# EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    print("==================================================")
    print("PUNTO 6: Dimensionamiento SIN Resistencia del Aire")
    print("==================================================")
    k1_s6, k2_s6, y_max_s6, a_max_s6 = find_optimal_params(with_air_resistance=False)

    if k1_s6:
        print("\n--- Resultados (Sin Aire) ---")
        print(f"Parámetros encontrados: k1 = {k1_s6:.4f}, k2 = {k2_s6:.2f}")
        print(f"Profundidad máxima:     y_max = {y_max_s6:.2f} m")
        print(f"Aceleración en y_max:   a_max = {a_max_s6:.2f} m/s^2 ({abs(a_max_s6/g):.2f} g)")

    print("\n==================================================")
    print("PUNTO 7: Dimensionamiento CON Resistencia del Aire")
    print("==================================================")
    k1_s7, k2_s7, y_max_s7, a_max_s7 = find_optimal_params(with_air_resistance=True)

    if k1_s7:
        print("\n--- Resultados (Con Aire) ---")
        print(f"Parámetros encontrados: k1 = {k1_s7:.4f}, k2 = {k2_s7:.2f}")
        print(f"Profundidad máxima:     y_max = {y_max_s7:.2f} m")
        print(f"Aceleración en y_max:   a_max = {a_max_s7:.2f} m/s^2 ({abs(a_max_s7/g):.2f} g)")

    print("\n\n--- COMPARACIÓN Y ANÁLISIS ---")
    if k1_s6 and k1_s7:
        print(f"k1 (Sin Aire): {k1_s6:.4f}  vs  k1 (Con Aire): {k1_s7:.4f}")
        print("La resistencia del aire disipa energía del sistema. "
              "Esto significa que, para una misma cuerda, el saltador no caerá tan profundo.")
        print("Para compensar esta pérdida de energía y alcanzar la misma "
              "profundidad objetivo, se necesita una cuerda 'más blanda', "
              "es decir, con una constante elástica k1 menor.")