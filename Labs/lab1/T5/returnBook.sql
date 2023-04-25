use lab1;
Delimiter //
drop procedure if exists returnBook;
create procedure returnBook(in readerID char(8), in bookID char(8), out return_info char(20))
BEGIN
    DECLARE s INT DEFAULT 0;
    DECLARE borrow_count INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR 1146 SET s = 1;
    DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02' SET s = 2;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET s = 3;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET s = 4;
    START TRANSACTION;

    -- TODO:returnBook
set foreign_key_checks = 0;
    UPDATE Borrow
    set return_Date = CURDATE()
    where reader_ID = readerID and book_ID = bookID;
    IF bookID in (select book_ID from Reserve where book_ID = bookID) THEN
        UPDATE Book
        set status = 2
        where ID = bookID;
    ELSE
        UPDATE Book
        set status = 2
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

        END CASE;
        ROLLBACK;
    END IF;
END //
Delimiter ;