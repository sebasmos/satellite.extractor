import sys
sys.path.append("..") 
from utils.utils import TestConvolucionUpsampling

mensaje = TestConvolucionUpsampling().test_convolucion_upsampling()
print(mensaje)
