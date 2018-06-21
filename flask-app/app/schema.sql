drop table if exists readings;
create table readings (
    id integer primary key autoincrement,
    name text not null,
    reading_date DATETIME not null,
    sent_value float not null,
    recv_value float not null
);
