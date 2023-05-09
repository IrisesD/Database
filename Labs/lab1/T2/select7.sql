/*
select reader_ID, name, COUNT(reader_ID)
from Reader
         JOIN Borrow B on Reader.ID = B.reader_ID and B.borrow_Date between '2022-01-01' and '2022-12-31'
group by reader_ID
order by COUNT(reader_ID) desc
limit 10
*/

select reader_ID, name, COUNT(reader_ID)
from Reader
         JOIN Borrow B on Reader.ID = B.reader_ID and B.borrow_Date between '2022-01-01' and '2022-12-31'
group by reader_ID
having COUNT(reader_ID) >= (select COUNT(reader_ID)
                            from Reader
                                     JOIN Borrow B on Reader.ID = B.reader_ID and
                                                      B.borrow_Date between '2022-01-01' and '2022-12-31'
                            group by reader_ID
                            order by COUNT(reader_ID) desc
                            limit 9,1)
order by COUNT(reader_ID) desc