/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2023/5/12 17:58:16                           */
/*==============================================================*/


drop table if exists Account;

drop table if exists Branch;

drop table if exists CheckingAccount;

drop table if exists Contact;

drop table if exists Customer;

drop table if exists CustomerBorrowLoan;

drop table if exists Department;

drop table if exists Employee;

drop table if exists Loan;

drop table if exists Manager;

drop table if exists Payment;

drop table if exists RegisterCheckingAccount;

drop table if exists RegisterSavingsAccount;

drop table if exists Responsible;

drop table if exists SavingsAccount;

/*==============================================================*/
/* Table: Account                                               */
/*==============================================================*/
create table Account
(
   Account_ID           char(32) not null,
   Branch_Name          char(32) not null,
   Account_Balance      float,
   Account_Open_Date    date,
   primary key (Account_ID)
);

/*==============================================================*/
/* Table: Branch                                                */
/*==============================================================*/
create table Branch
(
   Branch_Name          char(32) not null,
   Branch_Location      char(32),
   Branch_Assets        float,
   primary key (Branch_Name)
);

/*==============================================================*/
/* Table: CheckingAccount                                       */
/*==============================================================*/
create table CheckingAccount
(
   Account_ID           char(32) not null,
   Branch_Name          char(32),
   Account_Balance      float,
   Account_Open_Date    date,
   Overdraft            float,
   primary key (Account_ID)
);

/*==============================================================*/
/* Table: Contact                                               */
/*==============================================================*/
create table Contact
(
   Customer_ID          char(18) not null,
   Contact_Phone        decimal(11) not null,
   Contact_Name         char(32),
   Contact_Email        char(32),
   Relationship         char(32),
   primary key (Customer_ID, Contact_Phone)
);

/*==============================================================*/
/* Table: Customer                                              */
/*==============================================================*/
create table Customer
(
   Customer_ID          char(18) not null,
   Con_Customer_ID      char(18),
   Contact_Phone        decimal(11),
   Customer_Name        char(32),
   Customer_Phone       decimal(11),
   Customer_Address     char(128),
   primary key (Customer_ID)
);

/*==============================================================*/
/* Table: CustomerBorrowLoan                                    */
/*==============================================================*/
create table CustomerBorrowLoan
(
   Customer_ID          char(18) not null,
   Loan_ID              char(32) not null,
   primary key (Customer_ID, Loan_ID)
);

/*==============================================================*/
/* Table: Department                                            */
/*==============================================================*/
create table Department
(
   Department_ID        char(16) not null,
   Branch_Name          char(32) not null,
   Manager_ID           char(18),
   Department_Name      char(32),
   Department_Type      char(16),
   primary key (Department_ID)
);

/*==============================================================*/
/* Table: Employee                                              */
/*==============================================================*/
create table Employee
(
   Employee_ID          char(18) not null,
   Department_ID        char(16) not null,
   Employee_Name        char(32),
   Employee_Phone       decimal(11),
   Employee_Address     char(64),
   Employee_StartDate   date,
   primary key (Employee_ID)
);

/*==============================================================*/
/* Table: Loan                                                  */
/*==============================================================*/
create table Loan
(
   Loan_ID              char(32) not null,
   Branch_Name          char(32) not null,
   Loan_Amount          float,
   Loan_Payment_Details decimal,
   primary key (Loan_ID)
);

/*==============================================================*/
/* Table: Manager                                               */
/*==============================================================*/
create table Manager
(
   Manager_ID           char(18) not null,
   Department_ID        char(16),
   Manager_Name         char(32),
   Manager_Phone        decimal(11),
   Manager_Address      char(64),
   Manager_Start_Date   date,
   primary key (Manager_ID)
);

/*==============================================================*/
/* Table: Payment                                               */
/*==============================================================*/
create table Payment
(
   Loan_ID              char(32) not null,
   Payment_ID           decimal not null,
   Payment_Date         date,
   Payment_Amount       float,
   primary key (Loan_ID, Payment_ID)
);

/*==============================================================*/
/* Table: RegisterCheckingAccount                               */
/*==============================================================*/
create table RegisterCheckingAccount
(
   Branch_Name          char(32) not null,
   Customer_ID          char(18) not null,
   Account_ID           char(32),
   LastAccess           date,
   primary key (Branch_Name, Customer_ID)
);

