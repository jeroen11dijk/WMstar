cd Cpp
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_GENERATOR_PLATFORM=x64 -B build_py37
cmake --build build_py37 --config Release
cp build_py37/Release/Mstar_cpp.cp37-win_amd64.pyd .