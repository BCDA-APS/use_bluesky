#!/bin/bash

BLUESKY_ROOT=$HOME/Apps/BlueSky

#----------------------------------------------------
# make Jupyter Kernel (required to workaround Jupyter
# not using IPython profiles

echo "Creating directory BlueSky kernel for Jupyter"
KERNEL_DIR=$BLUESKY_ROOT/share/jupyter/kernels/python3-BS
if [ ! -d "$KERNEL_DIR" ]
then
	echo "Kernel directory doesn't exist. Creating one"
	mkdir ${KERNEL_DIR}
else
	echo "Kernel directory already exists."
fi

KERNEL_FILE=$KERNEL_DIR/kernel.json

if [ ! -f "$KERNEL_FILE" ]
then
	echo "Creating kernel file"
else
	echo "Overwriting old kernel file"
fi

/bin/cat <<EOM >$KERNEL_FILE
{
 "argv": [
  "${BLUESKY_ROOT}/bin/python",
  "-m",
  "ipykernel_launcher",
  "--profile=BS_jupyter",
  "-f",
  "{connection_file}"
 ],
 "display_name": "Python 3 - BlueSky",
 "language": "python"
}
EOM

