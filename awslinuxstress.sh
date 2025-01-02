#!/bin/bash
# Use this for your user data (script from top to bottom)
# install stress (Linux 2 version)
sudo amazon-linux-extras install epel -y
sudo yum install stress -y 

#stress -c #of cpus
#^C or ^D
