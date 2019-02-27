def to_camel_case(key):
    if not key or len(key) == 0:
        raise Exception('Key is empty')
    parts = key.split('_')
    if len(parts) == 1:
        return key
    while parts and not parts[0]:
        parts = parts[1:]
    return parts[0] + ''.join([item.capitalize() for item in parts[1:]])
