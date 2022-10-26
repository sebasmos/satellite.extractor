"""
Following https://blogs.oracle.com/cloud-infrastructure/post/uploading-whole-directories-oracle-object-storage-using-a-python-script 
path: /home/sebasmos/Desktop/satellite.extractor/src/Oracle-custom-scripts

Using a Pool of workers instead of spinning up new processes and storing references in proc_lis


"""
from array import array 
from pathlib import Path 
import oci 
from multiprocessing import Process 
from multiprocessing import Semaphore 
print(oci.__version__)
# Number of max processes allowed at a time 
from array import array 
from pathlib import Path 
import oci 
from multiprocessing import Process 
from multiprocessing import Semaphore
from multiprocessing import Pool #*ADDED*
# Number of max processes allowed at a time 
concurrency= 5 
#sema = Semaphore(concurrency) #*REMOVED*
# The root directory path, Replace with your path 
#p = Path('/home/sebasmos/Desktop/FULL_COLOMBIA_v2') 
p = Path("/home/sebasmos/Desktop/DATASETS/DATASET_augmented_v1")
# The Compartment OCID 
compartment_id = "ocid1.compartment.oc1..aaaaaaaamgl2tu5vh7mcyjsd2h7tq5umvcq6ivcjftljmzaq53kct6khrd7q"# "ocid1.bucket.oc1.iad.aaaaaaaag7iym7awzokrjn63epcjuczilhxk22olsqpk6nafhc43ok4exjuq"#"ocid1.compartment.oc1..aaaaaaaamgl2tu5vh7mcyjsd2h7tq5umvcq6ivcjftljmzaq53kct6khrd7q"
# The Bucket name where we will upload 
bucket_name = "Sentinel_2_Images" 

""" 
upload_to_object_storage will upload a file to an object storage bucket. 
This function is intended to be run as a separate process. The client is 
created with each invocation so that the separate processes do not have a reference to the same client. 
:param path: The path of the object to upload 
:param name: The name of the object to upload 
:param object_storage_client: The object storage sdk client 
:param namespace: The namespace of the bucket 

""" 
def upload_to_object_storage(path:str,name:str,namespace): 
  with open(path, "rb") as in_file: 
    print("Starting upload {}", format(name)) 
    object_storage_client.put_object(namespace,bucket_name,name,in_file) 
    print("Finished uploading {}".format(name)) 
    #sema.release() #*REMOVED*

#*ADDED* initialize the worksers with a reference to the authenticated client
# Unsure if this has concurrency (or other) consequences
def os_worker_initializer(os_client):
  global object_storage_client
  object_storage_client = os_client

""" 
createUploadProcess will create a concurrent upload process and put it in proc_list. 
:param object: The path of the object to upload 
:param object_storage_client: The object storage sdk client 
:param namespace: The namespace of the bucket 
:param proc_list:The client list, The client is created with each invocation so that the separate processes do not have a reference to the same client. 

""" 
def createUploadProcess(object:Path,object_storage_client,namespace,proc_list): 
  name = object.relative_to(p).as_posix() 
  args=(object.as_posix(),name,namespace) #*ADDED*
  proc_list.append(args) #*ADDED*
  #*REMOVED Below code* 
  #sema.acquire() 
  #process = Process(target=upload_to_object_storage, args=(object.as_posix(),name,object_storage_client,namespace)) 
  #proc_list.append(process) 
  #process.start() 

""" 
processDirectoryObjects will check if the current object path is a file or not, if yes it will create a upload process 
:param object: The path of the object to upload 
:param object_storage_client: The object storage sdk client 
:param namespace: The namespace of the bucket 

:param proc_list: The client list, The client is created with each invocation so that the separate processes do not have a reference to the same client. 

""" 
def processDirectoryObjects(object:Path,object_storage_client, namespace,proc_list): 
  if object.is_file(): 
    createUploadProcess(object,object_storage_client, namespace,proc_list) 

""" 
processDirectory will process the current directory 
:param path: the path of the current directory 
:param object_storage_client: The object storage sdk client 
:param namespace: The namespace of the bucket 
:proc_list: The client list, The client is created with each invocation so that the separate processes do not have a reference to the same client. 

""" 
def processDirectory(path:Path,object_storage_client,namespace,proc_list): 
  if path.exists(): 
    print("in directory ---- " + path.relative_to(p).as_posix()) 
    for objects in path.iterdir(): 
      if objects.is_dir(): 
        processDirectory(objects,object_storage_client, namespace,proc_list) 
      else: 
        processDirectoryObjects(objects,object_storage_client, namespace,proc_list)

if __name__ == '__main__': 
    config = oci.config.from_file() 
    object_storage_client = oci.object_storage.ObjectStorageClient(config) 
    namespace = object_storage_client.get_namespace().data 
    #proc_list: array = [] #*REMOVED*
    proc_list = [] #*ADDED*
    #sema = Semaphore(concurrency) #*REMOVED*
    if p.exists() and p.is_dir(): 
        processDirectory(p,object_storage_client,namespace,proc_list) 
  
    # ADDED Below, see docs here: https://docs.python.org/3/library/multiprocessing.html
    with Pool(processes=concurrency, initializer=os_worker_initializer(object_storage_client)) as pool:
        pool.starmap(upload_to_object_storage, proc_list)
  
    #*REMOVED Below*
    #for job in proc_list: 
    #    job.join()
