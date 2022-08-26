from math import e, pi, sqrt, floor, log
from config import *
import matplotlib
import matplotlib.pyplot as plt

"""
    Функция возвращает количество людей, выходящих из дома в момент времени t
    Параметры:
        t - [0, 24], float
        people - [0, +inf], int
"""
def peopleOfTime(time: float, people:int = 1) -> int:
    MorningPeakKoeff = -7.2
    EveningPeakKoeff = -18.5
    MorningPeak = (e**(-((time+MorningPeakKoeff)**2)))/sqrt(pi)
    EveningPeak = (e**(-((time+EveningPeakKoeff)**2)))/sqrt(pi)
    return people*(MorningPeak+EveningPeak)


def peopleOfTimeV2(time: float, people:int = 1) -> int:
    MorningPeakKoeff = 7.5
    EveningPeakKoeff = 18.3

    o = 2
    a = -(1/(2*(o**2)))
    # print(a)

    bMorning = MorningPeakKoeff/(o**2)
    cMorning = -(log(o)+0.5*log(2*pi)+((0.5*(MorningPeakKoeff**2))/(o**2)))
    # print(bMorning)

    # print(cMorning)

    bEvening = EveningPeakKoeff/(o**2)
    cEvening = -(log(o)+0.5*log(2*pi)+((0.5*(EveningPeakKoeff**2))/(o**2)))

    # print(bEvening)

    # print(cEvening)
    MorningPeak = e**(a*(time**2)+(bMorning*time)+cMorning)
    EveningPeak = e**(a*(time**2)+(bEvening*time)+cEvening)

    return people*(MorningPeak+EveningPeak)

    

"""
    Функция возвращает колечество машин на дороге в час и относительную загруженность
    Параметры:
        initialCars - начальное количество машин на дороге
        initialSituations - начальная загруженность дороги
        newCars - добавленные машины
"""
def calculateRoadSituation(initialCars:int, initialSituation:float, newCars:int) -> tuple((int, float)):
    maxCapacity = initialCars*(100/initialSituation)
    cars = initialCars+newCars
    newSituation = initialSituation + cars/maxCapacity
    return cars, newSituation


def carsDistribution(people: int, roadIndex:int=0) -> int:
    additionalLoad = people * initialRoadParameters[roadIndex]["peoplePercent"]

    return additionalLoad
    
    
def getRoadData(roadIndex:int=0, people:int=0) -> tuple((int, float)):
    _initialCars = initialRoadParameters[roadIndex]["absolute"]
    _initialLoad = initialRoadParameters[roadIndex]["relative"]
    return calculateRoadSituation(_initialCars, _initialLoad, carsDistribution(people, roadIndex=roadIndex))


def calculateCars(sqArea: int, isResident: bool) -> int: #! Multiply by PeopleOfRimeV2 
    if isResident:
        workPeople = sqArea / newBuildingsData["metersPerPersonResidental"] * capable
    else:
        workPeople = sqArea / newBuildingsData["metersPerPersonOffice"]
    cars = workPeople * autoUsers / peoplePerCar

    return floor(cars)


def peopleAtPoint(time:float, houseTimes:list((float, float, ...)), houseResidents:list((int, int, ...))):
    peopleAmount = 0
    
    n = min(len(houseTimes), len(houseResidents))
    houseResidents = houseResidents[:n]
    houseTimes = houseTimes[:n]

    workingPublicHouseResidents = [residents*capable*publicUsers for residents in houseResidents]
    # print(workingPublicHouseResidents)
    for i in range(n):
        peopleAmount+=peopleOfTimeV2(time-houseTimes[i], workingPublicHouseResidents[i])
    peopleAmount = floor(peopleAmount)
    # print(peopleAmount)
    return peopleAmount


def calculateColor(n: int):
    n=min(n, 100)
    n=max(0, n)
    n = int(n)
    colorLevelr = 0
    colorLevelg = 0
    if (0 <= n <= 50):
        colorLevelr = (n / 50) * 255
        colorLevelg = 255
    elif (50 < n <= 100):
        colorLevelr = 255
        colorLevelg = 255 - ((n-50) / 50) * 255
    
    return ((colorLevelr, colorLevelg, 50))


    
if __name__ == "__main__":
    print(peopleOfTime(7.5, 100))
    print(calculateRoadSituation(781, 50.0, 40))
    peopleAtPoint(7.5, (0.1, 0.1, 0.1), (1000, 2000, 3000))
    values = []
    x = []
    for i in range(0, 2400, 1):
        values.append(peopleAtPoint(i/100, (0.1, 0.1, 0.1), (1000, 2000, 3000)))
        x.append(i/100)
    plt.plot(x, values)
    plt.show()

    