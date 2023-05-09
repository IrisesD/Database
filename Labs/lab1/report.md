## Database Lab1 Report
**PB20000215 丁程**

### 一、实验目的
本次实验的主要目标是通过编写一系列的SELECT查询语句和过程化SQL以及触发器来加深对数据库操作的理解。这次实验将帮助我们理解如何查询数据库中的数据，以及如何创建和使用过程化SQL来处理更复杂的数据库操作。通过实践操作，我们可以更好地理解SQL语句的语法和执行方式，以及数据库的基本工作原理。

### 二、实验环境
本次实验使用Datagrip进行。操作系统为MacOS Monterey 12.6.2。

### 三、实验过程
实验的过程主要包含了以下几个步骤：

1. 根据实验要求，创建相应的数据库和表，将相应的要求用表约束的形式写下。将提供的初始化插入数据放进来，这样运行之后完成对数据库和各个表的初始化。
2. T2要求为编写SELECT查询语句，以满足实验中提出的数据查询需求。主要涉及到了基础查询、连接查询、分组查询、排序等操作。具体代码在附件中，这里不再赘述。
3. T3要求编写updateReaderID过程，首先将ppt中的错误处理框架复制过来，这题额外的要求是本题要求不得使用外键定义时的 on update cascade，在这里我们只要在需要修改外键的代码前面加上一行：
```
set foreign_key_checks = 0;
```
再在需要修改外键的代码之后重新使用：
```
set foreign_key_checks = 1;
```
将对外键的检查恢复即可。
在错误处理框架中，需要考虑的是oldID不存在的情况和newID已存在的情况，使用两个if语句结合select进行判断即可。其余的正常情况只需正常更新ID即可。
4. T4要求编写BorrowBook过程，需要考虑的异常情况有以下几种：
同一天不允许同一个读者重复借阅同一本读书,对应
```
CURDATE() = (select borrow_Date from Borrow where reader_ID = readerID and book_ID = bookID)
```
如果该图书存在预约记录，而当前借阅者没有预约，则不允许借阅,对应
```
bookID in (select book_ID from Reserve where reader_ID != readerID and book_ID = bookID) and
 bookID not in (select book_ID from Reserve where reader_ID = readerID and book_ID = bookID)
```
一个读者最多只能借阅 3 本图书，意味着如果读者已经借阅了 3 本图书并且未归还则不允许再借书,对应：
```
select COUNT(readerID) from Borrow where reader_ID = readerID and 
return_Date is null into borrow_count;
    IF borrow_count >= 3 THEN ...
```
如果借阅者已经预约了该图书，则允许借阅，但要求借阅完成后删除借阅者对该图书的预约记录,对应：
```
IF bookID in (select book_ID from Reserve where reader_ID = readerID and book_ID = bookID) THEN
        DELETE from Reserve where book_ID = bookID;
```
其余情况为正常情况，正常插入完借书记录后修改times和status即可

5. T5要求编写ReturnBook过程，这里异常处理不用考虑什么，直接根据Reserve表的信息更新status为不同的值即可。

6. 要求编写触发器，这题也比较简单，这里不再赘述

### 四、实验结果

对于每题（除触发器外）均编写了测试文件，测试文件覆盖各个异常处理的情况以及正常的情况，经过测试和线下检查，所编写的代码均准确无误。在测试过程中，我们的SQL语句都能够按照预期的方式工作。

### 五、总结与思考

通过本次实验，我们深入了解了SQL查询语句和过程化SQL的使用，对数据库的操作有了更深入的理解。我们学会了如何编写SQL查询语句，以从数据库中查询出所需的数据；同时，我们也了解了如何编写和使用存储过程和触发器，以处理更复杂的数据库操作。