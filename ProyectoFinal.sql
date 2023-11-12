/*Borrar la BD anterior*/
drop schema if exists bank;
drop table if exists clients;
drop table if exists accounts;
drop table if exists transactions;
drop table if exists ATM;
drop table if exists repairman;


/*Crear nuevamente la BD con cambios*/
create schema bank;
use bank;


/*Tablas:

    Usuarios*/
create table clients(
    ID          varchar(15),
    password    varchar(15) not null,
    user_name   varchar(15) not null,
    primary key (ID)
)  ENGINE=InnoDB;


    /*Cuentas*/
create table accounts(
    account_number  varchar(15),
    user_ID         varchar(15),
    account_type    varchar(15) not null,
    balance         float(2) not null,
    primary key (account_number),
    foreign key (user_ID) references clients(ID)
        on delete set null
)ENGINE=InnoDB;


    /*Parte administrativa:
    --Cajeros */
create table ATM(
    ID              varchar(15),
    atm_location    varchar(15) not null,
    atm_status      varchar(30) not null,
    primary key (ID)
)ENGINE=InnoDB;


    /*Tecnicos*/
create table repairman(
    ID                  varchar(15),
    password            varchar(15) not null,
    name                varchar(15) not null,
    assigned_atms       varchar(15),
    primary key (ID), 
    foreign key (assigned_atms) references ATM(ID)
        on delete set null
)ENGINE=InnoDB;

   /*Transacciones*/
create table transactions(
    trans_ID        varchar(15),
    account1        varchar(15),
    account2        varchar(15),
    trans_type      varchar(15) not null,
    atm             varchar(15),
    amount          float(2) not null,
    trans_date      DATE not null,
    trans_time      TIME not null,
    primary key (trans_ID),
    foreign key (account1) references accounts(account_number)
        on delete set null,
    foreign key (account2) references accounts(account_number)
        on delete set null,
    foreign key (atm) references ATM(ID)
        on delete set null
)ENGINE=InnoDB;


/*Funciones:*/


/*Datos:

    Users:*/
insert into clients values("0231638","12345","Alan");
insert into clients values("0221564","49521","Jose");
insert into clients values("0073793","79642","Emilio");
insert into clients values("0749274","43281","Danae");
insert into clients values("0047593","68421","Francisco");
insert into clients values("0759347","49358","Daniela");
insert into clients values("0634748","32812","Fernanda");
insert into clients values("0387593","11354","Adriana");
insert into clients values("0237490","38520","Ana");
insert into clients values("0751624","46824","Sofia");
insert into clients values("0952173","46851","Vicente");
insert into clients values("0456881","46821","Andres");
insert into clients values("0068435","68529","Patricia");
insert into clients values("0487627","98451","Jesus");
insert into clients values("0468424","08468","Carmen");

/*  Accounts:*/
insert into accounts values("1","0047593","debit card",288.68);
insert into accounts values("2","0751624","investments",60.58);
insert into accounts values("3","0068435","debit card",509.57);
insert into accounts values("4","0487627","corporate",128.48);
insert into accounts values("5","0759347","corporate",931.83);
insert into accounts values("6","0237490","corporate",898.35);
insert into accounts values("7","0456881","corporate",839.5);
insert into accounts values("8","0231638","debit card",818.86);
insert into accounts values("9","0456881","investments",684.49);
insert into accounts values("10","0456881","credit card",840.01);
insert into accounts values("11","0387593","credit card",817.5);
insert into accounts values("12","0751624","credit card",284.78);
insert into accounts values("13","0487627","debit card",931.51);
insert into accounts values("14","0237490","debit card",509.3);
insert into accounts values("15","0047593","credit card",12.66);
insert into accounts values("16","0237490","credit card",337.88);
insert into accounts values("17","0487627","investments",257.86);
insert into accounts values("18","0759347","debit card",692.29);
insert into accounts values("19","0073793","corporate",774.01);
insert into accounts values("20","0387593","corporate",378.45);
insert into accounts values("21","0068435","investments",185.64);
insert into accounts values("22","0952173","investments",896.55);
insert into accounts values("23","0751624","corporate",677.84);
insert into accounts values("24","0068435","credit card",295.89);
insert into accounts values("25","0634748","investments",714.41);
insert into accounts values("26","0073793","investments",474.35);
insert into accounts values("27","0749274","investments",777.85);
insert into accounts values("28","0952173","credit card",543.35);
insert into accounts values("29","0749274","corporate",214.96);
insert into accounts values("30","0231638","credit card",378.82);
insert into accounts values("31","0068435","corporate",613.16);
insert into accounts values("32","0221564","corporate",258.87);
insert into accounts values("33","0468424","credit card",527.72);
insert into accounts values("34","0487627","credit card",906.67);
insert into accounts values("35","0387593","investments",895.82);
insert into accounts values("36","0759347","credit card",118.33);
insert into accounts values("37","0221564","debit card",861.53);
insert into accounts values("38","0221564","investments",615.1);
insert into accounts values("39","0952173","debit card",928.62);
insert into accounts values("40","0073793","credit card",185.03);
insert into accounts values("41","0456881","corporate",1000.00);
insert into accounts values("42","0456881","investments",900.00);

/*  ATM:*/
insert into ATM values("1284", "Cancun", "OK");
insert into ATM values("8435", "Monterrey", "Pantalla danada");
insert into ATM values("8426", "CDMX", "Ranura de tarjeta trabada");
insert into ATM values("8513", "Guadalajara", "Sin efectivo");
insert into ATM values("7845", "Tijuana", "OK");
insert into ATM values("7514", "Juarez", "Corto circuito");
insert into ATM values("9854", "Jalapa", "OK");
insert into ATM values("8451", "Durango", "OK");
insert into ATM values("0258", "Culiacan", "Dano estructural");
insert into ATM values("3516", "Huatulco", "OK");

/*  Repairman:*/
insert into repairman values("p5012", "tecnico", "Pepe", "1284");
insert into repairman values("a8459", "gatitos", "Ana", "8426");
insert into repairman values("j2835", "patatas", "Juan", "9854");
insert into repairman values("r9364", "dormir", "Ruben", "3516");
insert into repairman values("b8457", "musica", "Berenice", "0258");

/*  Transacciones:*/

/* source C:/Users/sonic/Documents/UP/Semestre_5/Bases de datos/Final.sql; */