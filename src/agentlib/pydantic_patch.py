"""
Monkey patch Pydantic 1.x to include 2.x style methods
"""
import pydantic

if pydantic.__version__ < '2':
    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # Accepts dict or model
        if isinstance(obj, cls):
            return obj
        return cls.parse_obj(obj, *args, **kwargs)
    pydantic.BaseModel.model_validate = model_validate

    @classmethod
    def model_json_schema(cls, *args, **kwargs):
        schema = pydantic.BaseModel.schema.__func__(cls, *args, **kwargs)
        if 'description' not in schema and (model_doc := cls.__doc__):
            schema['description'] = model_doc.strip()
        if 'properties' in schema:
            for field_name, field_schema in schema['properties'].items():
                model_field = cls.__fields__.get(field_name)
                if model_field and model_field.allow_none:
                    original = field_schema.copy()
                    field_schema.clear()
                    for meta_key in ('title', 'description', 'examples', 'default'):
                        if meta_key in original:
                            field_schema[meta_key] = original.pop(meta_key)
                    any_of = original.pop('anyOf', [])
                    if original:
                        any_of.append(original)
                    if not any(
                        isinstance(branch, dict) and branch.get('type') == 'null'
                        for branch in any_of
                    ):
                        any_of.append({'type': 'null'})
                    field_schema['anyOf'] = any_of
        return schema
    pydantic.BaseModel.model_json_schema = model_json_schema
