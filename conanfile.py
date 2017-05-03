from nxtools import NxConanFile
from conans import CMake,tools


class GtestConan(NxConanFile):
    name = "gtest"
    version = "1.8.0"
    license = "https://raw.githubusercontent.com/google/googletest/master/googletest/LICENSE"
    url = "https://github.com/hoxnox/conan-gtest"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared":[True, False], "with_gmock":[True, False]}
    default_options = "shared=True", "with_gmock=False"
    build_policy = "missing"
    description = "Google testing framework."

    def do_source(self):
        self.retrieve("58a6f4277ca2bc8565222b3bbd58a177609e9c488e8a72649359ba51450db7d8",
                [
                    "vendor://google/googletest/googletest-release-{v}.tar.gz".format(v=self.version),
                    "https://github.com/google/googletest/archive/release-{v}.tar.gz".format(v=self.version)
                ], "gtest-{v}.tar.gz".format(v=self.version))

    def do_build(self):
        cmake = CMake(self)
        cmake.build_dir = "{staging_dir}/src".format(staging_dir=self.staging_dir)
        tools.untargz("gtest-{v}.tar.gz".format(v=self.version), cmake.build_dir)
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

