from pydantic import BaseModel, RootModel, field_validator, model_validator
from typing import List, Optional

"""Abomination of hacks to allow passing of dict with a single key that contains the real data"""
class NamedObject(RootModel[dict]):
    root: dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for k,v in self._data.items():
            setattr(self, k, v)

    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._old__annotations__ = cls.__annotations__
        cls.__annotations__ = {}
    
    @field_validator("root")
    @classmethod
    def f(cls, v: dict):
        class M(BaseModel):
            def __init_subclass__(c, /, **kwargs):
                c.__annotations__ = cls._old__annotations__
                super().__init_subclass__(**kwargs)

        class Mock(M):
            pass

        Mock.__annotations__ = cls._old__annotations__
    
        r = v[list(v.keys())[0]]

        m = Mock.model_validate(r)

        cls._data = {}
        cls.model_fields = m.model_fields
    
        if len(cls.__slots__) == 4:
            def f(self, join_str):
                attrs_names = cls.model_fields.keys()
                attrs = ((s, getattr(self, s)) for s in attrs_names)
                return join_str.join(repr(v) if a is None else f'{a}={v!r}' for a, v in [(a, v) for a, v in attrs if v is not None])
            cls.__repr_str__ = f

            l = list(cls.__slots__)
            for n in m.model_fields:
                l.append(n)
            cls.__slots__ = l

        for n in m.model_fields.keys():
            cls._data[n] = getattr(m, n)

        return None

class Runtime(BaseModel):
    type: str
    version: str
    root: str
    expose: List[int]

class Job(NamedObject):
    install: Optional[List[str]] = []
    script: List[str]
    after_run: Optional[List[str]] = []

class Configuration(BaseModel):
    runtime: Runtime
    install: List[str]
    jobs: List[Job]
    deployment: List[Job]