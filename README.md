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

[diagram]: docs/diagrams/out/Layer%201.png
