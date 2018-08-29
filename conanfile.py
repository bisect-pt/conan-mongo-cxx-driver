#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class MongoCDriverConan(ConanFile):
    name = "mongo-cxx-driver"
    version = "3.3.0"
    description = "C++ Driver for MongoDB"
    url = "https://github.com/mongodb/mongo-cxx-driver"
    license = "https://github.com/mongodb/mongo-cxx-driver/blob/r{0}/LICENSE".format(version)
    settings = "os", "compiler", "arch", "build_type"
    options = {"use_17_standard": [True, False]}
    default_options = "use_17_standard=True"
    requires = 'mongo-c-driver/[~=1.11]@bisect/stable'
    exports_sources = ["CMakeLists.txt", "diff.patch"]
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    generators = "cmake"

    def source(self):
        tools.get("https://github.com/mongodb/mongo-cxx-driver/archive/r{0}.tar.gz".format(self.version))
        extracted_dir = "mongo-cxx-driver-r{0}".format(self.version)
        os.rename(extracted_dir, self.source_subfolder)
        tools.patch(base_path=self.source_subfolder, patch_file="diff.patch")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = True # todo: Support static

        if self.options.use_17_standard:
            cmake.definitions["CMAKE_CXX_STANDARD"] = "17"
            cmake.definitions["BSONCXX_POLY_USE_STD"] = True
        else:
            cmake.definitions["CMAKE_CXX_STANDARD"] = "11"
            cmake.definitions["BSONCXX_POLY_USE_BOOST"] = True
            cmake.definitions["BSONCXX_POLY_USE_STD"] = False
            cmake.definitions["BSONCXX_POLY_USE_MNMLSTC"] = False

        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True

        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def requirements(self):
        if not self.options.use_17_standard:
            self.requires('boost/[>1.66.0]@conan/stable')

    def package(self):
        self.copy(pattern="LICENSE*", src=self.source_subfolder)
        # cmake installs all the files

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if tools.os_info.is_linux:
            self.cpp_info.libs.append("resolv")
