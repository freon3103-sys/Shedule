class Str_shed():

    def __init__(self, str_shed, hour):

        self.str = str_shed.replace(" ", "")
        colors = ["orange", "red", "green", "purple", "blue", "brown"]
        True_colors = {"orange": "оранжевый", "red": "красный", "green": "зеленый", "purple": "фиолетовый", "blue": "синий", "brown": "коричневый"}
        self.flights = []
        self.b = "False"
        self.color = []
        self.hour = hour

        if self.str.isdigit():

            self.flights.append(Flight(self.str))

        else:

            if any(color in self.str for color in colors) or "<b>" in self.str:

                flights = self.str.split("<br/>")

                for x in flights:

                    if any(color in x for color in colors) and "<b>" in x:

                        for color_x in colors:

                            if color_x in x:

                                self.flights.append(Flight("".join(char for char in x if char.isdigit()), color=True_colors[color_x],b="жирный"))
                                break

                        self.b = "жирный"

                    elif any(color in x for color in colors):

                        for color_x in colors:

                            if color_x in x:

                                self.flights.append(Flight("".join(char for char in x if char.isdigit()), color=True_colors[color_x]))
                                if color_x in self.color:

                                    None

                                else:

                                    self.color.append(True_colors[color_x])

                    elif "<b>" in x:

                        self.flights.append(Flight("".join(char for char in x if char.isdigit()), b="жирный"))
                        self.b = "жирный"

                    else:

                        self.flights.append(Flight("".join(char for char in x if char.isdigit())))

            else:

                self.flights = [Flight(x) for x in self.str.split("<br/>")]

        self.len = len(self.color)

    def __str__(self):

        return "".join(str(x) for x in self.flights)

class Flight():

    def __init__(self, str, color="черный", b="не жирный"):

        self.str = str
        self.color = color
        self.b = b

    def __str__(self):

        return f"({self.str}, {self.color}, {self.b}) "

class Table_shed():

    def __init__(self, table_list, name):

        self.table = table_list
        self.name = name
        self.result = dict()
        comb = ["черный_жирный", "черный_не жирный", "красный_не жирный", "оранжевый_не жирный", "синий_не жирный", "зеленый_не жирный", "фиолетовый_не жирный", "коричневый_жирный", "красный_жирный", "оранжевый_жирный", "синий_жирный", "зеленый_жирный", "фиолетовый_жирный", "коричневый_не жирный"]
        for combination in comb: # перебор комбинаций цветов и жирноты текста

            color, b = combination.split("_") # разделение на цвет и жирность

            for str in self.table: # перебор расписаний

                for x in str.flights:

                    if x.str == "":

                        continue

                    elif x.color == color and x.b == b:

                        if combination not in self.result:

                            self.result[combination] = []

                        self.result[combination].append(f"{str.hour}:{x.str}")