cmake_minimum_required(VERSION 2.8.12)
project(Mstar_pybind)

add_subdirectory(pybind11)
pybind11_add_module(Mstar_pybind Mstar_pybind.cpp Mstar/Mstar.cpp Mstar/source/Coordinate.cpp Mstar/source/Config_key.cpp Mstar/source/Queue_entry.cpp Mstar/source/Utils.cpp Mstar/source/Graph.cpp)