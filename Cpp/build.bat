SET pypath="C:\Users\Admin\AppData\Local\Programs\Python"

mkdir build_py37
cd build_py37
cmake .. -DPYTHON_EXECUTABLE="C:\Users\Jeroen\AppData\Local\Programs\Python\Python37\python.exe" .. -G"Visual Studio 15 2017 Win64"
cmake --build . --config Release
for /R . %%f in (*.pyd) do copy "%%f" ..
cd ..

pause