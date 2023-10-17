import sys
sys.path.append("..") 
from satellite_extractor.utils import TestConvolucionUpsampling

mensaje = TestConvolucionUpsampling().test_convolucion_upsampling()
print(mensaje)
