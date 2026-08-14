### Models

OCCID_MODEL_BY_ID = {}
OCCID_MODEL_ID_BY_CLASS = {}


class OCCIDModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __occid_model_id__: ClassVar[int | None] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        model_id = getattr(cls, "__occid_model_id__", None)
        if model_id is not None:
            OCCID_MODEL_BY_ID[model_id] = cls
            OCCID_MODEL_ID_BY_CLASS[cls] = model_id

    @model_validator(mode="after")
    def _validate_enum_relation_maps(self):
        module = sys.modules.get(type(self).__module__)
        if module is None:
            return self

        def field_name(enum_type):
            name = enum_type.__name__
            name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
            return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()

        for mapping_name, mapping in vars(module).items():
            if not mapping_name.startswith("VALID_"):
                continue
            if type(mapping) is not dict or not mapping:
                continue
            key = next(iter(mapping))
            value = mapping[key]
            if not isinstance(key, Enum) or not isinstance(value, Enum):
                continue
            key_field = field_name(type(key))
            value_field = field_name(type(value))
            if key_field not in type(self).model_fields or value_field not in type(self).model_fields:
                continue
            key_value = getattr(self, key_field)
            if key_value is None:
                continue
            expected = mapping.get(key_value)
            actual = getattr(self, value_field)
            if expected != actual:
                key_name = getattr(key_value, "name", str(key_value))
                value_name = getattr(actual, "name", str(actual))
                raise ValueError(
                    f"{key_field}={key_name} is not valid for {value_field}={value_name}"
                )
        return self

    def encode(self) -> bytes:
        envelope = {
            "schema_version": list(OCCID_SCHEMA_VERSION),
            "model_id": OCCID_MODEL_ID_BY_CLASS[type(self)],
            "fields": self._wire_model_fields(self),
        }
        return msgpack.packb(envelope, use_bin_type=True)

    @classmethod
    def decode(cls, payload: bytes):
        model = decode_model(payload)
        if type(model) is not cls:
            model_id = OCCID_MODEL_ID_BY_CLASS[type(model)]
            raise ValueError(f"payload model ID {model_id} does not identify {cls.__name__}")
        return model

    @classmethod
    def _from_wire_fields(cls, data):
        values = {
            field_name: cls._wire_to_value(cls.model_fields[field_name].annotation, value)
            for field_name, value in data.items()
        }
        return cls(**values)

    @classmethod
    def _wire_to_value(cls, annotation, data):
        if data is None:
            return None

        origin = get_origin(annotation)
        args = get_args(annotation)

        if type(data) == dict and set(data) == {"model_id", "fields"}:
            model_id = data["model_id"]
            model_cls = OCCID_MODEL_BY_ID.get(model_id)
            if model_cls is None:
                raise ValueError(f"unknown OCCID model ID {model_id}")
            return model_cls._from_wire_fields(data["fields"])

        if origin is Annotated:
            return cls._wire_to_value(args[0], data)

        if origin is list:
            return [cls._wire_to_value(args[0], item) for item in data]

        if origin is dict:
            return {key: cls._wire_to_value(args[1], value) for key, value in data.items()}

        if origin is tuple:
            return tuple(cls._wire_to_value(arg, item) for arg, item in zip(args, data))

        if origin in (Union, UnionType):
            for arg in args:
                try:
                    return cls._wire_to_value(arg, data)
                except (TypeError, ValueError, KeyError, IndexError):
                    pass
            return data

        try:
            if issubclass(annotation, OCCIDModel):
                return annotation._from_wire_fields(data)
        except TypeError:
            pass

        try:
            if issubclass(annotation, IntEnum):
                return annotation(data)
        except TypeError:
            pass

        try:
            if issubclass(annotation, Enum):
                return annotation(data)
        except TypeError:
            pass

        return data

    @classmethod
    def _wire_value(cls, value):
        if issubclass(type(value), OCCIDModel):
            return {
                "model_id": OCCID_MODEL_ID_BY_CLASS[type(value)],
                "fields": cls._wire_model_fields(value),
            }
        if type(value) == dict:
            return {key: cls._wire_value(item) for key, item in value.items()}
        if type(value) in (list, tuple):
            return [cls._wire_value(item) for item in value]
        if issubclass(type(value), IntEnum):
            return value.value
        if issubclass(type(value), Enum):
            return value.value
        return value

    @classmethod
    def _wire_model_fields(cls, value):
        return {
            field_name: cls._wire_value(getattr(value, field_name))
            for field_name in type(value).model_fields
        }

    def model_dump(self, *, mode="python", **kwargs):
        def encode(value):
            if type(value) == dict:
                return {key: encode(item) for key, item in value.items()}
            if type(value) in (list, tuple):
                return [encode(item) for item in value]
            if issubclass(type(value), IntEnum):
                return value.value
            if issubclass(type(value), Enum):
                return value.value
            return value

        if mode == "json":
            data = super().model_dump(mode="python", **kwargs)
            return encode(data)
        data = super().model_dump(mode=mode, **kwargs)
        return data


def decode_model(payload: bytes) -> OCCIDModel:
    """Decode a heterogeneous OCCID transient envelope by its permanent model ID.

    This is the counterpart to ``OCCIDModel.encode()`` for receivers that do not
    know the concrete model class before inspecting the envelope. It validates
    the schema version and model ID, then delegates field reconstruction to the
    registered generated model. Runtime routing or behavioral policy does not
    belong here.
    """
    envelope = msgpack.unpackb(payload, raw=False)
    if type(envelope) is not dict:
        raise ValueError("OCCID payload envelope must be a map")
    required = {"schema_version", "model_id", "fields"}
    if set(envelope) != required:
        raise ValueError(
            f"OCCID payload envelope fields must be {sorted(required)}; "
            f"got {sorted(envelope) if all(type(key) is str for key in envelope) else list(envelope)}"
        )
    version = tuple(envelope["schema_version"])
    if version != OCCID_SCHEMA_VERSION:
        raise ValueError(f"unsupported OCCID schema version {version}; expected {OCCID_SCHEMA_VERSION}")
    model_id = envelope["model_id"]
    model_cls = OCCID_MODEL_BY_ID.get(model_id)
    if model_cls is None:
        raise ValueError(f"unknown OCCID model ID {model_id}")
    fields = envelope["fields"]
    if type(fields) is not dict:
        raise ValueError("OCCID payload fields must be a map")
    return model_cls._from_wire_fields(fields)
