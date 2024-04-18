import identity
import os

def list_files(directory):
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' does not exist.")
        return
    
    files = os.listdir(directory)
    return files
    
   
directory_path_input = "reports_unedited"
directory_path_output="reports_deidentified"


def file_changer_all():                                                                 #call this function to change all files from input directory
    files=list_files(directory_path_input)                                              #and store on output directory
    for i in files:
        identity.identityremover(directory_path_input + "\\" + i, directory_path_output+"\\"+i)
        
file_changer_all()


