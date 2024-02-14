# High-availability Kubernetes homelab

![][diagram]

<!-- TOC -->
* [Install](#install)
* [Uninstall](#uninstall)
* [Intel AMT](#intel-amt)
* [Making backups to local MinIO](#making-backups-to-local-minio)
<!-- TOC -->

## Goal

Simple (relatively), flexible cluster with good uptime for "production" services, and flexibility to experiment

## Objectives
* mostly-identical infra on all nodes
* high-availability control plane
* fault tolerance for volumes
* durable storage for backups
* smart scheduling based on workload requirements
* ephemeral storage for ops purposes

## Inventory

Nodes:
* 1x Pi5
* 2x Pi4
* 3x TinyMiniMicro

Storage:
* 512GB partitions on most devices
* NVMe for all but one 512GB partition (USB 3 SSD)
* 4TB NVMe drive in Pi5 with two partitions: 512GB and 3.5TB
* 1TB USB 3 SSD on one Pi4 - two 512GB partitions
* 32GB micro SD card on other Pi4
* 2x 512GB NVMe's in all TinyMiniMicro nodes

Network:
* Everything plugged into a 1Gbe switch

## Configuration

* Talos Linux on everything that supports it (all but Pi5)
* 5x control nodes - all but Pi5
* 5x worker nodes: all but Pi5
* Most apps scheduled on TinyMiniMicro
* Apps requiring special devices (e.g. Z-wave controller) scheduled on Pi4 w/USB SSD
* Ephemeral storage on Pi5

Primary MinIO cluster:
* Uses 512GB partitions available on most devices
* Excludes SD-card-only Pi4 and 3.5TB partition on Pi5

## Fault tolerance

* If worker node goes down, scheduler can reschedule on another node, because storage would have been replicated there previously
* MinIO with erasure coding (N/2) on all nodes except the SD-card-only Pi4
* Longhorn replicates all volumes to all nodes except the SD-card only Pi4
* Longhorn backs up to MinIO


## Flexibility

* Pi 5 has additional MinIO instance (SNSD) in addition to the one with erasure coding. This is to use for ad-hoc storage or manual backups already replicated elsewhere
* Can remove a device and create a separate cluster for testing, upgrading, etc.
* Configuration as code for quick changes (Terraform)
* Rancher for easy monitoring and management

## Questions

* Assuming one drive has a lot more storage than the others, with MinIO is there any benefit to creating multiple partitions for MinIO on this drive? Consider erasure coding.
* How do I benchmark MinIO performance to ensure the 1Gbe links are being fully-saturated?
* How can I ensure special hardware is available when needed, and low-performance hardware is avoided? e.g. resource-based scheduling, affinity/anti-affinity rules, or taints and tolerations
* If worker node goes down, workloads should be rescheduled on remaining nodes. Assuming volumes were already replicated to all nodes, will Longhorn handle this automatically?
* What happens when all power is lost?
* How often should Longhorn backup? Retention policy?
* How can I create fault-tolerant storage for Home Assistant?
* How can I grant unfettered access to an Aeotec USB Z-Wave controller on the Pi4?
* How can I manage configuration for production cluster and experimental cluster? Note: I need to remove a node to support this
* How do I test fault tolerance of Longhorn PVs and MinIO nodes?

## Next steps

Imaging:
* Share network on ethernet and plug in Pi4
* Use Pi imager to update Pi4 to boot from USB
* Use Pi imager to create image on USB for Talos
* Insert USB drive into Pi4 and boot - ensure accessible via talosctl
Experimenting:
* Record storage devices and NIC MAC
* Figure out how to save secrets generated during Talos provisioning
* Install Talos with two equal-size partitions: one for Longhorn (mount at /var/lib/longhorn), one for MinIO
* Enable as worker node
* Create Kubernetes cluster
* Install Longhorn
* Install MinIO
* Configure Longhorn to backup to MinIO
* Join MinIO with Pi 5
* Determine if Z-wave controller can run in Kubernetes with device passthrough
Reproducing:
* Save the secrets somewhere
* Redo the above in Terraform
Making durable:
* Repeat on one existing TinyMiniMicro node - join to Pi4 as control + worker
* Repeat on another
* Ensure MinIO is now using erasure coding
* Ensure Longhorn replication and workload affinity makes sense
* Test failure scenario
* Add final TinyMiniMicro node

## Install

```
(cd metallb && helm upgrade --install metallb bitnami/metallb -f chart/values.yaml)
```

## Uninstall

```
helm uninstall metallb
```

## Intel AMT

If the hardware supports it, you can use Intel AMT for remote out-of-band management over IP; however, you must enable it first. Note: Intel AMT is supported by the always-on Intel Management Engine (ME); AMT is the part that allows *remote* administration.

To enable:

* Figure out how to get into Intel MEBx settings during BIOS/UEFI boot - you'll need this later; For me, I had to hit ESC - using ctrl-P didn't work
* Find BIOS setting to unprovision Intel ME
* Save and exit
* Use keystroke to enter Intel MEBx
* Choose the login option
* Set a new password - google to see what the password requirments are, because the error message for an insecure/invalid password is ambiguous
* Now navigate the menu to find the setting to enable network configuration
* Optionally, change from DHCP to static
* Find the option to enable KVM, SOL, etc. - enable whichever
* Find the option for user consent - select "none"; otherwise, you'll be asked to enter a code visible on the physical device when you try to remotely manage
* Exit - this saves the settings

Now you can figure out the IP of the machine and visit http://$IP:16992 in your browser - login with the same password you created above. You should be able to do basic things now like reboot, view status, etc.

For KVM over IP, there are additional steps:

* Install wsmancli
* Run (./enable-kvm.sh) - *WARNING* Be sure you read the part about password requirments when setting VNC password
* Launch a VNC viewer like noVNC:
  * novnc --vnc $IP:5900
  * google-chrome --app="http://localhost:6080/vnc.html?host=johntron-linux&port=6080"
* Connect to the machine using the password you created when running enable-kvm.sh

### MeshCentral

```shell
podman run -d --name meshcentral --rm -p 8443:443 typhonragewind/meshcentral
echo "There's no default login - you'll need to create an account"
open https://localhost:8443
```

### MeshCommander

```shell
podman run -d -p 127.0.0.1:3001:3000 --name meshcommander vga101/meshcommander
open http://localhost:3001
```


## Making backups to local MinIO

```shell
podman run -d \
  -v $PWD/s3_backups:/data \
  -p 9000:9000 \
  -p 9001:9001 \
  quay.io/minio/minio \
  server /data --console-address ":9001"
```

Open http://localhost:9001 and login - link to docs in output from container.
Set the region to "desktop", create an access key, and set env for the command below.

```shell
# set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
set AWS_ENDPOINTS http://(hostname -I | grep -E '192\.168\.1\.[0-9]+' -o):9000
kubectl create secret generic minio-backup \
  --from-literal=AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
  --from-literal=AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  --from-literal=AWS_ENDPOINTS="$AWS_ENDPOINTS" \
  --namespace=longhorn-system
```

Now back in Longhorn, go to Settings > Backups and use:
* s3://backups@desktop/
* minio-backup

```yaml
apiVersion: v1
kind: Secret
type: Opaque
data:
  AWS_ACCESS_KEY_ID: 
  AWS_ENDPOINTS: aHR0cDovLzE5Mi4xNjguMS4yMTc6OTAwMA==
  AWS_SECRET_ACCESS_KEY: 
metadata:
  name: minio-backup
  namespace: longhorn-system
```

## Next

* Use Windows VM to create BIOS upgrade media for tiny1/2
* ... try to enable KVM on tiny2?
* Use router as DNS, so I can use custom domain? (updates to Rancher config)
* Find some way to avoid changing EDID's (1920 for itx, 1280 for minis)
* RouterOS terraform to turn on netboot.xyz via PXE boot
* cloud-config server for Harvester
* Use terraform to create volumes: home assistant and ghost
* Restore Longhorn backups from S3 by starting a minio backup server (instructions above)
* ... or ...
* Use something like busybox to mount volumes and copy files to them
* Terraform for metallb
* ... home assistant
* ... ghost
* Terraform for Meshcommander to access KVM on tiny1?
* Delete S3 backups from gdrive?

## Quirks

* tiny1 supports KVM, but tiny2 does not
* Pikvm mass storage _may_ interfere with keyboard / mouse on tiny1/2
* Keyboard won't work during boot for tiny1/2:
  * use Logitech keyboard
  * physically disconnect pikvm USB
* tiny1/2 and itx require different EDID's in pikvm:
  * itx: 1920
  * tiny1/2: 1280
* ... see /home/pikvm/edids/README.md

[diagram]: docs/diagrams/out/Layer%201.png
