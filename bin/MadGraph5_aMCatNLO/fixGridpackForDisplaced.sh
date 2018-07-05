#!/bin/bash

#
# Fix the gridpack to generate a displaced vertex for the heavy neutrino
#

home=$(pwd)
gridpack=$(basename $1)
mkdir -p temp_$gridpack
cp $1 temp_$gridpack/$gridpack
cd temp_$gridpack
tar -xaf $gridpack
cp $home/addDisplacedVertex.py .
width=$(awk '/DECAY  9900012/{print $NF}' ./process/Cards/param_card.dat)            # NLO
#width=$(awk '/DECAY  9900012/{print $NF}' ./process/madevent/Cards/param_card.dat)   # LO
echo "Adapting gridpack $gridpack to add displaced vertex based on width $width"
sed -i "s/WIDTH/$width/g" addDisplacedVertex.py
sed -i 's#gzip -d  cmsgrid_final.lhe.gz#gzip -d  cmsgrid_final.lhe.gz\n ./addDisplacedVertex.py ${runname}_final.lhe#g' runcmsgrid.sh
tar cfJ $gridpack mgbasedir runcmsgrid.sh process gridpack_generation.log addDisplacedVertex.py
cd ..
mv temp_$gridpack/$gridpack $1
rm -r temp_$gridpack
