'''Utils module.
Contains tools to reduce boilerplate code.'''


def create_instance(schema, json):
    '''Custom method for model instance creation'''
    data = schema.load(json)
    return schema.model(**data)


def update_instance(schema, json, obj):
    '''Custom method for model instance update'''
    data = schema.load(json)
    for k, v in data:
        setattr(obj, k, v)
