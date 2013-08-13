#!/bin/sh

PYTHONPATH=$PYTHONPATH:"/home/mihai/allypy-workspace/Ally-Py/components"
PYTHONPATH=$PYTHONPATH:"/home/mihai/allypy-workspace/Ally-Py/components/ally"
PYTHONPATH=$PYTHONPATH:"/home/mihai/allypy-workspace/Ally-Py/components/ally-plugin"
PYTHONPATH=$PYTHONPATH:"/home/mihai/allypy-workspace/Ally-Py/components/ally-api"
PYTHONPATH=$PYTHONPATH:"/home/mihai/allypy-workspace/Ally-Py/components/ally-core"

export PYTHONPATH
echo $PYTHONPATH

idle3 -r "/home/mihai/allypy-workspace/Ally-Py/superdesk/distribution/application.py" &
