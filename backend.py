class List:

    def __init__(self, ls):
        self.__list = ls
        self.__n = len(ls)

    def __str__(self):
        self.__list.sort()
        tmp = ''
        for element in self.__list:
            tmp += str(element) + '; '
        return tmp

    def get_avg(self):
        self.__list.sort()
        si = 0
        for element in self.__list:
            si += float(element)
        return si/float(self.__n)

    def get_quartiles(self):
        self.__list.sort()
        quartiles = [0.25, 0.50, 0.75]
        results = []
        for quartile in quartiles:
            sp = quartile * (self.__n + 1)
            if sp % 1 == 0:
                results.append(self.__list[int(sp-1)])
            else:
                sp_leftover = sp % 1
                sp = float(sp) - float(sp_leftover)
                result = float(self.__list[int(sp-1)]) + float(sp_leftover) * (float(self.__list[int(sp)]) -
                                                                               float(self.__list[int(sp-1)]))
                results.append(result)
        return results

    def get_dispersion(self):
        self.__list.sort()
        avg = self.get_avg()
        res = 0
        for element in self.__list:
            res += (float(element) - float(avg))**2
        return (res / self.__n)**0.5

    def get_momentum(self, number):
        self.__list.sort()
        avg = float(self.get_avg())
        result = 0
        for element in self.__list:
            result += (float(element) - avg)**number
        return result/self.__n

    def get_kurtosis(self):
        return (self.get_momentum(4) / (self.get_dispersion()**4)) - 3

    def get_skewness(self):
        return self.get_momentum(3) / (self.get_dispersion()**3)

    def get_min(self):
        return min(self.__list)

    def get_max(self):
        return max(self.__list)

    def get_extent(self):
        return float(self.get_max()) - float(self.get_min())
