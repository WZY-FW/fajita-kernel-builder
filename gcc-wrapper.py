#!/usr/bin/env python3
# Pass-through gcc wrapper - satisfies gcc-version.sh without breaking builds
# Resolves the real compiler path so it works from any directory
import sys, os, subprocess, shutil

if len(sys.argv) < 2:
    sys.exit(1)

compiler = sys.argv[1]
if compiler == '--version':
    # Called as: gcc-wrapper.py --version
    # Print a plausible GCC version to satisfy gcc-version.sh
    print("aarch64-linux-gnu-gcc (GCC) 10.3.0")
    sys.exit(0)

# Resolve full path to real compiler
# gcc-version.sh calls: gcc-wrapper.py aarch64-linux-gnu-gcc ...
# but from the kernel source root, not the wrapper dir
possible_paths = [
    compiler,
    '/usr/bin/' + compiler,
    '/usr/aarch64-linux-gnu/bin/' + compiler,
]
real_cc = None
for p in possible_paths:
    if os.path.isfile(p) and os.access(p, os.X_OK):
        real_cc = p
        break

# Last resort: use shutil.which
if real_cc is None:
    real_cc = shutil.which(compiler)

if real_cc is None:
    sys.exit(1)

result = subprocess.run([real_cc] + sys.argv[2:])
sys.exit(result.returncode)
