@echo off

REM script to create a symbolic link more easily than the default windows method.
REM if more than 2 args are specified, the script will look for
    REM --from : to precede the file path to create a link for.
    REM --to : to precede the file path of the new link.
REM if exactly 2 args are specified, it will be assumed that the first one is the
REM "--from" arg, and the second one is the "--to" arg.

REM you may need to be admin for this script to work.

setlocal
    if "%1"=="--help" (
        echo script to create a symbolic link more easily than the default windows method.
        echo:
        echo if more than 2 args are specified, the script will look for these flags:
        echo     --from : to precede the file path to create a link for.
        echo     --to : to precede the file path of the new link.
        echo:
        echo if exactly 2 args are specified, it will be assumed that the first one is the
        echo "--from" arg, and the second one is the "--to" arg.
        echo:
        echo you may need to be admin for this script to work.
        
        goto end_marker
    )

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