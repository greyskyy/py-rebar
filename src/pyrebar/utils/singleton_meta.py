"""Singleton metaclass."""


class SingletonMeta(type):
    """Metaclass for singleton objects."""

    def __init__(self, name, bases, dic):
        """Metaclass constructor.

        Args:
            name (str): The class name
            bases (list): List of base classes
            dic (dict): dictionary
        """
        self.__instance = None
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs):
        """Function call to finish class construction.

        Returns:
            type: The class instance
        """
        if cls.__instance:
            return cls.__instance

        singleton = cls.__new__(cls)
        singleton.__init__(*args, **kwargs)
        cls._instance = singleton
        return singleton
