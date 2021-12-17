
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
    PRIMARY KEY (id),
    CONSTRAINT FK_Type FOREIGN KEY (valueid)
    REFERENCES pival(valueid),
    CONSTRAINT FK_Unit FOREIGN KEY (unitid)
    REFERENCES piunit(unitid)
);