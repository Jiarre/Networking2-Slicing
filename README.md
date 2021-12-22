# Networking 2 project

## How to Use
- Start mininet
```
sudo python3 mn_topo.pt
```

- Move the 3 controller scripts in the same folder as "run_controller.sh"
```
mv office1.py office2.py office3.py administration.py it.py controller.py ~/Networking2/
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
