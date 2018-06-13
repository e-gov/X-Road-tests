#!/bin/sh

#####################################################################
#
# This script installs Utimaco hardware token to LXD environment
# and a security server. Uses parameters from the main config.ini.
#
# You need to have the following files in the same directory
# as this script:
# - ADMIN.key
# - cs_pkcs11_R2.cfg
# - cssim410_test.tar
# - devices.ini
# - libcs_pkcs11_R2.so
# - p11tool2
#
# NOTE that some of the files need to be obtained from Utimaco.
#
# Usage: ./hwtoken_install.sh hwtoken_section ca_section config_file
#    where:
#      - hwtoken_section refers to the config file ini section name
#        that contains hardware token server (security server) info
#      - ca_section refers to the CA configuration section in the
#        configuration file
#      - config_file refers to the configuration file that contains
#        the aforementioned sections
#
#####################################################################

# Can be overriden with the third parameter
xroad_config_file="./config.ini"

# Filenames
csadm="csadm"
adminkey="ADMIN.key"
pkcs11_conf="cs_pkcs11_R2.cfg"
pkcs11_libcs_file="libcs_pkcs11_R2.so"
devices_ini="devices.ini"
docker_image="cssim410_test.tar"
p11="p11tool2"

# Override config file path
if test "$3" != ""; then
    xroad_config_file="$3"
fi

set -e
set -x

echo "Using configuration file $xroad_config_file"

# SS credentials
ss=$(sed -nr "/^\["$1"\]/ { :l /^ssh_host[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $xroad_config_file)
ss_user=$(sed -nr "/^\["$1"\]/ { :l /^ssh_user[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $xroad_config_file)
ss_pass=$(sed -nr "/^\["$1"\]/ { :l /^ssh_pass[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $xroad_config_file)
ss_host="$ss"
echo "SS host: $ss_host"

remote_tmp="/home/$ss_user"

# CA credentials

ca=$(sed -nr "/^\["$2"\]/ { :l /^ssh_host[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $xroad_config_file)
ca_user=$(sed -nr "/^\["$2"\]/ { :l /^ssh_user[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $xroad_config_file)
ca_pass=$(sed -nr "/^\["$2"\]/ { :l /^ssh_pass[ ]*=/ { s/.*=[ ]*//; p; q;}; n; b l;}" $xroad_config_file)
ca_host="$ca"
echo "CA host: $ca_host"

# Install sshpass if not already installed
sudo apt-get install -y sshpass

# Install Docker to host machine

curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Run docker image
sg docker "docker load -i $docker_image"
sg docker "docker run -p3001:3001 -dt --rm --name cssim410_test cssim410_test"

# Get host docker ip
docker_ip=$(ifconfig docker | grep "inet addr" | cut -d ':' -f 2 | cut -d ' ' -f 1)
sed -i 's/127.0.0.1/'$docker_ip'/g' cs_pkcs11_R2.cfg

# Writing files to SS temporary folder
sshpass -p $ss_pass scp -oStrictHostKeyChecking=no $csadm $ss_user@$ss_host:$remote_tmp
sshpass -p $ss_pass scp -oStrictHostKeyChecking=no $adminkey $ss_user@$ss_host:$remote_tmp
sshpass -p $ss_pass scp -oStrictHostKeyChecking=no $p11 $ss_user@$ss_host:$remote_tmp
sshpass -p $ss_pass scp -oStrictHostKeyChecking=no $pkcs11_conf $ss_user@$ss_host:$remote_tmp
sshpass -p $ss_pass scp -oStrictHostKeyChecking=no $devices_ini $ss_user@$ss_host:$remote_tmp
sshpass -p $ss_pass scp -oStrictHostKeyChecking=no $pkcs11_libcs_file $ss_user@$ss_host:$remote_tmp

# Change CA configuration

sshpass -p $ca_pass ssh -oStrictHostKeyChecking=no $ca_user@$ca_host <<EOF
	sudo sed -i 's/yes/'no'/g' /home/ca/CA/index.txt.attr
EOF

# Connecting and installing needed files in SS

sshpass -p $ss_pass ssh -oStrictHostKeyChecking=no $ss_user@$ss_host <<EOF
    chmod +x $remote_tmp/$csadm
    chmod +x $remote_tmp/$p11
	sudo apt-get install -y xroad-addon-hwtokens
	cd /etc	
	sudo mkdir -p utimaco
	sudo cp $remote_tmp/$pkcs11_conf /etc/utimaco/
	sudo cp $remote_tmp/$devices_ini /etc/xroad/
	sudo cp $remote_tmp/$pkcs11_libcs_file /usr/lib/

	cd $remote_tmp
	sudo service xroad-signer restart
	sudo reboot
EOF

# Let the machine shut down and reboot
sleep 10

# As we rebooted ss1, wait until SSH is up
echo "Waiting for $ss_host SSH server"
set +e
ssh -oStrictHostKeyChecking=no $ss_user@$ss_host echo 2> /dev/null
while test $? -gt 0
do
    sleep 5
    ssh $ss_user@$ss_host echo 2> /dev/null
done
echo "Waiting until SS retuns HTTP 302"
until test `curl -k -s -o /dev/null -w "%{http_code}" https://$ss_host:4000/` = "302"; do sleep 5; done
set -e

