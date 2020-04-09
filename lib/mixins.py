class ModelMixin:
    def to_dict(self):
        attr_dict = {}
        for filed in self._meta.get_fields():
            attr_dict[filed.attname] = getattr(self, filed.attname, None)
        return attr_dict
