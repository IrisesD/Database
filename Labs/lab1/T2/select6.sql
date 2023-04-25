select ID, name
from Reader
where ID not in (select reader_ID
                 from Borrow
                 where book_ID in (select ID
                                   from Book
                                   where author = 'John'))