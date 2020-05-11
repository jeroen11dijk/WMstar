#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

#include <string>
#include <utility>

#include <vector>

namespace py = pybind11;

int Jeroen(int a) {
	return a;
}


PYBIND11_MODULE(Mstar_cpp, m) {

    m.doc() = "Car path utilities";
	m.def("Jeroen", &Jeroen);
}