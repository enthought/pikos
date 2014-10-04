"%sdkver%" -q -version:v7.0
setenv /x64
if %cython% EQU "true" pip install cython
pip install -r requirements.txt
