pyNet A Raspberry Pi Intelligent Network

> The folder V1 contains a version of the pyNet which doesn't have an election algorithm such as contesting election but rather each node selects the leader based on the highest last octet of the IP addresses of the hosts on the network


# Development Dependencies

[nmap](https://nmap.org/)

Follow this step to install nmap : [How to install nmap](https://www.raspberrypi.org/documentation/remote-access/ip-address.md)


__### Optional Depencies and tools__

- ## Samba
Samba is used to connect your Raspberry pi to your local network so that way you don't have to issue ssh command or putty each time you want to access your file. It helps you share file between you Raspberry Pi and your PC and use any editor of your choice to develop your python app while running your code on your Pi.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Installation and setup information can be found here : [Setup Samba](https://www.youtube.com/watch?v=iQwWEsuRWUw)

- ## [WebIDE](https://learn.adafruit.com/webide/overview)
WebIDE is a Web Interface you can setup for your Raspberry PI to run and debug your python code running on your Raspberry Pi in real time.
It is straight forward to setup via ssh or terminal on your Raspberry PI.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; WebIDE installation and setup can be found here : [Setup webIDE](https://learn.adafruit.com/webide/installation)


- ## Resources & References:
- [Find Raspberry PI address on local network](https://raspberrypi.stackexchange.com/questions/13936/find-raspberry-pi-address-on-local-network/31324)
- [Quick awk tutorial](https://www.youtube.com/watch?v=az6vd0tGhJI&t=402s) & [More AWK](https://www.youtube.com/watch?v=fCw-xf31M_s&t=202s)
- [Python threading/Multi Tasking](https://www.youtube.com/watch?v=EvbA3qVMGaw&t=166s)
- [Python subprocess: check_output](https://www.youtube.com/watch?v=jq3uTixxrns)



