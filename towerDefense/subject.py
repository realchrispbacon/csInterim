from interface import Interface


class Subject(Interface):
    def registerObserver(self, observer):
        pass

    def removeObserver(self, observer):
        pass

    def notifyObservers(self):
        pass