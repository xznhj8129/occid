### Models

OCCID_MODEL_BY_ID = {}
OCCID_MODEL_ID_BY_CLASS = {}


class OCCIDModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    __occid_model_id__: ClassVar[int | None] = None
    __occid_semantic_role__: ClassVar[str | None] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "__occid_semantic_role__" not in cls.__dict__:
            cls.__occid_semantic_role__ = None
        model_id = getattr(cls, "__occid_model_id__", None)
        if model_id is not None:
            OCCID_MODEL_BY_ID[model_id] = cls
            OCCID_MODEL_ID_BY_CLASS[cls] = model_id

    def encode(self) -> bytes:
        envelope = {
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
    """Decode a heterogeneous OCCID transient envelope by its model ID.

    This is the counterpart to ``OCCIDModel.encode()`` for receivers that do not
    know the concrete model class before inspecting the envelope. The transient
    envelope identifies the concrete model and carries its fields; schema change
    detection belongs to the OCCID contract manifest/build check, not every wire
    payload.
    """
    envelope = msgpack.unpackb(payload, raw=False)
    if type(envelope) is not dict:
        raise ValueError("OCCID payload envelope must be a map")
    required = {"model_id", "fields"}
    if set(envelope) != required:
        raise ValueError(
            f"OCCID payload envelope fields must be {sorted(required)}; "
            f"got {sorted(envelope) if all(type(key) is str for key in envelope) else list(envelope)}"
        )
    model_id = envelope["model_id"]
    model_cls = OCCID_MODEL_BY_ID.get(model_id)
    if model_cls is None:
        raise ValueError(f"unknown OCCID model ID {model_id}")
    fields = envelope["fields"]
    if type(fields) is not dict:
        raise ValueError("OCCID payload fields must be a map")
    return model_cls._from_wire_fields(fields)
