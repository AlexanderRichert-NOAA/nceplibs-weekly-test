This workflow is intended to run through cron to build NCEPLIBS on Acorn weekly:
```console
NOSCRUB=...
PTMP=...
24 17 * * MON $NOSCRUB/nceplibs-weekly-test/nceplibs_weekly_test.sh > $PTMP/nceplibs-weekly-test/logs/$(date +\%Y\%m\%d).cron 2>&1
```

Updated the CDash dashboards requires that ~/.config/nceplibsweeklybuild/tokenpaths.yaml be populated:
```yaml
packages:
  bacio:
    require:
    - authtokenfile=~/.config/nceplibsweeklybuild/cdash.txt
    - ctest_site="Acorn weekly build"
    - cdash_script_path=${NOSCRUB}/nceplibs-weekly-test/ci-cdash/RunCDash.cmake
  g2c:
    require:
    - authtokenfile=~/.config/nceplibsweeklybuild/cdash.txt
    - ctest_site="Acorn weekly build"
    - cdash_script_path=${NOSCRUB}/nceplibs-weekly-test/ci-cdash/RunCDash.cmake
  ip:
    require:
    - authtokenfile=~/.config/nceplibsweeklybuild/cdash.txt
    - ctest_site="Acorn weekly build"
    - cdash_script_path=${NOSCRUB}/nceplibs-weekly-test/ci-cdash/RunCDash.cmake
  w3emc:
    require:
    - authtokenfile=~/.config/nceplibsweeklybuild/cdash.txt
    - ctest_site="Acorn weekly build"
    - cdash_script_path=${NOSCRUB}/nceplibs-weekly-test/ci-cdash/RunCDash.cmake
```
