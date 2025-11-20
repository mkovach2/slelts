








import os
import shutil

home = os.path.expanduser('~')
in_folder_name = os.path.join(home, 'Desktop/mx0095a_fc3r5/Cv_images/toist_wuh')

for file in os.listdir(in_folder_name):
    whole_file = os.path.join(in_folder_name, file)
    if not(os.path.isdir(whole_file)):
        out_folder_name = os.path.splitext(file.partition('_')[-1])[0]
        out_folder_wholepath = os.path.join(in_folder_name, out_folder_name)
        if not(os.path.isdir(out_folder_wholepath)):
            os.mkdir(out_folder_wholepath)
            print(f'created {out_folder_wholepath}')