class Pizza:

    def __init__(self, name, dough, sauce):
        self._name = name
        self._dough = dough
        self._sauce = sauce
        self._toppings = []

        def getName(self):
            return self._name

        def prepare(self):
            print("Preparing " + self._name)

        def bake(self):
            print("Baking " + self._name)

        def cut(self):
            print("Cutting " + self._name)

        def box(self):
            print("Boxing " + self._name)

        def __str__(self):
            #code to display pizza name and ingredients
            display = ""
            display.append("---- " + name + " ----\n")
            display.append(dough + "\n")
            display.append(sauce + "\n")
            for topping in self._toppings:
                display.append(topping + "\n")
            return display.toString()

