@echo off

setlocal
    REM if a uv-created folder named .venv is located in the parent dir of
    REM the python file specified as an inline variable or any of its 
    REM parent directories, this function will try to run it with the 
    REM python in that virtual environment.  otherwise, itll try to run it
    REM with the python specified by _default_python
	
	set CURRENT_DIR=%cd%
	set FILE_TO_RUN=%~f1
	set DEFAULT_PYTHON=C:\Users\miles\Documents\_git_repos\Miles_Scratch\.venv\Scripts\python.exe
	set PATH_TO_PYTHON=%DEFAULT_PYTHON%
	
	echo:
	echo CURRENT_DIR = %CURRENT_DIR%
	echo FILE_TO_RUN = %FILE_TO_RUN%
	echo:

	for %%I in ("%FILE_TO_RUN%") do (
		set PARENT_FOLDER=%%~dpI
		set PARENT_DRIVE=%%~dI
	)
	REM echo PARENT_FOLDER = %PARENT_FOLDER%
	REM echo PARENT_DRIVE = %PARENT_DRIVE%
	set LOOP_NUMBER=0
	set SAFETY_MAX_LOOPS=20
	REM set SAFETY_MAX_LOOPS=1000
	
	:VENV_LOOP
	REM echo PARENT_FOLDER 1 = %PARENT_FOLDER%
	REM echo LOOP_NUMBER = %LOOP_NUMBER%

	if exist %PARENT_FOLDER%\.venv (
		set PATH_TO_PYTHON=%PARENT_FOLDER%\.venv\Scripts\python.exe
		goto RUN_PYTHON
	) else (
		for %%I in ("%PARENT_FOLDER%\..") do (
			set PARENT_FOLDER=%%~fI
		)
		REM echo PARENT_FOLDER 2 = %PARENT_FOLDER%
	)
	
	if %LOOP_NUMBER% lss %SAFETY_MAX_LOOPS% (
		if "%PARENT_FOLDER%"=="%PARENT_DRIVE%\" (
			goto ERROR_PARENT
		) else (
			set /A LOOP_NUMBER=%LOOP_NUMBER%+1
			goto VENV_LOOP
		)
	)
	
	:ERROR_PARENT
	echo no ".venv" folder found in any parent directory, all the way up to %PARENT_DRIVE%  .
	echo continue using python at
	echo:
	echo %PATH_TO_PYTHON%
	echo:
	
	set /P yslashn=[Y/n]
	
	if not "%yslashn%"=="n" (
		if not "%yslashn%"=="N" (
			goto RUN_PYTHON
		) else (
			goto EXIT_POINT
		)
	) else (
		goto EXIT_POINT
	)
	
	:RUN_PYTHON
	if exist %PATH_TO_PYTHON% (
		echo:
		echo PATH_TO_PYTHON = %PATH_TO_PYTHON%
		echo:
		%PATH_TO_PYTHON% C:\Users\miles\Documents\_git_repos\slelts\obliterate_Unnamed.py
	)
	
	:EXIT_POINT
	echo done.

endlocal
