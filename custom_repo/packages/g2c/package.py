# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.packages.g2c.package import G2c as BuiltinG2c

from spack.package import *


class G2c(BuiltinG2c):

    variant("authtokenfile", default="unset")
    variant("ctest_site", default="unset")
    variant("cdash_script_path", default="unset")

    depends_on("valgrind", type=("build"))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            ctest(
                "-VV",
                "--test-dir", self.build_directory,
                "-S", self.spec.variants["cdash_script_path"].value,
                "-DVALGRIND_EXECUTABLE="+self.spec["valgrind"].prefix.bin.valgrind,
                "-DCTEST_PROJECT_NAME=NCEPLIBS-g2c",
                f"-DCTEST_SOURCE_DIRECTORY={self.stage.source_path}",
                f"-DCTEST_BINARY_DIRECTORY={self.build_directory}",
                "-DAUTH_TOKEN_FILE=" + self.spec.variants["authtokenfile"].value,
                "-DCTEST_SITE=" + self.spec.variants["ctest_site"].value,
            )
            cmake("--install", self.build_directory)
