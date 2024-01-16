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

## Locations of PicoRun4_1E17_RHC Flow files (update after MiniRun4_RHC):
FNAL: /pnfs/dune/tape_backed/users/mkramer/prod/PicoRun4/PicoRun4_1E17_RHC/PicoRun4_1E17_RHC.flow/FLOW
Web: https://portal.nersc.gov/project/dune/data/2x2/simulation/productions/PicoRun4_1E17_RHC/PicoRun4_1E17_RHC.flow/FLOW/
wget https://portal.nersc.gov/project/dune/data/2x2/simulation/productions/PicoRun4_1E17_RHC/PicoRun4_1E17_RHC.flow/FLOW/PicoRun4_1E17_RHC.flow.00000.FLOW.h5
base_path = "/pnfs/dune/tape_backed/users/mkramer/prod/PicoRun4/PicoRun4_1E17_RHC/PicoRun4_1E17_RHC.flow/FLOW"
filenames = [f"{base_path}/PicoRun4_1E17_RHC.flow.{i:05}.FLOW.h5" for i in range(10)]


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


## To copy an entire folder from DUNE GPVM to my local machine
scp -r mazam@dunegpvm13.fnal.gov:<path_on_gpvm> <path_on_local_machine>
scp -r mazam@dunegpvm13.fnal.gov:/dune/app/users/mazam/working_area/dunendlar_multiplicity/bilal_work/inProgress/MiniRun4_RHC/mult/2d/ppt/sep22 .

## To copy some files ending on .h5 from DUNE GPVM to my local machine
scp -r mazam@dunegpvm13.fnal.gov:/dune/data/users/drielsma/minirun4/output_ana/$(ls /dune/data/users/drielsma/minirun4/output_ana/*.h5 | shuf -n 100) /home/bilal/working/MLreco/output_ana/


## To copy an entire folder from my local machine to DUNE GPVM 
scp -r /path/to/your/local/folder mazam@dunegpvm11.fnal.gov:/remote/destination/path



## To copy just one file from DUNE GPVM to my local machine
scp mazam@dunegpvm11.fnal.gov:/dune/app/users/mazam/working_area/dunendlar_multiplicity/out_gen.root .

## Path to access folder using This PC
\\wsl.localhost\Ubuntu\home\bilal
