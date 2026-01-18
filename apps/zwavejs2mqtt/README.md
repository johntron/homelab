* Connect Aeotec Zstick to USB port of Raspberry Pi
* Install any OS that can run Docker
* Run zwavejs2mqtt:

```
docker run -d -p 80:8091 -p 3000:3000 --restart unless-stopped --device=/dev/ttyACM0 -v $(pwd)/store:/usr/src/app/store zwavejs/zwavejs2mqtt:9.5.1
```

Previous version:
    zwavejs2mqtt: 6.13.0
    zwave-js: 9.5.0
    home id: 4111696383
    home hex: 0xf51381ff

Recently updated to:
    zwave-js-ui: 9.5.1.e4c1eb5
    zwave-js: 12.4.0
    home id: 4111696383
    home hex: 0xf51381ff


Note: zwave2mqtt is deprecated. Switch to https://zwave-js.github.io/zwave-js-ui/#/ - details: https://hub.docker.com/r/zwavejs/zwavejs2mqtt; this migration includes some breaking changes