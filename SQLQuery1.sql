select Year, sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs
join star.DimDate as dd
on fs.InvoiceDateID = dd.DateID
group by Year
order by Year

select fs.CustomerId, CustomerName, count(distinct InvoiceId) as 'Total No of invoices', sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs 
join star.DimCustomer as dc 
on fs.CustomerId = dc.CustomerId 
group by fs.CustomerId, CustomerName 
order by 'Total Sales' desc


select fs.CustomerId, CustomerName , avg(NumberOfDaysReturned) as 'Average Days returned'
from [star].[FactGenre] as fs
join star.DimCustomer as dc 
on fs.CustomerId = dc.CustomerId 
group by fs.CustomerId, CustomerName
order by 'Average Days returned'

SELECT CustomerName, OrderDateID, NumberOfDaysReturned
FROM ( SELECT CustomerId, OrderDateID, NumberOfDaysReturned,
              ROW_NUMBER() OVER (partition by CustomerId  ORDER BY OrderDateID desc) as rn
       FROM star.FactGenre
     ) as temp
join star.DimCustomer as dc
on temp.CustomerId = dc.CustomerId
WHERE temp.rn = 1
order by NumberOfDaysReturned desc

---
select
    CustomerId,
    Count(distinct MonthOfYear) as month,
    Year
from star.FactGenre as fg
join star.DimDate as dd
on dd.DateID = fg.OrderDateID
group by CustomerId, Year
order by CustomerId

with temp as
(
	select CustomerId, Year, Count(distinct MonthOfYear) as Month
	from star.FactGenre as fg
	join star.DimDate as dd
	on dd.DateID = fg.OrderDateID
	group by CustomerId, Year
)
select distinct dc.CustomerName, temp.CustomerId, Year, Month
from temp
join star.DimCustomer as dc
on dc.CustomerId = temp.CustomerId
order by temp.CustomerId

with temp as (
	select CustomerId, Count(distinct Year) as Year
	from star.FactGenre as fg
	join star.DimDate as dd
	on dd.DateID = fg.OrderDateID
	group by CustomerId
)
select temp.CustomerId, CustomerName, Year
from temp
join star.DimCustomer as dc
on dc.CustomerId = temp.CustomerId
order by temp.CustomerId

select distinct *
from star.FactGenre as fg
join star.DimDate as dd
on dd.DateID = fg.OrderDateID
order by CustomerId

---
select de.EmployeeId, count(InvoiceId) as 'Total Invoices'
from star.FactSales as fs
right join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
group by de.EmployeeId

select fs.EmployeeId, EmployeeName, FullDate, MonthofYear, Year, count(InvoiceID) as 'Total Invoices'
from star.FactSales as fs
join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
join star.DimDate as dd
on dd.DateID = fs.InvoiceDateID
group by fs.EmployeeId, EmployeeName, FullDate, MonthofYear, Year
order by EmployeeId,MonthOfYear,Year;

with temp as
(
    select EmployeeId, Year, MonthOfYear, count(fs.InvoiceId) as Total_Invoices, sum(fs.ExtendedPrice) as Total_Sales
	from star.FactSales as fs
	join star.DimDate as dd
	on dd.DateID = fs.InvoiceDateID
	group by EmployeeId, Year, MonthOfYear
)
select temp.EmployeeId, de.EmployeeName, MonthOfYear,Year, Total_Invoices, Total_Sales
from temp
join star.DimEmployee as de
on de.EmployeeId = temp.EmployeeId
order by temp.EmployeeId, MonthOfYear, Year

select distinct EmployeeId
from star.DimEmployee

select *
from star.DimDate

---
select *
from star.FactGenre as fg
join star.DimDate as dd
on fg.OrderDateID = dd.DateID