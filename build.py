#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(archs=["x86_64"], build_policy="missing")
    builder.add_common_builds()
    builder.add({}, {"mongo-cxx-driver:use_17_standard" : False}, {}, {})
    builder.add({}, {"mongo-cxx-driver:use_17_standard" : True, "mongo-cxx-driver:use_boost" : True}, {}, {})
    builder.run()
