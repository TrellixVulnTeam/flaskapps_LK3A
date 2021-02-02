create database sc;
\c sc;
create table Student(
    Sno char(9) primary key,
	Sname char(20) unique,
	Ssex char(2),
	Sage smallint,
	Sdept char(20)
	);
create table Course(
    Cno char(10) primary key,
	Cname char(40) NOT NULL,
	Cpno char(4),
	Ccredit smallint);
create table SC(
	Sno char(9),
	Cno char(4),
	Grade smallint);
insert into Student(Sno,Sname,Ssex,Sage,Sdept) values('200215121','����','��',20,'CS');
insert into Student(Sno,Sname,Ssex,Sage,Sdept) values('200215122','����','Ů',19,'CS');
insert into Student(Sno,Sname,Ssex,Sage,Sdept) values('200215123','����','Ů',18,'MA');
insert into Student(Sno,Sname,Ssex,Sage,Sdept) values('200215125','����','��',19,'IS');

insert into Course(Cno,Cname,Cpno,Ccredit) values('1','���ݿ�','5','4');
insert into Course(Cno,Cname,Cpno,Ccredit) values('2','��ѧ',null,'2');
insert into Course(Cno,Cname,Cpno,Ccredit) values('6','���ݴ���',null,'2');
insert into Course(Cno,Cname,Cpno,Ccredit) values('4','����ϵͳ','6','3');
insert into Course(Cno,Cname,Cpno,Ccredit) values('7','PASCAL����','6','4');
insert into Course(Cno,Cname,Cpno,Ccredit) values('5','���ݽṹ','7','4');
insert into Course(Cno,Cname,Cpno,Ccredit) values('3','��Ϣϵͳ','1','4');

insert into SC(Sno,Cno,Grade) values('200215121','1',92);
insert into SC(Sno,Cno,Grade) values('200215121','2',85);
insert into SC(Sno,Cno,Grade) values('200215121','3',88);
insert into SC(Sno,Cno,Grade) values('200215122','2',90);
insert into SC(Sno,Cno,Grade) values('200215122','3',80);