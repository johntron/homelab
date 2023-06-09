## Running

Prepare:

```shell
poetry install
poetry run python3 -m bootserver prepare
```

Run - uses privileged port 69, so must use sudo:
```shell
sudo (which poetry) install
sudo (which poetry) run python3 -m bootserver run
```

## Building iPXE

Follow these instructions to build iPXE alone without bootserver.

Install dependencies:

```shell
sudo apt install -y build-essential liblzma-dev
```

```shell
git clone https://github.com/ipxe/ipxe.git
make -C ipxe/src clean \
  bin-x86_64-efi/ipxe.efi \
  EMBED="../../chainload-bootserver.ipxe"
cp ipxe/src/bin-x86_64-efi/ipxe.efi bootserver/
```

Note: if using older hardware, the UNDI-only iPXE might work better. e.g. make bin/undionly.kpxe

## Configuring DHCP server

1. Set next-server to IP of bootserver
2. Set boot filename to "ipxe.efi"

## Device ID

tiny1 Intel L219-LM (11) is device ID 8086:0d4c