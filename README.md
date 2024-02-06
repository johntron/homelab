# High-availability Kubernetes homelab

![][diagram]

<!-- TOC -->
* [Install](#install)
* [Uninstall](#uninstall)
* [Intel AMT](#intel-amt)
* [Making backups to local MinIO](#making-backups-to-local-minio)
<!-- TOC -->

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
  AWS_ACCESS_KEY_ID: Z2llandYamxiazJsbG1nVw==
  AWS_ENDPOINTS: aHR0cDovLzE5Mi4xNjguMS4yMTc6OTAwMA==
  AWS_SECRET_ACCESS_KEY: MmtjaEZiZzNZQm1BODIwcjZybHNwWG5DNGozbFducjU=
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
