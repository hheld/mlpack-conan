from conans import ConanFile, CMake, tools


class MlpackConan(ConanFile):
    name = "mlpack"
    version = "4.0.0"
    license = "BSD-3-Clause"
    author = "Harald Held <harald.held@gmail.com>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "mlpack is an intuitive, fast, and flexible header-only C++ machine learning library with bindings to other languages."
    topics = ("machine learning")
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"

    requires = ["armadillo/10.7.3", "ensmallen/2.19.0", "cereal/1.3.2"]
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True, "armadillo:use_hdf5": False}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run(f"git clone -b {self.version} https://github.com/mlpack/mlpack.git")

    def build(self):
        cmake = CMake(self)

        cmake.definitions["ARMADILLO_INCLUDE_DIR"] = self.dependencies["armadillo"].cpp_info.includedirs[0]
        cmake.definitions["ARMADILLO_LIBRARY"] = self.dependencies["armadillo"].cpp_info.libs
        cmake.definitions["ENSMALLEN_INCLUDE_DIR"] = self.dependencies["ensmallen"].cpp_info.includedirs[0]
        cmake.definitions["CEREAL_INCLUDE_DIR"] = self.dependencies["cereal"].cpp_info.includedirs[0]
        cmake.definitions["BUILD_CLI_EXECUTABLES"] = "OFF"
        
        cmake.configure(source_folder="mlpack")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="mlpack/src")
        self.copy("*.hpp", dst="include", src="mlpack/src")
