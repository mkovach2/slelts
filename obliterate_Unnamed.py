import os

'''
a script to blow up all the shit that clogs my temp/gds folder
'''

PATH_TO_TEMP_GDSF = r'C:\Users\miles.HYPERLIGHT\AppData\Local\Temp\gdsfactory'
FILES_TO_DESTROY_PREFIXES = (
    "Unnamed",
    "remap",
    "boolean",
)

if __name__ == "__main__":
    noisy = False
    files_destroyt = 0

    for file in os.listdir(PATH_TO_TEMP_GDSF):
        DESTROY = False
        splitted_name = file.split('_')
        if splitted_name[0] in FILES_TO_DESTROY_PREFIXES:
            DESTROY = True
        if (not DESTROY) and len(splitted_name) > 1:
            DESTROY = DESTROY or splitted_name[1] in FILES_TO_DESTROY_PREFIXES

        if DESTROY:
            os.remove(os.path.join(PATH_TO_TEMP_GDSF, file))
            if noisy:
                print(f'{file} destroyt? -> YES')
            files_destroyt += 1

        # else:
        #     print(f'{file} destroyt? -> NO')

        # print(f'\t{splitted_name}')

    print(f'{files_destroyt = }')


# end if __name__ == "__main__"
