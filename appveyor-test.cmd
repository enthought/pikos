"%sdkver%" -q -version:v7.0
call setenv /x64
python -version
python setup.py test || exit 1
