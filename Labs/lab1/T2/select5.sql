select name
from Reader
where ID in (select reader_ID
             from Borrow
             group by reader_ID
             having COUNT(reader_ID) > 10)