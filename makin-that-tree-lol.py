from directory_tree import display_tree

pathe = "C:/Users/miles.HYPERLIGHT/Documents/_git_repos/HyperLightPDK/hlpdk"
savefile = pathe + "/tree.txt"

treetext = display_tree(pathe, string_rep = True)

with open(savefile, 'w', encoding = "utf-8") as tf:
    tf.write(treetext)















