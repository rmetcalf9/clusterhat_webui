# clusterhat_webui - Web userinterface for the Raspberry Pi Cluster hat (https://clusterhat.com/)

## Overview
This is a python based webserver that can be run on the Raspberry Pi the clusterhat is plugged into. You can then execute the commands "clusterhat on p1" from the browser.

## Install Instructions

Log in as user Pi
cd ~
git clone git@github.com:rmetcalf9/clusterhat_webui.git
sudo cp -l /home/pi/clusterhat_webui/clusterhat_webui.service /etc/systemd/system/.
sudo systemctl enable clusterhat_webui
sudo systemctl start clusterhat_webui

Then using a web browser surf to the raspberry pi's 
