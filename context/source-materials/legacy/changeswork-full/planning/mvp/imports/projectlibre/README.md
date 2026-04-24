# ProjectLibre Imports

## Files

- `Q2.pod` source ProjectLibre plan file (provided by user)
- `Q2.json` export from `Q2.pod` (MPXJ), used for parsing tasks/deps/resources

## How `Q2.json` Was Generated

ProjectLibre `.pod` is a Java-serialized format; parsing it directly is inconvenient.

This repo uses MPXJ bundled inside ProjectLibre jar to export it:

```bash
java -cp /usr/share/projectlibre/projectlibre.jar \
  net.sf.mpxj.sample.MpxjConvert \
  planning/mvp/imports/projectlibre/Q2.pod \
  planning/mvp/imports/projectlibre/Q2.json
```

