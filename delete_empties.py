import os

the_dir = input('input directory:\n').replace('\\','/')
subf = os.listdir(the_dir)
print(subf)
print('\n')
for file in subf:
    if os.path.isdir(the_dir + '/' + file):
        if os.listdir(the_dir + '/' + file) == []:
            yslashn = input('\n\"{}\" seems empty. delete (Y/n/q = quit) ?\t'.format(file))
            if yslashn.lower() == 'q':
                break
            elif yslashn.lower() != 'n':
                os.rmdir(the_dir + '/' + file)
                print('deleted {}'.format(the_dir + '/' + file))