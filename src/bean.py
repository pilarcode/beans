class Bean:

    def __init__(self, bean_id, name, method, rating):
        self._name = name
        self._method = method
        self._rating = rating
        self._id = bean_id

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_method(self):
        return self._method

    def set_method(self, value):
        self._method = value

    def get_method(self):
        return self._rating

    def set_rating(self, value):
        self._rating = value

    def serialize(self):
        return { "id": self._id,
                "name": self._name,
                "method": self._method,
                "rating": self._rating
                }
