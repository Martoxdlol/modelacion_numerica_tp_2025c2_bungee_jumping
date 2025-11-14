import numpy as np
import matplotlib.pyplot as plt
from punto_6y7 import m, L0, g, c1, c2

# --- MOTOR DE SIMULACIÓN (ADAPTADO PARA SER REUTILIZABLE) ---

def simulate_jump_history(k1, k2, with_air_resistance, t_max=40, h=0.05):
    """
    Simula el salto completo usando RK4 y devuelve el historial de datos.

    Args:
        k1 (float): Constante elástica de la cuerda.
        k2 (float): Exponente elástico de la cuerda.
        with_air_resistance (bool): Si es True, incluye el efecto del aire.
        t_max (float): Tiempo total de simulación en segundos.
        h (float): Paso de tiempo para la simulación.

    Returns:
        dict: Un diccionario con los arrays de tiempo, posición, velocidad y aceleración.
    """
    state = np.array([0.0, 0.0])  # [y, v]
    t = 0.0
    history = {'t': [], 'y': [], 'v': [], 'a': []}

    # Función anidada para calcular la derivada del estado (dy/dt, dv/dt)
    def state_derivative(current_state):
        y, v = current_state
        
        # Fuerza elástica
        f_elastica = k1 * (y - L0) ** k2 if y > L0 else 0.0
        
        # Fuerza viscosa (resistencia del aire)
        f_viscosa = np.sign(v) * c1 * (abs(v) ** c2) if with_air_resistance else 0.0
        
        # Aceleración total
        a = g - (f_elastica + f_viscosa) / m
        
        return np.array([v, a])

    # Bucle de simulación
    while t <= t_max:
        y, v = state
        a = state_derivative(state)[1] # Obtenemos la aceleración del cálculo
        history['t'].append(t)
        history['y'].append(y)
        history['v'].append(v)
        history['a'].append(a)

        # Pasos de Runge-Kutta 4
        k1_v = h * state_derivative(state)
        k2_v = h * state_derivative(state + 0.5 * k1_v)
        k3_v = h * state_derivative(state + 0.5 * k2_v)
        k4_v = h * state_derivative(state + k3_v)
        state += (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6.0
        t += h

    # Convertir listas a arrays de NumPy para facilitar el post-procesamiento
    for key in history:
        history[key] = np.array(history[key])
        
    return history


# --- FUNCIÓN PRINCIPAL DE GRAFICACIÓN ---

def plot_simulation(k1, k2, with_air_resistance=False):
    """
    Dada una combinación de k1 y k2, simula y grafica el salto.
    """
    print(f"\nGenerando gráfico para k1={k1}, k2={k2} (Resistencia del Aire: {'Sí' if with_air_resistance else 'No'})...")
    
    # 1. Ejecutar la simulación para obtener los datos
    data = simulate_jump_history(k1, k2, with_air_resistance)
    
    # 2. Convertir unidades para los gráficos
    data['v'] *= 3.6  # m/s -> km/h
    data['a'] /= g    # m/s^2 -> g's
    
    # 3. Crear los gráficos
    fig, axes = plt.subplots(3, 1, figsize=(12, 15), sharex=True)
    
    # Título general
    air_status = "CON Resistencia del Aire" if with_air_resistance else "SIN Resistencia del Aire"
    fig.suptitle(f'Simulación de Salto Bungee\nk1={k1}, k2={k2} - {air_status}', fontsize=16)

    # Gráfico de Posición
    axes[0].plot(data['t'], data['y'], label='Posición del saltador', color='blue')
    axes[0].axhline(y=L0, color='r', linestyle='-.', label=f'Longitud natural L0 = {L0:.1f} m')
    axes[0].set_ylabel('Posición [m]')
    axes[0].set_title('Posición vs. Tiempo')
    axes[0].invert_yaxis()
    axes[0].grid(True, linestyle=':')
    axes[0].legend()

    # Gráfico de Velocidad
    axes[1].plot(data['t'], data['v'], label='Velocidad del saltador', color='green')
    axes[1].set_ylabel('Velocidad [km/h]')
    axes[1].set_title('Velocidad vs. Tiempo')
    axes[1].grid(True, linestyle=':')

    # Gráfico de Aceleración
    axes[2].plot(data['t'], data['a'], label='Aceleración del saltador', color='purple')
    axes[2].set_xlabel('Tiempo [s]')
    axes[2].set_ylabel('Aceleración [g]')
    axes[2].set_title('Aceleración vs. Tiempo')
    axes[2].grid(True, linestyle=':')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


# --- EJEMPLOS DE USO ---
if __name__ == "__main__":
    # --- Ejemplo para el Punto 6 (Sin Resistencia del Aire) ---
    # Usamos los parámetros óptimos encontrados anteriormente.
    k1_punto6 = 13
    k2_punto6 = 1.17
    plot_simulation(k1=k1_punto6, k2=k2_punto6, with_air_resistance=False)

    # --- Ejemplo para el Punto 7 (Con Resistencia del Aire) ---
    # Usamos los parámetros óptimos encontrados para este caso.
    k1_punto7 = 7
    k2_punto7 = 1.17
    plot_simulation(k1=k1_punto7, k2=k2_punto7, with_air_resistance=True)

    # --- Ejemplo Adicional: Cuerda muy "dura" para ver la diferencia ---
    # plot_simulation(k1=2.5, k2=1.9, with_air_resistance=True)