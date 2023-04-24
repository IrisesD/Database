-- Q1
create database if not exists lab1;
use lab1;

drop table if exists Reserve;
drop table if exists Borrow;
drop table if exists Book;
drop table if exists Reader;

create table Book(
	ID char(8),
    name varchar(10) not null,
    author varchar(10),
    price float,
    status int default 0 check (status in (0,1,2)),
    borrow_Times int default 0 check (borrow_Times>=0),
    reserve_Times int default 0 check (reserve_Times>=0),
    constraint PK_Book primary key(ID)
);

create table Reader(
	ID char(8),
    name varchar(10),
    age int check (age>=0),
    address varchar(20),
    constraint PK_Reader primary key(ID)
);

create table Borrow(
	book_ID char(8),
    reader_ID char(8),
    borrow_Date date,
    return_Date date,
    constraint PK_Borrow primary key(book_ID,reader_ID,borrow_Date),
    constraint FK_Borrow_Book foreign key(book_ID) references Book(ID),
    constraint FK_Borrow_Reader foreign key(reader_ID) references Reader(ID)
);

create table if not exists Reserve(
	book_ID char(8),
    reader_ID char(8),
    reserve_Date date default (current_date),
    take_Date date,
    constraint PK_Borrow primary key(book_ID,reader_ID,reserve_Date),
    constraint FK_Reserve_Book foreign key(book_ID) references Book(ID),
    constraint FK_Reserve_Reader foreign key(reader_ID) references Reader(ID),
    constraint CHK_Reserve check (take_Date<reserve_Date)
);
