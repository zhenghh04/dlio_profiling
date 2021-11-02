module load conda/2021-09-22
conda activate
# Loading Darshan
module load darshan
export DARSHAN_DISABLE_SHARED_REDUCTION=1
export DXT_ENABLE_IO_TRACE=1
export LD_PRELOAD="$DARSHAN_PRELOAD $LD_PRELOAD"
export DARSHAN_DIR=$(dirname $(dirname $DARSHAN_PRELOAD))
[[ -e tmp ]] || mkdir tmp
git clone git@github.com:zhenghh04/vanidl.git tmp/vanidl
cd tmp/vanidl
python setup.py build
python setup.py install --user
cd -
