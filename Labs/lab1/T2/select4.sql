select ID, name
from Book
where name like '%MySQL%'
  and ID in (select book_ID
             from Borrow
             where return_Date is NULL)