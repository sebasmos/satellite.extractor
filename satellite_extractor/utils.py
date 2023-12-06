import numpy as np
import glob
import os
import matplotlib.pyplot as plt
from skimage import io
import skimage
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import random

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

def read_tiff(img_path, resize_ratio=None, resizing=True, normalize=True, printing=True):
    """
    Read and preprocess a TIFF image.

    Parameters:
    - img_path (str): Path to the TIFF image file.
    - resize_ratio (float, optional): Ratio for resizing the image.
    - resizing (bool, optional): Flag to indicate whether resizing is enabled.
    - normalize (bool, optional): Flag to indicate whether image normalization is enabled.
    - printing (bool, optional): Flag to indicate whether to print information about the image.

    Returns:
    - img_F (numpy.ndarray): Processed image.
    """
    img = io.imread(img_path)
    img_F = img.copy()

    path_img = os.path.basename(img_path)
    if normalize:
        CHANNELS = range(12)
        img_F = np.dstack([
            skimage.exposure.rescale_intensity(img_F[:, :, c], out_range=(0, 1))
            for c in CHANNELS])
    if printing:
        print(f"(origin shape: {path_img}: {img.shape} -> rescale: {str(img_F.shape)}) - Range -> [{img_F.min(), img_F.max()}]")
    return img_F

if __name__ == '__main__':
    TestConvolucionUpsampling().test_convolucion_upsampling()

