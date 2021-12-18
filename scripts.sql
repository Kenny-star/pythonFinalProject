
CREATE TABLE piunit (
    unitid int NOT NULL auto_increment,
    pi_valuecelsius float NOT NULL,
    pi_valuefahrenheit float NOT NULL,
    PRIMARY KEY (unitid)
);


CREATE TABLE pival (
    valueid int NOT NULL auto_increment,
    value_temp float NOT NULL,
	value_hum float NOT NULL,
    timestamp_ datetime NOT NULL,
    PRIMARY KEY (valueid)
);


CREATE TABLE summary (
    id int NOT NULL auto_increment,
    pi_value float NOT NULL,
    valueid int NOT NULL,
    unitid int NOT NULL,
    name varchar(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT FK_Type FOREIGN KEY (valueid)
    REFERENCES pival(valueid),
    CONSTRAINT FK_Unit FOREIGN KEY (unitid)
    REFERENCES piunit(unitid),
    CONSTRAINT FK_User FOREIGN KEY (name)
    REFERENCES users(name)
);


CREATE TABLE user (
    id int NOT NULL auto_increment,
    public_id varchar(255) NOT NULL UNIQUE,
    name varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL,
    admin boolean NOT NULL default 0,
    PRIMARY KEY (id)
);