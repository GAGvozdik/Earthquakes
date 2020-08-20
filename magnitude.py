from pandas import *
from matplotlib.pyplot import *

# открываю файл с точками карты
file = open("HRESMAP.DAT.txt", 'r')

# массивы куда будут забиваться широты и долготы точек карты
map_longitude = []
map_latitude = []

# заполняю массивы с точками данными из файла, разделяя широты и долготы по точке
for line in file:
    if '.' in line:
        map_longitude.append(float(line[10:20]))
        map_latitude.append(float(line[0:9]))

# создаю основное окно отображения
main_figure = figure(figsize=(20, 10))
ax1 = main_figure.add_subplot(111)
ax1.set_aspect(1.2)

# рисую карту по массивам с точками карты
ax1.scatter(map_longitude, map_latitude, s=0.02, color='black')

# открываю файл с данными о землетрясениях
df = read_csv(r"earthquake_database.csv")

# отмечаю желтыми точками глубинные очаги землетрясений
ax1.scatter(df[df['Depth'] <= 250]['Longitude'],
            df[df['Depth'] <= 250]['Latitude'],
            s=30, color='yellow')
# отмечаю оранжевыми полупрозрачными точками средние по глубине очаги землетрясений
ax1.scatter(df[(df['Depth'] > 40) | (df['Depth'] < 250)]['Longitude'],
            df[(df['Depth'] > 40) | (df['Depth'] < 250)]['Latitude'],
            s=10, color='orange', alpha=0.3)
# отмечаю красными почти прозрачными точками околоповерхностные очаги землетрясений
ax1.scatter(df[df['Depth'] <= 40]['Longitude'],
            df[df['Depth'] <= 40]['Latitude'],
            s=5, color='Red', alpha=0.03)

# создаю второе окно для отображения статистики
statistic_figure = figure(figsize=(13, 5))
ax2 = statistic_figure.add_subplot(121)
ax3 = statistic_figure.add_subplot(122)
ax2.set_aspect(1)

# задаю параметры круговой диаграммы
labels = '40 - 250 км', '> 250 км', '< 40 км'
explode = (0, 0, 0.1)

# создаю список данных для круговой диаграммы с распределением по глубине
m = [len(df[(df['Depth'] > 40) | (df['Depth'] < 250)]),
     len(df[df['Depth'] >= 250]),
     len(df[df['Depth'] <= 40])]

# рисую круговую диаграмму
ax2.pie(m, explode=explode, labels=labels, shadow=True, startangle=90)

# рисую гистограмму по распределению магнитуд землетрясений
ax3.hist(df['Magnitude'], bins=10)

show()
