@echo off

setlocal
    if "%1"=="--test" (
        set TEST=1
        shift
    )
    if defined TEST (
        echo TEST = %TEST%
    )
    
    set ARG2=%2
    set ARG3=%3
    
    if not defined ARG3 (
        if defined ARG2 (
            set TWO_ARGS=1
        )
    )
    
    if defined TWO_ARGS (
        set FROM_PATH=%~f1
        set TO_PATH=%~f2
        goto args_done
    )
    
    set LAST_WAS_FROM=0
    set LAST_WAS_TO=0
    
    :processargs
        set ARG=%1
        if not defined ARG (
            goto args_done
        )
        if %LAST_WAS_FROM%==1 (
            set FROM_PATH=%~f1
            set FROM_PATH_FILENAME=%~nx1
            set LAST_WAS_FROM=0
        ) else if %ARG%==--from (
            set LAST_WAS_FROM=1
        ) else if %LAST_WAS_TO%==1 (
            set TO_PATH=%~f1
            set LAST_WAS_TO=0
        ) else if "%ARG%"=="--to" (
            set LAST_WAS_TO=1
        )
        shift
        goto processargs
    
    :args_done
    echo:
    echo FROM_PATH = %FROM_PATH%
    echo TO_PATH = %TO_PATH%
    
    for /f %%i in (
        'powershell Test-Path -Path %TO_PATH% -PathType Container'
    ) do (
        set TO_IS_A_FOLDER=%%i
    )
    
    if defined TO_IS_A_FOLDER (
        echo %TO_PATH% is a directory.
        echo Enter a filename for the softlink, or "e" to exit
        set /P TO_PATH_INPUT=[%FROM_PATH_FILENAME%]
    )
    
    if defined TO_PATH_INPUT (
        goto new_path_i_guess
    ) else if defined TO_IS_A_FOLDER (
        set TO_PATH_INPUT=%FROM_PATH_FILENAME%
        goto new_path_i_guess
    ) else (
        goto final_command
    )
    
    :new_path_i_guess
        if %TO_PATH_INPUT%==e (
            goto end_marker
        ) else (
            set TO_PATH=%TO_PATH%\%TO_PATH_INPUT%
        )

    
    :final_command
    if defined TEST (
        echo:
        echo test:
        echo powershell New-Item -Itemtype SymbolicLink -Path %TO_PATH% -Target %FROM_PATH%
    ) else (
        powershell New-Item -Itemtype SymbolicLink -Path %TO_PATH% -Target %FROM_PATH%
    )
    
    :end_marker
endlocal