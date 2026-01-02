# <filename>.py
# <project>
# Author: miles at hyperlightcorp dot com
# Created: <date>

# <description>

# -------10--------20--------30--------40--------50--------60--------70--------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import subprocess
import pathlib

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

home = pathlib.Path.home()
git_folder_default = pathlib.Path(home / "__git_repos/hl_cad")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/user~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~main~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == "__main__":
    
    repo_list = []
    not_utd_list = []
    details_list = []
    
    gitdir = pathlib.Path(input(f"what dir to use?\ndefault: {git_folder_default}\n_ "))
    if gitdir == pathlib.Path(""):
        gitdir = git_folder_default
    elif not(gitdir.is_dir()):
        if pathlib.Path(home / "__git_repos" / gitdir).is_dir():
            gitdir = pathlib.Path(home / "__git_repos" / gitdir)
        elif pathlib.Path(home / "__git_repos/hl_cad" / gitdir).is_dir():
            gitdir = pathlib.Path(home / "__git_repos/hl_cad" / gitdir)
        elif pathlib.Path(home / gitdir).is_dir():
            gitdir = pathlib.Path(home / gitdir)
        else:
            no_dir_str = f'couldnt find path:\n{gitdir}\nquitting.'
            print(no_dir_str)
            gitdir = None
    
    if gitdir is not None:
        for item in gitdir.iterdir():
            if item.is_dir():
                if pathlib.Path(item / ".git") in item.iterdir():
                    repo_list.append(item)
        
        for repo in repo_list:
            # fetcharoo = subprocess.run(
            subprocess.run(
                (
                    "git",
                    "-C",
                    repo,
                    "fetch",
                ),
                capture_output=True,
                text=True,
            )#.stdout
            
            utd_status = False # reflects whether git says a repo is up to date
            outputski = subprocess.run(
                (
                    "git",
                    "-C",
                    repo,
                    "status",
                ),
                capture_output=True,
                text=True,
            ).stdout
            
            outputski_split = outputski.split("\n")
            details_list.append([repo, "", ""])
            for line in outputski_split:
                if line[:10].lower() == "on branch ":
                    details_list[-1][1] = outputski_split[0][10:]
                
                if outputski_split[1][:25].lower() != 'your branch is up to date':
                    details_list[-1][2] = outputski
                    utd_status = True
                else:
                    utd_status = False
                
            if utd_status:
                not_utd_list.append(details_list[-1])
    
    if len(not_utd_list) > 0:
        utd_str = f'\nin the folder\n{gitdir}\n\nthese repos are NOT listed as '+\
            f'\"up to date\" by git:\n'
        print(utd_str)
        for repo in not_utd_list:
            repo_info =\
                f"{repo[0]} ~~~~~\n"+\
                f"branch: {repo[1]}\n"+\
                f"message:\n{repo[2]}\n"
            print(repo_info)
        
        yslashn = input("pull all? (y/N)\n_ ")
        if yslashn.lower() == 'y':
            for repo in not_utd_list:
                subprocess.run(
                    (
                        "git",
                        "-C",
                        repo[0],
                        "pull",
                    ),
                    # capture_output=True,
                    text=True,
                )
        else:
            print("not pulling.")
        
    else:
        utd_str = f'\nin the folder\n{gitdir}\n\nall repos are listed as '+\
            f'\"up to date\" by git.\nhere is a list of currently checked-out branches:\n'
        
        print(utd_str)
        for repo in details_list:
            print(f"{str(repo[0]):50}: {repo[1]}")
    
    print('done.')
#end if __name__ == "__main__"
