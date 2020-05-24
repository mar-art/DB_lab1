
import cx_Oracle
import re
import chart_studio
from plotly import graph_objects as go
import chart_studio.plotly as py
import chart_studio.dashboard_objs as dash

chart_studio.tools.set_credentials_file(username='maryna.prystavska', api_key='mQKTVtl7vUGw9peQvgBp')

def fileId_from_url(url):
    raw_fileId = re.findall("~[A-z.0-9]+/[0-9]+", url)[0][1: ]
    return raw_fileId.replace('/', ':')

username = 'SYSTEM'
password = 'marynka'
databaseName = "DESKTOP-M72EL4D/xe"

connection = cx_Oracle.connect(username, password, databaseName)
cursor = connection.cursor()

cursor.execute(  """
 select max(avgprice), region
from Prices
INNER JoIN Regions on
Regions.id = Prices.id
GROUP BY regions.region
""" )

region = []
price = []


for row in cursor:
    print("region:", row[0],"price :",row[1])
    price += [row[1]]
    region += [row[0]]

data = [go.Bar(
             x=region,
             y=price
      )]

layout = go.Layout(
    title = '',
    xaxis=dict(
        title='price ',
        titlefont=dict(
            family='Courier New, monospace',
            size=20,
            color='#7d7d7d'
        )
    ),
    yaxis=dict(
        title='region',
        rangemode='nonnegative',
        autorange=True,
        titlefont=dict(
            family='Courier New, monospace',
            size=20,
            color='#7d7d7d'
        )
    )
)

fig = go.Figure(data=data, layout=layout)

price_by_region = py.plot(fig, filename='region -price')

cursor.execute( """
   SELECT region, 
 round( COUNT(*) * 100 / ( SELECT COUNT(*) FROM Regions ), 2 ) as PERC
FROM Avocado
JOIN Regions 
ON Avocado.id=Regions.id
GROUP BY region
ORDER BY PERC DESC
   """)
region = []
perc = []

for row in cursor:
    region.append(row[0])
    perc.append(row[1])

pie_data = go.Pie(
        labels=region,
        values=perc,
        title="Вивести регіон та % отриманих даних про авокадо з цього регіону відносно решти регіонів."
    )
region_percent = py.plot([pie_data], filename='region-percent')


cursor.execute( """
SELECT month, avg(avgprice)
FROM Months 
JOIN Prices
ON Months.id = Prices.id
GROUP BY month
""")

month = []
price = []

for row in cursor:
    print("month", row[0], " price: ", row[1])
    month += [row[0]]
    price += [row[1]]

month_price = go.Scatter(
    x=month,
    y=price,
    mode='lines+markers'
)
data = [month_price]
month_price_url = py.plot(data, filename='month_price')


my_dboard = dash.Dashboard()
first_id = fileId_from_url(price_by_region)
second_id = fileId_from_url(region_percent)
third_id = fileId_from_url(month_price_url)

box_1= {
    'type': 'box',
    'boxType': 'plot',
    'fileId': first_id,
    'title': 'Запит 1 - Вивести регіон та найвищу ціну, що була в цьому регіоні.'
}
box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': second_id,
    'title': 'Запит 2 -  Вивести регіон та % отриманих даних про авокадо з цього регіону відносно решти регіонів.'

}

box_3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': third_id,
    'title': 'Вивести динаміку змін цін по місяцях..'
}

my_dboard.insert(box_1)
my_dboard.insert(box_2, 'below', 1)
my_dboard.insert(box_3, 'right', 2)

py.dashboard_ops.upload(my_dboard, 'Billboard1')


cursor.close()
connection.close()
