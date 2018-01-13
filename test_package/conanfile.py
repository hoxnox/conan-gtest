from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "hoxnox")

class SnappyTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "gtest/1.8.0@%s/%s" % (username, channel)
    #default_options = "gtest:system=True", "gtest:root=/tmp/sss", "gtest:shared=true"
    #default_options = "gtest:shared=True"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        self.run('cmake "%s" %s' % (self.source_folder, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        os.chdir("bin")
        self.run(".%stestapp" % os.sep)
