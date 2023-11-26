# Track sales per day, month, quarter, year?
query_1_quarter = '''select Quarter, Year, 
    sum(ExtendedPrice) as 'Total Sales'
    from star.FactSales as fs
    join star.DimDate as dd
    on fs.InvoiceDateID = dd.DateID
    group by Quarter, Year
    order by Year, Quarter'''
query_1_day = '''select FullDate, Year, 
    sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs
join star.DimDate as dd
on fs.InvoiceDateID = dd.DateID
group by FullDate, Year
order by FullDate'''
query_1_month = '''select MonthOfYear, MonthName, Year, 
    sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs
join star.DimDate as dd
on fs.InvoiceDateID = dd.DateID
group by MonthOfYear, MonthName, Year
order by Year, MonthOfYear'''
query_1_year = '''select Year, 
    sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs
join star.DimDate as dd
on fs.InvoiceDateID = dd.DateID
group by Year
order by Year'''
#  Which album has the most listeners?
query_2 = '''select top %s 
    fl.AlbumId, 
        da.AlbumTitle, 
    sum(fl.PlaylistTrackViews) as [Views]
from star.FactListen as fl
join star.DimAlbum as da
on fl.AlbumId = da.AlbumId
group by fl.AlbumId, da.AlbumTitle
order by [Views] desc'''
query_2_1 = '''	select top %s 
		fl.AlbumId, 
		count(TrackId) as 'No of Track', 
		sum(fl.Milliseconds) as 'Song Duration', 
        da.AlbumTitle, 
        sum(fl.PlaylistTrackViews) as [Views]
	from star.FactListen as fl
	join star.DimAlbum as da
	on fl.AlbumId = da.AlbumId
	join star.DimGenre as dg
	on fl.GenreId = dg.GenreId
	group by fl.AlbumId, da.AlbumTitle'''
#  Which customers regularly buy music?
query_3_monthyear = '''with temp as
(
    select CustomerId, Year, Count(distinct MonthOfYear) as 'Month'
    from star.FactGenre as fg
    join star.DimDate as dd
    on dd.DateID = fg.OrderDateID
    group by CustomerId, Year
)
select temp.CustomerId, dc.CustomerName, Year, Month
from temp
join star.DimCustomer as dc
on dc.CustomerId = temp.CustomerId
order by temp.CustomerId'''
query_3_year = '''with temp as 
(
    select CustomerId, Count(distinct Year) as Year
    from star.FactGenre as fg
    join star.DimDate as dd
    on dd.DateID = fg.OrderDateID
    group by CustomerId
)
select top %s temp.CustomerId, dc.CustomerName, Year
from temp
join star.DimCustomer as dc
on dc.CustomerId = temp.CustomerId
order by temp.CustomerId
'''
#  Which customer spends the most money for buying album?
# TODO: - check distinct InvoiceID, - đúng khum má
query_4 = '''select top %s fs.CustomerId, 
    CustomerName, 
    count(InvoiceId) as 'Total No of invoices',
    sum(ExtendedPrice) as 'Total Sales'
from star.FactSales as fs 
join star.DimCustomer as dc 
on fs.CustomerId = dc.CustomerId 
group by fs.CustomerId, CustomerName 
order by 'Total Sales' desc'''

