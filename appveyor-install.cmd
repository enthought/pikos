"%sdkver%" -q -version:v7.0
call setenv /x64
if %cython%=='true' ("%pip%" install cython)
"%pip%" install -r requirements.txt
