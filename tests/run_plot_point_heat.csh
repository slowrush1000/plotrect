#!/usr/bin/csh -f
set dir         = "/media/PROJECT02/project/plotrect"
set input_file  = "${dir}/tests/test_xyz.01.5.10.txt"
python3 ${dir}/src/plotpointheat.py \
test_xyz.01.5.10.output    \
${input_file}       \
0 1 2               \
5 10                \
0.0 0.0 4.0 9.0    \
-max
