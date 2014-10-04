"%sdkver%" -q -version:v7.0 || exit 1
setenv /x64 || exit 1
python setup.py test || exit 1
