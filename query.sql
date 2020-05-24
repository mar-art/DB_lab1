--вивести регіон та найвищу ціну, що була в цьому регіоні.
select max(avgprice), region
from Prices
INNER JoIN Regions on
Regions.id = Prices.id
GROUP BY regions.region;
--запит 2 - Вивести регіон та % отриманих даних про авокадо з цього регіону відносно решти регіонів.
SELECT region, 
 round( COUNT(*) * 100 / ( SELECT COUNT(*) FROM Regions ), 2 ) as PERC
FROM Avocado
JOIN Regions 
ON Avocado.id=Regions.id
GROUP BY region
ORDER BY PERC DESC;

--запит 3 - вивести динаміку змін цін по місяцях.
SELECT avgprice, month
FROM Prices
JOIN Months 
ON Prices.id=Months.id
GROUP BY month;
