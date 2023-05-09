drop trigger if exists AutoUpdateWhenInsert;
Delimiter //
Create Trigger AutoUpdateWhenInsert After Insert ON Reserve For Each Row
BEGIN
    -- TODO:AutoUpdateWhenInsert
    -- 当一本书被预约时, 自动将 Book 表中相应图书的 status 修改为 2，并增加 reserve_Times；
    UPDATE Book
    set status=2, reserve_Times = reserve_Times+1
    where ID = new.book_ID;
END //
DELIMITER ;
drop trigger if exists AutoUpdateWhenDelete;
Delimiter //
Create Trigger AutoUpdateWhenDelete After DELETE ON Reserve For Each Row
BEGIN
    -- TODO:AutoUpdateWhenDelete
    -- 当某本预约的书被借出时或者读者取消预约时, 自动减少 reserve_Times
    UPDATE Book
    set reserve_Times = reserve_Times - 1
    where ID = old.book_ID;
    IF NOT EXISTS(
        SELECT * FROM Reserve WHERE book_id = OLD.book_id
    ) THEN
        UPDATE Book SET status = 0 WHERE id = OLD.book_id;
    END IF;
END //
DELIMITER ;