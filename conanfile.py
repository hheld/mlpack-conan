from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeToolchain, CMakeDeps


class MlpackConan(ConanFile):
    name = "mlpack"
    version = "4.0.0"
    license = "BSD-3-Clause"
    author = "Harald Held <harald.held@gmail.com>"
    url = "https://github.com/hheld/mlpack-conan"
    description = "mlpack is an intuitive, fast, and flexible header-only C++ machine learning library with bindings to other languages."
    topics = ("machine learning")
    settings = "os", "compiler", "build_type", "arch"

    requires = ["armadillo/11.4.3", "ensmallen/2.19.0", "cereal/1.3.2"]
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True, "armadillo:use_hdf5": False}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run(f"git clone -b {self.version} https://github.com/mlpack/mlpack.git")

    def generate(self):
        tc = CMakeToolchain(self, generator="Ninja")
        tc.cache_variables["ARMADILLO_INCLUDE_DIR"] = self.dependencies["armadillo"].cpp_info.includedirs[0]
        tc.cache_variables["ARMADILLO_LIBRARY"] = self.dependencies["armadillo"].cpp_info.libs
        tc.cache_variables["ENSMALLEN_INCLUDE_DIR"] = self.dependencies["ensmallen"].cpp_info.includedirs[0]
        tc.cache_variables["CEREAL_INCLUDE_DIR"] = self.dependencies["cereal"].cpp_info.includedirs[0]
        tc.cache_variables["BUILD_CLI_EXECUTABLES"] = "OFF"
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)

        cmake.configure(build_script_folder="mlpack")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="mlpack/src")
        self.copy("*.hpp", dst="include", src="mlpack/src")

    def layout(self):
            cmake_layout(self)