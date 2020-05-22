cmake_minimum_required(VERSION 2.8.12)
project(Mstar_pybind)

add_subdirectory(pybind11)
add_subdirectory(Mstar)
pybind11_add_module(Mstar_cpp Mstar_pybind.cpp)