# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.packages.ip.package import Ip as BuiltinIp

from spack.package import *


class Ip(BuiltinIp):

    variant("authtokenfile", default="unset")
    variant("ctest_site", default="unset")
    variant("cdash_script_path", default="unset")

    depends_on("valgrind", type=("build"))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            # JCSDA repo only; main Spack repo should just use `ctest("-L", "NO_INPUT_DATA")`
            if self.spec.satisfies("+alltests") or self.spec.satisfies("@:5.2"):
                ctest(
                    "-VV",
                    "--test-dir", self.build_directory,
                    "-S", self.spec.variants["cdash_script_path"].value,
                    "-DCTEST_PROJECT_NAME=NCEPLIBS-ip",
                    f"-DCTEST_SOURCE_DIRECTORY={self.stage.source_path}",
                    f"-DCTEST_BINARY_DIRECTORY={self.build_directory}",
                    "-DAUTH_TOKEN_FILE=" + self.spec.variants["authtokenfile"].value,
                    "-DCTEST_SITE=" + self.spec.variants["ctest_site"].value,
                )
            else:
                ctest(
                    "-S", self.spec.variants["cdash_script_path"].value,
                    "-DCTEST_PROJECT_NAME=NCEPLIBS-ip",
                    f"-DCTEST_SOURCE_DIRECTORY={self.stage.source_path}",
                    f"-DCTEST_BINARY_DIRECTORY={self.build_directory}",
                    "-DAUTH_TOKEN_FILE=" + self.spec.variants["authtokenfile"].value,
                    "-DCTEST_SITE=" + self.spec.variants["ctest_site"].value,
                    "-L", "NO_INPUT_DATA",
                )
            cmake("--install", self.build_directory)
