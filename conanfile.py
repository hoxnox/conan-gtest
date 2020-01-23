from nxtools import NxConanFile
from conans import CMake,tools


class GtestConan(NxConanFile):
    name = "gtest"
    version = "1.10.0"
    license = "https://raw.githubusercontent.com/google/googletest/master/googletest/LICENSE"
    url = "https://github.com/hoxnox/conan-gtest"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared":[True, False], "with_gmock":[True, False]}
    default_options = "shared=True", "with_gmock=False"
    build_policy = "missing"
    description = "Google testing framework."

    def do_source(self):
        self.retrieve("9dc9157a9a1551ec7a7e43daea9a694a0bb5fb8bec81235d8a1e6ef64c716dcb",
                [
                    "vendor://google/googletest/googletest-release-{v}.tar.gz".format(v=self.version),
                    "https://github.com/google/googletest/archive/release-{v}.tar.gz".format(v=self.version)
                ], "gtest-{v}.tar.gz".format(v=self.version))

    def do_build(self):
        cmake = CMake(self)
        tools.untargz("gtest-{v}.tar.gz".format(v=self.version))
        cmake.configure(defs={
                "BUILD_GTEST":"1",
                "BUILD_GMOCK":"1" if self.options.with_gmock else "0",
                "CMAKE_INSTALL_PREFIX": self.staging_dir,
                "CMAKE_INSTALL_LIBDIR": "lib",
                "BUILD_SHARED_LIBS": "1" if self.options.shared else "0"
            }, source_dir="googletest-release-{v}".format(v=self.version))
        cmake.build(target="install")

    def do_package_info(self):
        self.cpp_info.libs = ["gtest", "gtest_main"]

