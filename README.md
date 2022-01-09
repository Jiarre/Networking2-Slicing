# Networking 2 project

## Files description
A brief description for each file in the repo:
- `controller.py`: Ryu controller to handle voip communication
- `flowvisor.sh`: bash script to load flowvisor configuration 
- `it.py`: Ryu controller to handle IT Support slice
- `mn_topo.py`: Network Topology
- `office1.py`: Ryu controller to handle office 1 slice
- `office2.py`: Ryu controller to handle office 2 slice
- `office3.py`: Ryu controller to handle office 3 slice
- `README.md`: this README file
- `run_controllers.sh`: bash script to start Ryu controllers
- `Schema Topologia.png`: graphical representation of network topology
- `send.py`: Python script to test ping and iperf utilities
- `sshsocket.py`: listener for ssh service
- `voipsocket.py`: listener for voip service

<br>

## How to Use
- Start Vagrant
```
vagrant up comnetsemu
```

- Start mininet
```
sudo python3 mn_topo.py
```

- Move the controller scripts in the same folder as "run_controller.sh"
```
mv office1.py office2.py office3.py it.py controller.py ~/Networking2/
```

- Put the flowvisor script into /home/vagrant/comnetsemu/app/realizing_network_slicing/slicing_scripts
```
cp flowvisor.sh ../comnetsemu/app/realizing_network_slicing/slicing_scripts/
```

- cd into /home/vagrant/flowvisor_patch/
```
cd ../flowvisor_patch/
```

- build and run flowvisor
```
./build_flowvisor_image.sh
./run_flowvisor_container.sh 
```

- once in the container cd into "/root/slicing_scripts" and execute flowvisor.sh
```
cd /root/slicing_scripts
./flowvisor.sh
```

- In another terminal execute run_controller.sh
```
./run_controller.sh
```

- Enjoy!
