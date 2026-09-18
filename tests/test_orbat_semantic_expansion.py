from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
COMPILED = yaml.safe_load((ROOT / "occid.yaml").read_text())
MODELS = COMPILED["models"]
VOCAB = COMPILED["vocabulary"]


def fields(name: str) -> dict[str, str]:
    return MODELS[name].get("fields", {})


def children(name: str) -> set[str]:
    return set(MODELS[name].get("children", []))


def test_sidc_is_standard_qualified_code():
    assert fields("SIDC") == {"value": "string", "standard": "SymbologyStandard"}
    assert "MIL_STD_2525D = 0" in VOCAB["SymbologyStandard"]["values"]
    assert "MIL_STD_2525E" in VOCAB["SymbologyStandard"]["values"]
    assert "APP_6D" in VOCAB["SymbologyStandard"]["values"]


def test_affiliation_is_not_side_membership_or_subject_identity():
    assert MODELS["Side"]["parent"] == "Set"
    assert MODELS["MilitaryAffiliation"]["parent"] == "Relationship"
    assert fields("MilitaryAffiliation")["identity"] == "StandardIdentity"
    assert "Faction" not in VOCAB


def test_subjects_do_not_embed_graphic_portrayal():
    assert "symbology" not in fields("Entity")
    assert "symbology" not in fields("Location")
    assert "sidc" not in fields("MilitaryOrg")
    assert MODELS["SymbolGraphic"]["parent"] == "Graphic"
    assert MODELS["MilitarySymbolGraphic"]["parent"] == "SymbolGraphic"


def test_graphics_are_representations_not_geometry_semantics():
    assert MODELS["Graphic"]["parent"] == "IdentifiedRepresentation"
    assert MODELS["IdentifiedRepresentation"]["parent"] == "Representation"
    assert fields("GeometryGraphic")["location_uid"] == "UID"
    assert "style" in fields("Graphic")
    for geometry in ("GeoArea", "GeoPath", "GeoCircle", "GlobalPosition"):
        assert "style" not in fields(geometry)
        assert "color" not in fields(geometry)
        assert "opacity" not in fields(geometry)


def test_tactical_graphic_is_semantic_standard_graphic_not_orbat_option_bag():
    tf = fields("TacticalGraphic")
    assert tf["sidc"] == "SIDC"
    assert tf["control_points"] == "list[GlobalPosition]"
    assert tf["status"].startswith("TacticalGraphicStatus")
    for forbidden in ("graphicKind", "options", "textAmplifiers", "amplifierPlacements", "colorMode"):
        assert forbidden not in tf


def test_spatial_aggregates_extend_existing_geometry_without_style():
    assert fields("GeoCircle") == {"center": "GlobalPosition", "radius": "DistanceMeters"}
    assert fields("GeoMultiPoint") == {"points": "list[GlobalPosition]"}
    assert fields("GeoMultiPath") == {"paths": "list[GeoPath]"}
    assert fields("GeoMultiArea") == {"areas": "list[GeoArea]"}


def test_persistent_measurements_are_objects_and_range_ring_is_derived():
    assert MODELS["SpatialMeasurement"]["parent"] == "Data"
    assert {"DistanceMeasurement", "AreaMeasurement", "BearingMeasurement", "RadiusMeasurement", "RouteMeasurement"} <= children("SpatialMeasurement")
    assert MODELS["MeasurementGraphic"]["parent"] == "Graphic"
    assert "RangeRing" not in MODELS


def test_organization_identity_and_mutable_state_are_separated():
    org = fields("Organization")
    state = fields("OrganizationState")
    for mutable in ("position", "operational_status", "readiness", "inventory", "health"):
        assert mutable not in org
        assert mutable in state
    for membership in ("member_uids", "roster"):
        assert membership in org
        assert membership not in state
    assert MODELS["OrganizationState"]["parent"] == "SubjectState"
    assert fields("Group")["org_level"].endswith("GROUP")
    assert fields("Unit")["org_level"].endswith("UNIT")
    assert "orglevel" not in fields("Group")
    assert "orglevel" not in fields("Unit")


def test_authorized_resources_are_distinct_from_current_holdings():
    assert MODELS["ResourceTemplate"]["parent"] == "Definition"
    assert {"EquipmentTemplate", "PersonnelTemplate", "SupplyTemplate"} <= children("ResourceTemplate")
    req = fields("ResourceRequirement")
    holding = fields("ResourceHolding")
    assert req == {"resource_definition_uid": "UID", "quantity": "Quantity"}
    assert holding["resource_definition_uid"] == "UID"
    assert holding["on_hand"] == "Quantity"
    assert "authorized" not in holding
    assert fields("MilitaryOrg")["resource_requirements"] == "list[ResourceRequirement]"
    assert fields("OrganizationState")["inventory"] == "optional InventoryState"


