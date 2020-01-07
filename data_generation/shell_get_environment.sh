 #!/usr/bin/env bash
# for lab desktop
for i in  5
do
port=`expr ${i} + 19994`
cd ..
cd V-REP/
gnome-terminal -x bash -c "./vrep.sh -gREMOTEAPISERVERSERVICE_${port}_FALSE_TRUE ../data_generation/simulation/simulation_new_calibration.ttt; exec bash"

sleep 3
cd ..
cd data_generation/
# start=`expr ${i} \* 5000`
gnome-terminal -x bash -c "python main_calibration.py -n 100 -o 0 -p ${port}; exec bash"

done
