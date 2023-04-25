use lab1;
Delimiter //
drop procedure if exists borrowBook;
create procedure borrowBook(in readerID char(8), in bookID char(8), out return_info char(20))
BEGIN
    DECLARE s INT DEFAULT 0;
    DECLARE borrow_count INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR 1146 SET s = 1;
    DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02' SET s = 2;
    -- DECLARE CONTINUE HANDLER FOR SQLWARNING SET @status=1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET s = 3;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET s = 4;
    START TRANSACTION;

    -- TODO:borrowBook
set foreign_key_checks = 0;
    -- a) 同一天不允许同一个读者重复借阅同一本读书；
    IF CURDATE() = (select borrow_Date from Borrow where reader_ID = readerID and book_ID = bookID) THEN
        set s = 5;
    end if;

    -- b) 如果该图书存在预约记录，而当前借阅者没有预约，则不允许借阅；
    IF bookID in (select book_ID from Reserve where reader_ID != readerID and book_ID = bookID) and bookID not in
    (select book_ID from Reserve where reader_ID = readerID and book_ID = bookID) THEN
        set s = 6;
    end if;

    -- c) 一个读者最多只能借阅 3 本图书，意味着如果读者已经借阅了 3 本图书并且未归还则不允许再借书；
    select COUNT(readerID) from Borrow where reader_ID = readerID and return_Date is null into borrow_count;
    IF borrow_count >= 3 THEN
        set s = 7;
    end if;

    -- d) 如果借阅者已经预约了该图书，则允许借阅，但要求借阅完成后删除借阅者对该图书的预约记录；
    IF bookID in (select book_ID from Reserve where reader_ID = readerID and book_ID = bookID) THEN
        DELETE from Reserve where book_ID = bookID;
    end if;

    -- e) 借阅成功后图书表中的 times 加 1；
    -- f) 借阅成功后修改 status。
    IF s = 0 or s = 8 THEN
        UPDATE Book
        set borrow_Times = borrow_Times + 1
        where ID = bookID;
        INSERT into Borrow (book_ID, reader_ID, borrow_Date, return_Date)
            VALUES (bookID, readerID, NOW(), null);
        UPDATE Book
        set status = 1
        where ID = bookID;
    end if;

set foreign_key_checks = 1;

    IF s = 0 THEN
        SET return_info = 'ok';
        COMMIT;
    ELSE
        CASE s
            WHEN 1 THEN
                SET return_info = 'no such table';
                COMMIT;
            WHEN 2 THEN
                SET return_info = 'no such table';
                COMMIT;
            WHEN 3 THEN
                SET return_info = 'not found';
                COMMIT;
            WHEN 4 THEN
                SET return_info = 'sql exception';
                COMMIT;
            WHEN 5 THEN
                SET return_info = 'duplicate borrow';
                COMMIT;
            WHEN 6 THEN
                SET return_info = 'reserved by others';
                COMMIT;
            WHEN 7 THEN
                SET return_info = 'max borrow nums';
                COMMIT;

        END CASE;
        ROLLBACK;
    END IF;
END //
Delimiter ;