CREATE TABLE Avocado(
id char(10) NOT NULL,
averageprice float(10) NULL,
region char(20) NULL,
month char(10) NULL
);

CREATE TABLE Prices(
averageprice float(10) NOT NULL);

CREATE TABLE Months(
month char(10) NOT NULL);

CREATE TABLE Regions(
region char(20) NOT NULL);

ALTER TABLE Avocado ADD CONSTRAINT id_pk PRIMARY KEY (id);
ALTER TABLE Prices ADD CONSTRAINT averageprice_pk PRIMARY KEY (averageprice);
ALTER TABLE Months ADD CONSTRAINT month_pk PRIMARY KEY (month);
ALTER TABLE Regions ADD CONSTRAINT region_pk PRIMARY KEY (region);

ALTER TABLE Avocado
ADD CONSTRAINT averageprice_fk FOREIGN KEY (averageprice) REFERENCES Prices (averageprice);
ALTER TABLE Avocado
ADD CONSTRAINT month_fk FOREIGN KEY (month) REFERENCES Months (month);
ALTER TABLE Avocado
ADD CONSTRAINT region_fk FOREIGN KEY (region) REFERENCES Regions (region);