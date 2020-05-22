cmake_minimum_required(VERSION 2.8.12)
project(Mstar_cpp)

include_directories(source)
add_executable(Mstar Mstar.cpp main.cpp source/Coordinate.cpp source/Config_key.cpp source/Queue_entry.cpp inc/Utils.h source/Utils.cpp inc/Graph.h source/Graph.cpp)