"%sdkver%" -q -version:v7.0 || exit 1
setenv /x64 || exit 1
if %cython% EQU "true" pip install cython || exit 1
pip install -r requirements.txt" || exit 1
