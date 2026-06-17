#!/bin/bash

# Using PBS during `spack install` will break CDash pushes
USE_PBS=${USE_PBS:-NO}

function alert_failure() {
  mail -s 'NCEPLIBS weekly build failure' $(whoami)@noaa.gov  < <(echo "Weekly NCEPLIBS build failed for $SPACK_ENV.")
}

trap alert_failure ERR

set -ex

autoroot=${autoroot:-${PTMP:-/tmp}/nceplibs-weekly-test}
configdir=$(dirname $(realpath $0))
logdir=${configdir}/logs/

mkdir -p ${autoroot}
cd ${autoroot}

if [ ! -d spack-packages ]; then
  git clone --depth 1 https://github.com/JCSDA/spack-packages
fi
if [ ! -d spack ]; then
  git clone --depth 1 https://github.com/spack/spack
  . ./spack/share/spack/setup-env.sh
  spack repo add $(realpath ${autoroot}/spack-packages/repos/spack_repo/builtin)
else
  . ./spack/share/spack/setup-env.sh
fi

spack bootstrap root '$spack/bootstrap'
spack bootstrap now

envname=$(date +%Y%m%d)

spack env create ${envname} ${configdir}/spack.yaml

spack env activate ${envname}

cp -r $configdir/custom_repo ${SPACK_ENV:?}/.

for p in $(grep -oP "[-\w]+@develop" ${SPACK_ENV}/spack.yaml); do spack develop ${p} ; done

# Patch needed for JCSDA repo as of Apr 2025:
#sed -i 's|self\.builder|self.|' $(spack location --package-dir g2)/package.py

spack external find --not-buildable --path /apps/spack/cmake/3.30.5/intel/19.1.3.304/xkpegogpnyae4l2anf6dm77o7ksrez6t/ cmake

if [ ${USE_PBS} == YES ]; then
  cd ${logdir}
  qsub -Wblock=true -N ${envname}.concretize -j oe -A NCEPLIBS-DEV -q dev -l walltime=00:10:00,select=1:ncpus=4:mem=4GB -V -- $(which spack) concretize --jobs 4
else
  spack concretize &> ${logdir}/${envname}.concretize
fi

spack fetch --missing &> ${logdir}/${envname}.fetch

if [ ${USE_PBS} == YES ]; then
  cd ${logdir}
  qsub -Wblock=true -N ${envname}.install -j oe -A NCEPLIBS-DEV -q dev -l walltime=00:55:00,select=1:ncpus=16:mem=8GB -V -- ${configdir}/parallel_install.sh 2 8
else
  ${configdir}/parallel_install.sh 2 3
fi

mail -s 'NCEPLIBS weekly build success' $(whoami)@noaa.gov  < <(echo "Weekly NCEPLIBS build succeeded for $SPACK_ENV.")
