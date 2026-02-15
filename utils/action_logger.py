def log_action(func):
    def wrapper(self, *args, **kwargs):
        self.logger.info(
            f"PAGE ACTION | {self.__class__.__name__}.{func.__name__}()"
        )
        return func(self, *args, **kwargs)
    return wrapper
