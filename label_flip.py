import os
import shutil
import sys

original_dataset = sys.argv[1]

original_folders = []
folders_copy = []
n=1

for folder_name in os.listdir(original_dataset):
    original_folders.append(folder_name)
    folders_copy.append(folder_name)
    
for i in range(0, n):    
    last = original_folders[len(original_folders)-1]
    for j in range(len(original_folders)-1, -1, -1):       
        original_folders[j] = original_folders[j-1]
        original_folders[0] = last             

shutil.move(original_dataset+"/"+folders_copy[0],original_dataset+"/label_0")
shutil.move(original_dataset+"/"+folders_copy[len(original_folders)-1],original_dataset+"/last_label")
for i in range(1,len(original_folders)):
    shutil.move(original_dataset+"/"+folders_copy[i], original_dataset+"/"+original_folders[i])
shutil.move(original_dataset+"/label_0", original_dataset+"/"+folders_copy[len(folders_copy)-1])
shutil.move(original_dataset+"/last_label",original_dataset+"/"+folders_copy[0])

