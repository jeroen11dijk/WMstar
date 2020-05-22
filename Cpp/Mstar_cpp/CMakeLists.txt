cmake_minimum_required(VERSION 2.8.12)
project(Mstar_cpp)

include_directories(Classes)
add_executable(Mstar Mstar_cpp.cpp main.cpp Classes/Coordinate.cpp Classes/Config_key.cpp Classes/Queue_entry.cpp)