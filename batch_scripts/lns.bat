@echo off

setlocal
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
    
    :processargs
        set ARG=%1
        if defined ARG (
            REM echo "from path = %FROM_PATH%"
            REM echo "to path = %TO_PATH%"
            if %LAST_WAS_FROM%==1 (
                echo last was from
                set FROM_PATH=%~f1
                set LAST_WAS_FROM=0
            ) else if "%ARG%"=="--from" (
                set LAST_WAS_FROM=1
                echo fucj
            )else if %LAST_WAS_TO%==1 (
                echo last was to
                set TO_PATH=%~f1
                set LAST_WAS_TO=0
            ) else if "%ARG%"=="--to" (
                set LAST_WAS_TO=1
                echo t00t
            )
            shift
            goto processargs
        )
    
    :args_done

    powershell New-Item -Itemtype SymbolicLink -Path %TO_PATH% -Target %FROM_PATH%
    
endlocal