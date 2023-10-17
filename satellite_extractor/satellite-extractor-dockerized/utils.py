
import shutil
# Source path 
src = '../../linux'
# Destination path 
dest = './linux'
# Copy the content of 
# source to destination 
destination = shutil.copytree(src, dest, copy_function = shutil.copy) 
print("files copied succesfully")