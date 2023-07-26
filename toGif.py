'''
[file name]
[project]
Author: miles at hyperlightcorp dot com
Created: [YYYY-mm-dd]
Modified: [YYYY-mm-dd]

i literally copied this from
https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python

1--------10--------20--------30--------40--------50--------60--------70--------
'''
import os
import imageio
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
  
  pathWithImages = \
    "C:/Users/miles.HYPERLIGHT/HyperLight Corporation/Products - General/"+\
    "+NewFileSystem/Device Components/Mode Converter/"+\
    "20220907_cladding_h_sweep_bgN_1p44/simulation/data_softlinks/"
  images = []
  os.chdir(pathWithImages)
  filenames = os.listdir()
  for filename in filenames:
    # print("4: ",filename[-4:])
    # print("8: ",filename[-8:])
    # print("11: ",filename[-11:])
    # print("15: ",filename[-15:])

    if filename[-11:].lower() == "rawdata.png" or \
      filename[-15:].lower() == "rawdata_fAx.png":
        images.append(imageio.v3.imread(filename))
    #end if filename[-4] == ".png"

  #end for filename in filenames
  imageio.mimsave('C:/Users/miles.HYPERLIGHT/Desktop/anim.gif', images)
  
  import glob
  from PIL import Image
  
  # filepaths
  fp_in = filenames
  fp_out = "/path/to/image.gif"
  
  # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
  imgs = (Image.open(f) for f in sorted(glob.glob(fp_in)))
  img = next(imgs)  # extract first image from iterator
  img.save(fp=fp_out, format='GIF', append_images=imgs,
           save_all=True, duration=200, loop=0)
  
  

  # with imageio.get_writer(pathWithImages + '/anim.gif', mode='I') as writer:
  #     for filename in filenames:
  #         image = imageio.v2.imread(filename)
  #         writer.append_data(image)
  
  
  
# end if __name__ == "__main__"