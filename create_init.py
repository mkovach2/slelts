import os
def create_init(folder_path, root_dir_name):
    functions_dict = {}

    folder_path = os.path.abspath(folder_path)
    folder_path_temp = folder_path

    package_str = ''
    n = 0 # for safety
    while os.path.basename(folder_path_temp) != root_dir_name and n < 10:
        print(os.path.dirname(folder_path_temp))
        package_str = os.path.basename(folder_path_temp) + '.' + package_str
        folder_path_temp = os.path.dirname(folder_path_temp)
        n += 1
    package_str = root_dir_name + '.' + package_str

    for file in os.listdir(folder_path):
        if os.path.splitext(file)[-1] == '.py' and file != 'create_init.py':
            file_pack_name = file.split('.py')[0]
            functions_dict[file_pack_name] = []
            with open(os.path.join(folder_path, file), 'r') as fr:
                for line in fr.readlines():
                    if line.strip() == "if __name__ == \"__main__\":":
                        break
                    elif line.strip()[:4] == "def ":
                        functions_dict[file_pack_name].append(
                            line.strip()[4:].split('(')[0]
                        )

    out_str_1 = ''
    out_str_2 = '__all__ = [\n'
    for key in functions_dict.keys():
        if len(functions_dict[key]) == 1:
            out_str_1 += f'from {package_str + key} import {functions_dict[key][0]}\n'
            out_str_2 += f'    \"{functions_dict[key][0]}\",\n'
        elif len(functions_dict[key]) > 1:
            out_str_1 += f'from {package_str + key} import (\n'
            for item in functions_dict[key]:
                out_str_1 += f'    {item},\n'
                out_str_2 += f'    \"{item}\",\n'

            out_str_1 += ')\n'
    out_str_2 += ']'
    # print(out_str_1)
    # print(out_str_2)

    with open(os.path.join(folder_path, "__init__.py"), 'w') as init:
        init.write(out_str_1 + out_str_2)


if __name__ == "__main__":
    folder = input('what foldeur?\n_')
    rootname = input('what root_dir_name?\n_')

    if '__init__.py' in os.listdir(folder):
        exists_warn = (
            "__init__.py already exsists in:\n"
            + os.path.abspath(folder)
            + "\noverwrite it? (y/N)_"
        )
        yslashn = input(exists_warn)
    else:
        yslashn = 'y'

    if yslashn.lower() == 'y':
        create_init(
            folder_path=os.path.abspath(folder),
            root_dir_name=rootname,
        )

    input('done, slam that mf [enter] to be REAL done.')

# end if __name__ == "__main__"
