import numpy as np
import matplotlib.pyplot as plt
from constantes import L0, g, k1, k2, m

# DEFINICIÓN DE LA FÍSICA
def get_acceleration(y):
    """Calcula la aceleración en una posición y dada."""
    if y <= L0:
        return g
    else:
        f_elastica = k1 * (y - L0) ** k2
        return g - f_elastica / m


# FUNCIONES DE SIMULACIÓN (MODIFICADAS PARA GUARDAR HISTORIAL)

def simulate_euler(h, t_max):
    """
    Simula el salto con el método de Euler y devuelve el historial completo.
    """
    # Inicialización de variables e historiales
    y, v, t = 0.0, 0.0, 0.0
    history = {'t': [], 'y': [], 'v': [], 'a': []}

    while t <= t_max:
        a = get_acceleration(y)
        # Guardar estado actual
        history['t'].append(t)
        history['y'].append(y)
        history['v'].append(v)
        history['a'].append(a)
        # Actualización de Euler
        y += h * v
        v += h * a
        t += h

    # Convertir a arrays de NumPy para facilitar operaciones
    for key in history:
        history[key] = np.array(history[key])
    return history


def simulate_rk4(h, t_max):
    """
    Simula el salto con el método RK4 y devuelve el historial completo.
    """
    # Estado inicial [y, v] y tiempo
    state = np.array([0.0, 0.0])
    t = 0.0
    history = {'t': [], 'y': [], 'v': [], 'a': []}

    def state_derivative(current_state):
        y, v = current_state
        return np.array([v, get_acceleration(y)])

    while t <= t_max:
        # Guardar estado actual
        y, v = state
        a = get_acceleration(y)
        history['t'].append(t)
        history['y'].append(y)
        history['v'].append(v)
        history['a'].append(a)

        # Pasos de Runge-Kutta
        k1 = h * state_derivative(state)
        k2 = h * state_derivative(state + 0.5 * k1)
        k3 = h * state_derivative(state + 0.5 * k2)
        k4 = h * state_derivative(state + k3)

        state += (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        t += h

    for key in history:
        history[key] = np.array(history[key])
    return history


# EJECUCIÓN PRINCIPAL Y GRAFICACIÓN
if __name__ == "__main__":
    T_MAX = 40  # [s] Tiempo total de simulación para ver 4 caídas
    H_EULER = 0.002  # [s] Paso encontrado en el ítem 3
    H_RK4 = 0.1  # [s] Un paso razonable para RK4

    print("Ejecutando simulación de Euler...")
    data_euler = simulate_euler(H_EULER, T_MAX)

    print("Ejecutando simulación de Runge-Kutta 4...")
    data_rk4 = simulate_rk4(H_RK4, T_MAX)

    # Se genera una solución de referencia con RK4 y un paso muy pequeño
    # para simular la "solución analítica" en el tiempo.
    print("Ejecutando simulación de referencia (RK4 alta precisión)...")
    data_ref = simulate_rk4(0.001, T_MAX)

    # Conversión de unidades para los gráficos
    # Velocidad: m/s -> km/h (multiplicar por 3.6)
    data_euler['v'] *= 3.6
    data_rk4['v'] *= 3.6
    data_ref['v'] *= 3.6
    # Aceleración: m/s^2 -> g (dividir por 9.81)
    data_euler['a'] /= g
    data_rk4['a'] /= g
    data_ref['a'] /= g

    # Creación de los gráficos
    fig, axes = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
    fig.suptitle('Análisis Comparativo de Métodos Numéricos - Bungee Jumping', fontsize=16)

    # 1. Gráfico de Posición
    axes[0].plot(data_ref['t'], data_ref['y'], 'k--', label='Referencia (RK4 h=0.001s)')
    axes[0].plot(data_euler['t'], data_euler['y'], label=f'Euler (h={H_EULER}s)')
    axes[0].plot(data_rk4['t'], data_rk4['y'], ':', label=f'RK4 (h={H_RK4}s)')
    axes[0].axhline(y=L0, color='r', linestyle='-.', label=f'L0 = {L0:.1f} m')
    axes[0].set_ylabel('Posición [m]')
    axes[0].set_title('Posición vs. Tiempo')
    axes[0].invert_yaxis()  # Poner y=0 en la parte superior
    axes[0].grid(True)
    axes[0].legend()

    # 2. Gráfico de Velocidad
    axes[1].plot(data_ref['t'], data_ref['v'], 'k--', label='Referencia (RK4 h=0.001s)')
    axes[1].plot(data_euler['t'], data_euler['v'], label=f'Euler (h={H_EULER}s)')
    axes[1].plot(data_rk4['t'], data_rk4['v'], ':', label=f'RK4 (h={H_RK4}s)')
    axes[1].set_ylabel('Velocidad [km/h]')
    axes[1].set_title('Velocidad vs. Tiempo')
    axes[1].grid(True)
    axes[1].legend()

    # 3. Gráfico de Aceleración
    axes[2].plot(data_ref['t'], data_ref['a'], 'k--', label='Referencia (RK4 h=0.001s)')
    axes[2].plot(data_euler['t'], data_euler['a'], label=f'Euler (h={H_EULER}s)')
    axes[2].plot(data_rk4['t'], data_rk4['a'], ':', label=f'RK4 (h={H_RK4}s)')
    axes[2].set_xlabel('Tiempo [s]')
    axes[2].set_ylabel('Aceleración [g]')
    axes[2].set_title('Aceleración vs. Tiempo')
    axes[2].grid(True)
    axes[2].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()