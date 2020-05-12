cmake_minimum_required(VERSION 2.8.12)
project(Mstar_cpp)

add_subdirectory(pybind11)
pybind11_add_module(Mstar_cpp Mstar_cpp.cpp)