/*==============================================================*/
/* Table: RegisterSavingsAccount                                */
/*==============================================================*/
create table RegisterSavingsAccount
(
   Customer_ID          char(18) not null,
   Branch_Name          char(32) not null,
   Account_ID           char(32),
   LastAccess           date,
   primary key (Customer_ID, Branch_Name)
);

/*==============================================================*/
/* Table: Responsible                                           */
/*==============================================================*/
create table Responsible
(
   Customer_ID          char(18) not null,
   Employee_ID          char(18) not null,
   ServiceType          char(32) not null,
   primary key (Customer_ID, Employee_ID)
);

/*==============================================================*/
/* Table: SavingsAccount                                        */
/*==============================================================*/
create table SavingsAccount
(
   Account_ID           char(32) not null,
   Branch_Name          char(32),
   Account_Balance      float,
   Account_Open_Date    date,
   Interest             float,
   CurrencyType         char(32),
   primary key (Account_ID)
);

alter table Account add constraint FK_BranchRegisterAccount foreign key (Branch_Name)
      references Branch (Branch_Name) on delete restrict on update restrict;

alter table CheckingAccount add constraint FK_CheckingAccount foreign key (Account_ID)
      references Account (Account_ID) on delete restrict on update restrict;

alter table Contact add constraint FK_ContactBelongsToCustomer2 foreign key (Customer_ID)
      references Customer (Customer_ID) on delete restrict on update restrict;

alter table Customer add constraint FK_ContactBelongsToCustomer foreign key (Con_Customer_ID, Contact_Phone)
      references Contact (Customer_ID, Contact_Phone) on delete restrict on update restrict;

alter table CustomerBorrowLoan add constraint FK_CustomerBorrowLoan foreign key (Customer_ID)
      references Customer (Customer_ID) on delete restrict on update restrict;

alter table CustomerBorrowLoan add constraint FK_CustomerBorrowLoan2 foreign key (Loan_ID)
      references Loan (Loan_ID) on delete restrict on update restrict;

alter table Department add constraint FK_DepartmentBelongsToBranch foreign key (Branch_Name)
      references Branch (Branch_Name) on delete restrict on update restrict;

alter table Department add constraint FK_ManagerBelongsToDepartment2 foreign key (Manager_ID)
      references Manager (Manager_ID) on delete restrict on update restrict;

alter table Employee add constraint FK_EmployeeBelongsToDepartment foreign key (Department_ID)
      references Department (Department_ID) on delete restrict on update restrict;

alter table Loan add constraint FK_BranchLendLoan foreign key (Branch_Name)
      references Branch (Branch_Name) on delete restrict on update restrict;

alter table Manager add constraint FK_ManagerBelongsToDepartment foreign key (Department_ID)
      references Department (Department_ID) on delete restrict on update restrict;

alter table Payment add constraint FK_PaymentPayForLoan foreign key (Loan_ID)
      references Loan (Loan_ID) on delete restrict on update restrict;

alter table RegisterCheckingAccount add constraint FK_RegisterCheckingAccount foreign key (Branch_Name)
      references Branch (Branch_Name) on delete restrict on update restrict;

alter table RegisterCheckingAccount add constraint FK_RegisterCheckingAccount2 foreign key (Customer_ID)
      references Customer (Customer_ID) on delete restrict on update restrict;

alter table RegisterSavingsAccount add constraint FK_RegisterSavingsAccount foreign key (Customer_ID)
      references Customer (Customer_ID) on delete restrict on update restrict;

alter table RegisterSavingsAccount add constraint FK_RegisterSavingsAccount2 foreign key (Branch_Name)
      references Branch (Branch_Name) on delete restrict on update restrict;

alter table Responsible add constraint FK_Responsible foreign key (Customer_ID)
      references Customer (Customer_ID) on delete restrict on update restrict;

alter table Responsible add constraint FK_Responsible2 foreign key (Employee_ID)
      references Employee (Employee_ID) on delete restrict on update restrict;

alter table SavingsAccount add constraint FK_SavingsAccount foreign key (Account_ID)
      references Account (Account_ID) on delete restrict on update restrict;

