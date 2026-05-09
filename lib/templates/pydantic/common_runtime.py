### Models

class OCCIDModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    def model_dump(self, *, mode="python", **kwargs):
        def encode(value):
            if type(value) == dict:
                return {key: encode(item) for key, item in value.items()}
            if type(value) in (list, tuple):
                return [encode(item) for item in value]
            if issubclass(type(value), IntEnum):
                return value.name
            if issubclass(type(value), Enum):
                return value.value
            return value

        if mode == "json":
            data = super().model_dump(mode="python", **kwargs)
            return encode(data)
        data = super().model_dump(mode=mode, **kwargs)
        return data
