cmake_minimum_required(VERSION 2.8.12)
project(Mstar_cpp)

include_directories(source)
add_executable(Mstar Mstar_cpp.cpp main.cpp source/Coordinate.cpp source/Config_key.cpp source/Queue_entry.cpp)