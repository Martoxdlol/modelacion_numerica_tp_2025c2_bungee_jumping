# PARÁMETROS GLOBALES DEL PROBLEMA
# Se utilizan los valores calculados en la resolución teórica.
NP = 107973
H = 150.0  # m
m = 40.0 / 10000.0 * (NP - 100000) + 50.0  # kg (81.892)
L0 = (0.1 / 10000.0 * (NP - 100000) + 0.25) * H  # m (49.4595)
k1 = 10.0 / 10000.0 * (NP - 100000) + 40.0  # N/m (47.973)
k2 = 1.0  # Para los ítems 2, 3 y 4
g = 9.81  # m/s^2
# Valor analítico para la comparación
Y_MAX_ANALITICO = 110.22  # m

def get_acceleration(y, _v):
    """
    Calcula la aceleración en un punto y dado.
    Se ignora la velocidad 'v' ya que no hay rozamiento en estos ítems.
    """
    if y <= L0:
        # Caída libre
        return g
    else:
        # La cuerda está tensa
        f_elastica = k1 * (y - L0) ** k2
        return g - f_elastica / m