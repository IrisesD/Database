/*
    create view borrow_info as
    select Reader.ID as reader_ID, Reader.name as reader_name, book_ID, B.name as book_name, borrow_Date
    from Reader JOIN Borrow on Reader.ID = Borrow.reader_ID JOIN Book B on B.ID = Borrow.book_ID;
*/
select reader_ID, COUNT(reader_ID)
from borrow_info
where DATEDIFF(borrow_Date, NOW()) < 365
group by reader_ID
order by COUNT(reader_ID) desc