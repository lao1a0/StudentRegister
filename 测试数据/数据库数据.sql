--第一张表

create database test;
create table user(
`学号` varchar(50) primary key,
`姓名` varchar(255),
`班级` varchar(255),
`宿舍` varchar(255),
`学院` varchar(255),
`辅导员` varchar(255)
);
insert into user values('20183614','卢修斯·马尔福','信1803','207','斯莱特林学院','萨拉查·斯莱特林');
insert into user values('20183613','西弗勒斯·斯内普','信1603','407','斯莱特林学院','萨拉查·斯莱特林');
insert into user values('20183013','哈利·波特','信1823','247','格兰芬多学院','戈德里克·格兰芬多');
insert into user values('20183513','赫敏·格兰杰','信1823','247','格兰芬多学院','戈德里克·格兰芬多');
insert into user values('20183523','罗恩·韦斯莱','信1823','247','格兰芬多学院','戈德里克·格兰芬多');

--第二张表

create table teacher(
`姓名` varchar(50),
`UID` varchar(255)
)
insert into teacher values('戈德里克·格兰芬多','UID_wL85bprwzyAigwmf61FnVHWLbP1N')
