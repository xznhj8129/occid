# Pipeline Trace: UAVTelemetry

How a telemetry message carrying position, altitude, attitude,
waypoint, battery, sats, and ground speed builds through the pipeline.

    Ontology (clades):
      Communication → Message → Telemetry
      Data → State → {Location, Kinematic, Resources, Mission}
      Reference → {Frame, Coordinate, Geometry}

    Typology (specialization):
      [enum]     AltitudeReference, GlobalFrame, CoordinateEncoding, GPSFixType
      [variants] Telemetry → UAV: UAVTelemetry
      [variants] Resources → BATTERY: Battery
      [facets]   LLA needs: lat, lon, altitude, altitude_reference
      [facets]   Location needs: position, altitude, sats, velocity_enu, uncertainty
      [facets]   Kinematic needs: attitude, ground speed, heading, climb rate
      [facets]   Battery needs: voltage, current, remaining pct, temperature
      [facets]   MissionProgress needs: waypoint index, total
      [facets]   UAVTelemetry needs: location, kinematic, battery, mission

    Schema (definition, in YAML):
      enums:     AltitudeReference, GlobalFrame, CoordinateEncoding, GPSFixType, ...
      structs:   LLA{lat,lon,alt,ref,...} → Location{position,alt,...}
                 Quaternion{x,y,z,w} → Kinematic{attitude,speed,...}
                 Battery{voltage,pct,...} MissionProgress{idx,total}
                 → UAVTelemetry{location,kinematic,battery,mission}

Each stage consumes the one above. No stage is skipped.
