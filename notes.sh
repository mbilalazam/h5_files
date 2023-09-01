## MiniRun3.1 FHC Files
https://portal.nersc.gov/project/dune/data/2x2/simulation/productions/MicroRun3.1_1E18_FHC/

## MiniRun3.1 RHC Files
https://portal.nersc.gov/project/dune/data/2x2/simulation/productions/MiniRun3_1E19_RHC/

## MiniRun4 RHC Files
https://github.com/DUNE/2x2_sim/wiki/MiniRun4-file-locations
cd /pnfs/dune/tape_backed/users/mkramer/prod/MiniRun4/MiniRun4_1E19_RHC/MiniRun4_1E19_RHC.flow/FLOW/

## To download multiple files from the MiniRun3.1 FHC link
wget https://portal.nersc.gov/project/dune/data/2x2/simulation/productions/MicroRun3.1_1E18_FHC/MicroRun3.1_1E18_FHC.flow/FLOW/MicroRun3.1_1E18_FHC.flow.0000{0..11}.FLOW.h5

## To download multiple files from the MiniRun4 RHC link
wget https://portal.nersc.gov/project/dune/data/2x2/simulation/productions/MiniRun4_1E19_RHC/MiniRun4_1E19_RHC.flow/FLOW/MiniRun4_1E19_RHC.flow.0000{0..11}.FLOW.h5

## My Directory 
cd /dune/app/users/mazam/working_area/dunendlar_multiplicity/bilal_work/inProgress/MiniRun4_RHC

## To create python files
gedit name.py

## To run python files
python name.py

## Size of all files in a directory in MBs
ls -lh --block-size=M

## Zip any file to reduce size
tar czvf data.tar.gz data.txt


