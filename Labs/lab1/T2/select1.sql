use lab1;
select ID, name, borrow_Date
from Book,
     Borrow
where Book.ID = Borrow.book_ID
  and Borrow.reader_ID in (select ID
                           from Reader
                           where name = 'Rose');