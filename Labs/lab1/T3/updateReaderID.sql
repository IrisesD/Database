use lab1;
Delimiter //
drop procedure if exists updateReaderID
create procedure updateReaderID(in oldID char(8),in newID char(8), out return_info char(20))
BEGIN
    DECLARE s INT DEFAULT 0;
    DECLARE CONTINUE HANDLER FOR 1146 SET s = 1;
    DECLARE CONTINUE HANDLER FOR SQLSTATE '42S02' SET s = 2;
    -- DECLARE CONTINUE HANDLER FOR SQLWARNING SET @status=1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET s = 3;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET s = 4;

    START TRANSACTION;

    -- TODO:UpdateReaderID
set foreign_key_checks = 0;

    Update Reader
    set ID = newID
    where ID = oldID;

    Update Borrow
    set reader_ID = newID
    where reader_ID = oldID;

    Update Reserve
    set reader_ID = newID
    where reader_ID = oldID;

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