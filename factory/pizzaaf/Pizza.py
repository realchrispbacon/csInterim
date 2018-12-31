class Pizza:
    def __init__(self):
        self._name = ""
        self._dough = ""
        self._sauce = ""
        self._veggies = []
        self._cheese = ""
        self._pepperoni = ""
        self._clam = ""

    def prepare(self):
        pass

    def bake(self):
        print("Bake for 25 minutes at 350")

    def cut(self):
        print("Cutting the pizza into diagonal slices")

    def box(self):
        print("Place pizza in official PizzaStore box")

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def __str__(self):
        result = ""
        result += "---- " + self._name + " ----\n"
        if self._dough != "":
            result += self._dough
            result += "\n"
        if self._sauce != "":
            result += self._sauce
            result += "\n"
        if self._cheese != "":
            result += self._cheese
            result += "\n"
        if self._veggies != "":
            for i in self._veggies.length:
                result += self._veggies[i]
                if i < self._veggies.length-1:
                    result += ", "
            result += "\n"
        if self._clam != "":
            result += self._clam
            result += "\n"
        if self._pepperoni != "":
            result += self._pepperoni
            result += "\n"
        return result
