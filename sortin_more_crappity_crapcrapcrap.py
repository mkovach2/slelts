








import os
import shutil

manip_enabled = True
remove_original = True

home = os.path.expanduser('~')

band = 'o'
orientation = 'v'
stack = 'teos'

in_folder_name = os.path.join(
    home,
    f'Desktop/MX0095A_FC3R5/{stack}/raw_data/{band}{orientation}_{stack}_images'
)
# in_folder_name = os.path.join(home, 'Desktop/mx0095a_fc3r5/Cv_images/toist_wuh')

# out_folder_name = os.path.join(home, 'Desktop/MX0095A_FC3R5/g2f11/Cv_images')
out_folder_name = in_folder_name

for file in os.listdir(in_folder_name):
    whole_file = os.path.join(in_folder_name, file)
    if not(os.path.isdir(whole_file)):
        out_folder_name = os.path.splitext(file.partition('_')[-1])[0]
        out_folder_wholepath = os.path.join(in_folder_name, out_folder_name)
        if not(os.path.isdir(out_folder_wholepath)):
            os.mkdir(out_folder_wholepath)
            print(f'created {out_folder_wholepath}')
        
        if manip_enabled:
            try:
                shutil.copy2(whole_file, os.path.join(out_folder_wholepath, file))
            except:
                print(f'OPE: dident shootle: {whole_file}')
            else:
                if remove_original:
                    os.remove(whole_file)
        else:
            print(f'would be moving\n{file}\nright now, but isnt.')