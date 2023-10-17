import numpy as np

def convolucion_upsampling(imagen, filtro):
    """
    Realiza una convolución de upsampling de una imagen con un filtro.

    Args:
    imagen (numpy.ndarray): La imagen de entrada.
    filtro (numpy.ndarray): El filtro de convolución.

    Returns:
    numpy.ndarray: La imagen resultante después de la convolución de upsampling.
    """
    if not isinstance(imagen, np.ndarray) or not isinstance(filtro, np.ndarray):
        raise ValueError("Ambos argumentos deben ser matrices NumPy.")
    
    if imagen.ndim != 2 or filtro.ndim != 2:
        raise ValueError("Tanto la imagen como el filtro deben ser matrices 2D.")

    altura_imagen, ancho_imagen = imagen.shape
    altura_filtro, ancho_filtro = filtro.shape
    altura_resultado = altura_imagen + altura_filtro - 1
    ancho_resultado = ancho_imagen + ancho_filtro - 1
    resultado = np.zeros((altura_resultado, ancho_resultado))

    for i in range(altura_imagen):
        for j in range(ancho_imagen):
            resultado[i:i+altura_filtro, j:j+ancho_filtro] += imagen[i, j] * filtro

    return resultado


class TestConvolucionUpsampling():
    def test_convolucion_upsampling(self):
        
        imagen = np.array([[1, 2],
                          [3, 4]])
        filtro = np.array([[0.5, 0.5],
                          [0.5, 0.5]])

        
        print("Convolution shape: ",convolucion_upsampling(imagen, filtro).shape)
        
if __name__ == '__main__':
    TestConvolucionUpsampling().test_convolucion_upsampling()

