#!/bin/bash

# Variables
VMID=100
VMNAME="docker-k8s-vm"
NODE="pve"
ISO_PATH="/var/lib/vz/template/iso/debian-11.2.0-amd64-netinst.iso"
STORAGE="local-lvm"
BRIDGE="vmbr0"
DISK_SIZE="32G"
MEMORY="8192"
CPUS="4"

# Create VM
qm create $VMID --name $VMNAME --node $NODE --memory $MEMORY --cores $CPUS --net0 virtio,bridge=$BRIDGE
qm set $VMID --ide2 $STORAGE:iso/$ISO_PATH,media=cdrom
qm set $VMID --scsihw virtio-scsi-pci --scsi0 $STORAGE:$DISK_SIZE
qm set $VMID --boot c --bootdisk scsi0
qm start $VMID
echo "VM $VMID ($VMNAME) has been created and started."

# SSH into the VM and run Docker setup
ssh root@<VM-IP> <<EOF
apt-get update
apt-get install -y docker.io
systemctl start docker
systemctl enable docker
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9000:9000 --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce
EOF
