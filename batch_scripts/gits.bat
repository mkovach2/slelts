@echo off

setlocal
	set CURRENT_DIR=%cd%

	if "%1"=="" (
		set FILE_TO_RUN=%CURRENT_DIR%
	) else (
		set FILE_TO_RUN=%1
	)
	
	REM guess i have to do this for a variable to refresh
	if not "%1"=="" (
		echo:
		echo ~~~~~
		echo git -C "%FILE_TO_RUN%" status
		echo ~~~~~
		echo:
	)

	git -C "%FILE_TO_RUN%" status
	
	echo done.

endlocal