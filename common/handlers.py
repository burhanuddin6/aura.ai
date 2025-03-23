class ActionHandler:
    def handle(self, command, *args):
        raise NotImplementedError("Each handler must implement the 'handle' method.")

class AddHandler(ActionHandler):
    def handle(self, *args):
        return sum(args)

class MultiplyHandler(ActionHandler):
    def handle(self, *args):
        result = 1
        for num in args:
            result *= num
        return result
