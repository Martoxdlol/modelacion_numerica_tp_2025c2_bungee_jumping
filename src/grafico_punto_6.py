import numpy as np
import matplotlib.pyplot as plt
import punto_6y7 as bd

def scan_parameter_space():
    """
    Realiza una búsqueda en una grilla de parámetros (k1, k2) y
    almacena todas las combinaciones que cumplen las condiciones del Punto 6.
    """
    print("Iniciando escaneo del espacio de parámetros. Esto puede tardar varios segundos...")

    # Definir un rango de búsqueda más amplio y denso para el gráfico
    k1_range = np.arange(0.5, 20, 0.25)
    k2_range = np.arange(1, 2, 0.01)

    # Listas para almacenar las soluciones válidas
    valid_solutions = []

    total_iterations = len(k1_range) * len(k2_range)
    current_iteration = 0

    # Iterar sobre todas las combinaciones de k1 y k2
    for k2_val in k2_range:
        for k1_val in k1_range:
            # Actualizar el progreso en la consola
            current_iteration += 1
            print(f"  Progreso: {current_iteration / total_iterations * 100:.1f}%", end='\r')

            # Ejecutar la simulación para el Punto 6 (sin resistencia de aire)
            y_max, a_max = bd.simulate_first_drop(k1_val, k2_val, with_air_resistance=False)

            # Verificar si se cumplen las condiciones de altura y aceleración
            condicion_altura = bd.Y_MIN_TARGET < y_max < bd.Y_MAX_TARGET
            condicion_aceleracion = abs(a_max) < bd.A_MAX_LIMIT

            if condicion_altura and condicion_aceleracion:
                # Si es una solución válida, la guardamos
                valid_solutions.append({
                    'k1': k1_val,
                    'k2': k2_val,
                    'y_max': y_max,
                    'a_max': a_max
                })

    print("\nEscaneo completado.")
    return valid_solutions


def plot_results(solutions):
    """
    Genera un gráfico de dispersión con las soluciones válidas y sus anotaciones.
    """

    # Extraer los datos para el gráfico
    k1_vals = [s['k1'] for s in solutions]
    k2_vals = [s['k2'] for s in solutions]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(15, 10))

    # Graficar los puntos (k1, k2) que son soluciones válidas
    ax.scatter(k1_vals, k2_vals, color='royalblue', zorder=5)

    contador_annotation = 0

    max_max_y = max([s['y_max'] for s in solutions])
    min_max_y = min([s['y_max'] for s in solutions])

    max_max_a = max([abs(s['a_max']) for s in solutions])
    min_max_a = min([abs(s['a_max']) for s in solutions])

    max_k2 = max(k2_vals)
    min_k2 = min(k2_vals)

    max_k1 = max(k1_vals)
    min_k1 = min(k1_vals)

    # Añadir anotaciones para cada punto
    for sol in solutions:
        k1 = sol['k1']
        k2 = sol['k2']
        y_max = sol['y_max']
        a_max = sol['a_max']

        annotation_text = ''

        is_max_max_y = y_max == max_max_y
        is_min_max_y = y_max == min_max_y
        is_max_max_a = a_max == max_max_a
        is_min_max_a = a_max == min_max_a

        is_min_max_k1_k2 = k1 == min_k1 or k2 == min_k2 or k1 == max_k1 or k2 == max_k2

        if contador_annotation % 10 == 0 or is_max_max_y or is_min_max_y or is_max_max_a or is_min_max_a or is_min_max_k1_k2:
            # Formatear el texto de la anotación
            annotation_text = f"y={y_max:.1f}m\na={abs(a_max):.2f}m/s²\nk1={k1:.2f}\nk2={k2:.2f}"
            if is_max_max_y:
                annotation_text = "↑ Máx y\n" + annotation_text
            if is_min_max_y:
                annotation_text = "↓ Mín y\n" + annotation_text
            if is_max_max_a:
                annotation_text = "↑ Máx |a|\n" + annotation_text
            if is_min_max_a:
                annotation_text = "↓ Mín |a|\n" + annotation_text

        else:
            annotation_text = ''

        contador_annotation += 1

        ax.annotate(annotation_text,
                    xy=(k1, k2),
                    xytext=(5, 5),  # Pequeño desplazamiento del texto
                    textcoords="offset points",
                    ha='left',
                    va='bottom',
                    fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.3", fc="ivory", ec="gray", lw=0.5, alpha=0.7))

    # Configurar el estilo y las etiquetas del gráfico
    ax.set_xlabel('Constante Elástica k1 [N/m^k2]', fontsize=12)
    ax.set_ylabel('Exponente Elástico k2', fontsize=12)
    ax.set_title('Espacio de Soluciones Válidas para Parámetros de Cuerda (Punto 6)', fontsize=16)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Mejorar la apariencia general
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 1. Escanear el espacio de parámetros para encontrar todas las soluciones
    valid_solutions_found = scan_parameter_space()
    
    # 2. Graficar los resultados encontrados
    plot_results(valid_solutions_found)