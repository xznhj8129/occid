## Sensory

### AV

[variants]:
- VIDEO: Video
- IMAGE: Image
- AUDIO: Audio

ThermalImage [facets]:
- temperature range
- palette

[enum] SARMode:
- Spotlight
- Stripmap
- ScanSAR
- ISAR
- GMTI

SARImage [facets]:
- SAR mode (SARMode)
- resolution
- look direction
- incidence angle
- polarization

### Spatial

[variants]:
- POINTCLOUD: PointCloud
- MESH: Mesh
- SCAN: Scan

### Samples

[variants]:
- IQ: IQSamples — in-phase/quadrature
- ANALOG: AnalogSamples

