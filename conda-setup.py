import os

_res = get_ipython().run_cell("""
%env PYTHONPATH=
!echo $PYTHONPATH
""")
if _res != 0:
    raise Exception("get_ipython error")

if os.system("bash ./__conda_init.sh.sh") != 0:
    raise Exception("ERROR: conda_init script, see output")

# todo make this just done in python
_res = get_ipython().run_cell("""
ls /usr/local/lib/python3.6/dist-packages
""")
if _res != 0:
    raise Exception("get_ipython error")

import sys
_ = (sys.path.append("/usr/local/lib/python3.6/site-packages"))