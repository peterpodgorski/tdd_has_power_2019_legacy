class MultipleObjectsReturned(Exception):
    pass


class ObjectNotFound(Exception):
    pass


class Manager:
    def __init__(self):
        self.clear()

    def clear(self):
        self._objects = []

    def all(self):
        return list(self._objects)

    def get(self, **kwargs):
        objs = self.filter(**kwargs)
        if not objs:
            raise ObjectNotFound()
        elif len(objs) > 1:
            raise MultipleObjectsReturned()
        else:
            return objs[0]

    def filter(self, **kwargs):
        fields_match = (
            lambda obj: all(
                (getattr(obj, field) == value for field, value in kwargs.items())
            )
        )
        return [obj for obj in self._objects if fields_match(obj)]


class Model:
    def __repr__(self):
        return f'{type(self).__name__} {self.id}'

    def save(self):
        if self not in self.__class__.objects.all():
            self.__class__.objects._objects.append(self)