select reader_ID, name, COUNT(reader_ID)
from Reader
         JOIN Borrow B on Reader.ID = B.reader_ID and B.borrow_Date > '2022-01-01'
group by reader_ID
order by COUNT(reader_ID) desc
limit 10