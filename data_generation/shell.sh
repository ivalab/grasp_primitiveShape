#!/usr/bin/env bash
# for lab desktop
for i in  0 1 2 3 4  
do
port=`expr ${i} + 1984`
cd ..
cd V-REP/
gnome-terminal -x bash -c "./vrep.sh -h -gREMOTEAPISERVERSERVICE_${port}_FALSE_TRUE ../data_generation/simulation/simulation_NEW.ttt; exec bash"

sleep 5
cd ..
cd data_generation/
start=`expr ${i} \* 5000`
gnome-terminal -x bash -c "python main_New.py -n 5000 -o ${start} -p ${port}; exec bash"

done