def test_electrical_resource_values_use_measurement_primitives():
    electrical = fields("ElectricalResourceState")
    assert electrical["potential"] == "optional Volts"
    assert electrical["current"] == "optional Amperes"
    assert electrical["power"] == "optional Watts"
    assert electrical["remaining_ratio"] == "optional NormalizedRatio"
    assert electrical["temperature"] == "optional DegreesCelsius"


def test_media_has_semantic_children():
    assert MODELS["MediaItem"]["semantic_role"] == "concept"
    assert {"DurationalMedia", "StillMedia"} <= children("MediaItem")
    assert MODELS["StillImage"]["parent"] == "StillMedia"
    assert MODELS["VideoFrame"]["parent"] == "StillImage"
    assert MODELS["PointCloudMedia"]["parent"] == "StillMedia"
    assert MODELS["AudioMedia"]["parent"] == "DurationalMedia"
    assert MODELS["VideoMedia"]["parent"] == "DurationalMedia"
    assert MODELS["LiveVideoStream"]["parent"] == "VideoMedia"
    assert MODELS["SpectrumMedia"]["parent"] == "DurationalMedia"
    assert MODELS["SpectrumRecording"]["parent"] == "SpectrumMedia"


def test_event_base_remains_sparse_and_specific_events_specialize_it():
    assert fields("Event") == {"record": "Record"}
    assert MODELS["SubjectEvent"]["parent"] == "Event"
    assert MODELS["FlightEvent"]["parent"] == "SubjectEvent"
    assert fields("FlightEvent")["event"] == "AirMissionEvent"
    assert MODELS["TimelineEvent"]["parent"] == "Event"
    assert "temporal_extent" in fields("TimelineEvent")


def test_shared_representation_layers_and_views_are_explicit():
    assert MODELS["Layer"]["parent"] == "IdentifiedRepresentation"
    assert {"OverlayLayer", "ReferenceLayer", "DataLayer"} <= children("Layer")
    assert MODELS["MapView"]["parent"] == "IdentifiedRepresentation"
    assert fields("MapView")["layers"] == "list[LayerView]"
    assert fields("MapView")["bearing"] == "optional AngleDegrees"
    assert fields("LayerView")["opacity"] == "optional Opacity"
    assert {"UTMMapGrid", "MGRSMapGrid", "LatitudeLongitudeMapGrid", "LocalMapGrid"} <= children("MapGrid")
    assert fields("LocalMapGrid")["origin"] == "GlobalPosition"
    assert fields("LocalMapGrid")["interval"] == "DistanceMeters"
    assert fields("LocalMapGrid")["bearing"] == "AngleDegrees"
    assert fields("UTMMapGrid")["zone"] == "UTMZone"


def test_operational_context_is_not_a_nested_scenario_document():
    assert MODELS["OperationalContext"]["parent"] == "Context"
    assert {"Operation", "Scenario"} <= children("OperationalContext")
    context_fields = fields("OperationalContext")
    assert context_fields["reality"] == "Reality"
    assert context_fields["member_uids"] == "list[UID]"
    assert "sides" not in context_fields
    assert "layers" not in context_fields
    assert "events" not in context_fields


def test_oob_size_vocabulary_preserves_three_letter_codes():
    names = [entry.split(" = ", 1)[0] for entry in VOCAB["OOBSize"]["values"]]
    assert all(len(name) == 3 for name in names)
    assert {"COR", "ARM", "AGP", "THR", "CMD"} <= set(names)
    for forbidden in ("CORPS", "ARMY", "ARMY_GROUP", "REGION_THEATER", "COMMAND"):
        assert forbidden not in names


def test_noncombat_military_and_nato_semantics_are_not_separate_modules():
    expected_core_models = {
        "MilitaryOrg": "organization",
        "MilitaryOrgTemplate": "organization",
        "MilitaryOrganizationState": "organization",
        "MilitaryAffiliation": "relationship",
        "MilitarySymbolGraphic": "representation",
        "TacticalGraphic": "representation",
        "MilitarySupplyTemplate": "resource",
        "RadioProfile": "radio",
        "MilitaryAirNavigation": "entities",
        "MilitaryUnitFlightPlan": "aerial",
        "MilitaryMachine": "entities",
    }
    for model, package in expected_core_models.items():
        assert MODELS[model]["package"] == package

    expected_core_vocab = {
        "OOBSize": "organization",
        "NATOUnitCategory": "organization",
        "SymbologyStandard": "attribute",
        "StandardIdentity": "attribute",
        "TacticalGraphicStatus": "representation",
        "NATOSupplyClass": "resource",
        "NATOAlphabet": "communication",
        "AirRole": "aerial",
        "AirISRType": "aerial",
        "PayloadType": "payload",
    }
    for vocabulary, package in expected_core_vocab.items():
        assert VOCAB[vocabulary]["package"] == package

    military_packages = {
        spec["package"]
        for spec in MODELS.values()
        if spec["package"].startswith("military_")
    }
    military_packages |= {
        spec["package"]
        for spec in VOCAB.values()
        if spec["package"].startswith("military_")
    }
    assert military_packages == {"military_effects", "military_entities", "military_tasks"}
