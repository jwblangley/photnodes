EXCEPTIONS = {}


def attribute_dict_rename_adapter(attr_dict):
    return {EXCEPTIONS[k] if k in EXCEPTIONS else k: v for k, v in attr_dict.items()}
