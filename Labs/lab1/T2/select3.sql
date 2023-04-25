use lab1;
select author
from (select author, sum(borrow_Times)
      from Book
      group by author
      order by sum(borrow_Times) desc
      limit 1) temp;