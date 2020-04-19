SELECT region, MAX(averageprice)
FROM Avocado
JOIN Regions ON Avocado.region = Regions.region
JOIN Prices ON Avocado.averageprice = Prices.averageprice
GROUP BY Avocado.region
--запит 2 - Вивести регіон та % отриманих даних про авокадо з цього регіону відносно решти регіонів.
SELECT Avocado.region, 
 round( COUNT(*) * 100 / ( SELECT COUNT(*) FROM Regions ), 2 ) as PERC
FROM Avocado
JOIN Regions 
ON Avocado.region=Regions.region
GROUP BY region
ORDER BY PERC DESC

--запит 3 - вивести динаміку змін цін по місяцях.
SELECT averageprice, month
FROM Avocado
JOIN Months 
ON Avocado.month=Months.month
GROUP BY month