#  Which employee helps achieve invoices the most?
query_5 = '''select de.EmployeeId, de.EmployeeName, count(InvoiceId) as 'Total Invoices'
from star.FactSales as fs
right join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
group by de.EmployeeId,de.EmployeeName'''
query_5_time = '''select 
    fs.EmployeeId, 
    EmployeeName, 
    FullDate, 
    MonthofYear, Year,
    count(InvoiceID) as 'Total Invoices'
from star.FactSales as fs
join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
join star.DimDate as dd
on dd.DateID = fs.InvoiceDateID
group by fs.EmployeeId, EmployeeName, FullDate, MonthofYear, Year
order by fs.EmployeeId'''
query_5_year = '''with temp as
(
    select EmployeeId, Year, MonthOfYear, 
        count(fs.InvoiceId) as Total_Invoices, 
        sum(fs.ExtendedPrice) as Total_Sales
	from star.FactSales as fs
	join star.DimDate as dd
	on dd.DateID = fs.InvoiceDateID
	group by EmployeeId, Year, MonthOfYear
)
select temp.EmployeeId, de.EmployeeName, 
    MonthOfYear,Year, Total_Invoices, Total_Sales
from temp
join star.DimEmployee as de
on de.EmployeeId = temp.EmployeeId
order by temp.EmployeeId, MonthOfYear, Year'''
#  Which employee has the highest sales revenue?
query_6 = '''select de.EmployeeId, de.EmployeeName, sum(fs.ExtendedPrice) as Total_Sales
from star.FactSales as fs
right join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
group by de.EmployeeId, de.EmployeeName'''
query_6_time = '''select 
    fs.EmployeeId, 
    EmployeeName, 
    FullDate, 
    MonthofYear, Year,
    sum(fs.ExtendedPrice) as Total_Sales
from star.FactSales as fs
join star.DimEmployee as de
on de.EmployeeId = fs.EmployeeId
join star.DimDate as dd
on dd.DateID = fs.InvoiceDateID
group by fs.EmployeeId, EmployeeName, FullDate, MonthofYear, Year
order by fs.EmployeeId'''
query_6_year = '''with temp as
(
    select EmployeeId, Year, MonthOfYear, 
        sum(fs.ExtendedPrice) as Total_Sales
	from star.FactSales as fs
	join star.DimDate as dd
	on dd.DateID = fs.InvoiceDateID
	group by EmployeeId, Year, MonthOfYear
)
select temp.EmployeeId, de.EmployeeName, 
    MonthOfYear,Year, Total_Sales
from temp
join star.DimEmployee as de
on de.EmployeeId = temp.EmployeeId
order by temp.EmployeeId, MonthOfYear, Year'''

#  Which music genre is purchased the most by year?
query_7_day = '''
select GenreId, FullDate, count(fs.InvoiceId) as 'Total Invoices' , sum(SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.FactSales as fs
on fs.InvoiceDateID = fg.OrderDateID
join star.DimDate as dd
on fg.OrderDateID = dd.DateID
group by GenreId, FullDate
order by GenreId, FullDate'''
query_7_month = '''
select GenreId, MonthOfYear, count(fs.InvoiceId) as 'Total Invoices' , sum(SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.FactSales as fs
on fs.InvoiceDateID = fg.OrderDateID
join star.DimDate as dd
on fg.OrderDateID = dd.DateID
group by GenreId, MonthOfYear
order by GenreId, MonthOfYear'''
query_7_quarter = '''
select GenreId, Quarter, count(fs.InvoiceId) as 'Total Invoices' , sum(SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.FactSales as fs
on fs.InvoiceDateID = fg.OrderDateID
join star.DimDate as dd
on fg.OrderDateID = dd.DateID
group by GenreId, Quarter
order by GenreId, Quarter'''
query_7_year = '''
select GenreId, Year, count(fs.InvoiceId) as 'Total Invoices' , sum(SumPrice) as 'Total Sales'
from star.FactGenre as fg
join star.FactSales as fs
on fs.InvoiceDateID = fg.OrderDateID
join star.DimDate as dd
on fg.OrderDateID = dd.DateID
group by GenreId, Year
order by GenreId, Year'''

#!  How much gerne music in playlist?
#  How long does it take for customers to return to buy track?
# TODO: đúng khum má?
query_9_avg = '''select top %s 
    fs.CustomerId, 
    CustomerName, 
        avg(NumberOfDaysReturned) as 'Average Days returned'
from [star].[FactGenre] as fs
join star.DimCustomer as dc 
on fs.CustomerId = dc.CustomerId 
group by fs.CustomerId, CustomerName
order by fs.CustomerId'''
query_9_last = '''
SELECT TOP %s CustomerName, OrderDateID, NumberOfDaysReturned
FROM ( 
    SELECT CustomerId, OrderDateID, NumberOfDaysReturned,
            ROW_NUMBER() OVER 
                (partition by CustomerId  ORDER BY OrderDateID desc) as rn
       FROM star.FactGenre
     ) as temp
join star.DimCustomer as dc
on temp.CustomerId = dc.CustomerId
WHERE temp.rn = 1'''
#!  How much genre in playlist?