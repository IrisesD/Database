use lab1;
select ID, name
from Reader
where ID not in (select reader_id
                 from Borrow)
  and ID not in (select reader_id
                 from Reserve);