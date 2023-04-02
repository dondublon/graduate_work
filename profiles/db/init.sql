create table if not exists users
(
    id          uuid         not null,
    first_name  varchar(100) not null,
    family_name varchar(100) not null,
    father_name varchar(100),
    phone       varchar(20)
);

comment on table users is 'email is in auth-db';

comment on column users.id is 'must be equal to the same in auth-db users';

comment on column users.first_name is 'имя';

comment on column users.family_name is 'фамилия';

comment on column users.father_name is 'отчество';

alter table users
    owner to app;

