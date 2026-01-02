#!/bin/bash

py_auto(){
    # if a uv-created folder named .venv is located in the parent dir of
    # the python file specified as an inline variable or any of its 
    # parent directories, this function will try to run it with the 
    # python in that virtual environment.  otherwise, itll try to run it
    # with the python specified by _default_python
    
    # _default_python="/usr/bin/python3"
    _default_python="/home/miles/__git_repos/Miles_Scratch/.venv/bin/python"
    _max_folders_up=1000 # just in case lol
    
    if [ ! -e "$1" ]; then
        printf "couldnt find a python file at:\n$1\nexiting.\n"
    else
        file_to_run="$(realpath "$1")"
        parent_dir="$(dirname "$file_to_run")"
        initial_pwd="$(pwd)"
        
        venv_found=0
        counter=0
        while [[ 
            "$parent_dir" != "/"  && 
            venv_found -eq 0 && 
            counter -lt _max_folders_up 
        ]]; do
            counter=$((counter + 1))
            
            ## printf "counter = $counter\n"
            ## printf "venv_found = $venv_found\n"
            ## printf "parent_dir = $parent_dir\n"
            
            if [ -d "$parent_dir/.venv" ]; then
                venv_found=1
            else
                parent_dir="$(dirname "$parent_dir")"
            fi
        done
        
        if [[ venv_found -eq 0 ]]; then
            input_str="no .venv found."
            input_str="$input_str  continue with $_default_python ? (Y/n)"
            read -p "$input_str" yslashn
            if [[ $yslashn == [nN] ]]; then
                run_str=0
                printf "done\n"
            else
                run_str="$_default_python $file_to_run"
                printf "$run_str\n"
                cd "$(dirname "$file_to_run")"
            fi
        else
            run_str="$parent_dir/.venv/bin/python $file_to_run"
            printf "$run_str\n"
            cd "$(dirname "$file_to_run")"
        fi
        
        if [[ $run_str != 0 ]]; then
            $run_str
        fi
        
        cd $initial_pwd
    fi
}

# py_auto /home/miles/__git_repos/slelts/get_nutty_plots_different.py
py_auto /home/miles/__git_repos/hl_cad/XX0115/xx0115/reticle.py
# py_auto /home/miles/__git_repos/slelts/git_pull_all.py
# py_auto ~/__git_repos/slelts/git_pull_all.py
