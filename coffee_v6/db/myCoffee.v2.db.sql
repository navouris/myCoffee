BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "CoffeMachine" (
	"id"	INTEGER,
	"place"	TEXT,
	"coordX"	REAL,
	"coordY"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "coin" (
	"value"	INTEGER,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("value")
);
CREATE TABLE IF NOT EXISTS "buy" (
	"id"	INTEGER,
	"cost"	INTEGER NOT NULL,
	"datetime"	TEXT NOT NULL,
	"productid"	INTEGER,
	"machineid"	INTEGER,
	FOREIGN KEY("productid") REFERENCES "product"("id"),
	FOREIGN KEY("machineid") REFERENCES "CoffeMachine"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "product" (
	"id"	INTEGER,
	"description"	TEXT,
	"cost"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "insertCoins" (
	"machineID"	INTEGER,
	"datetime"	TEXT,
	"coinvalue"	INTEGER,
	PRIMARY KEY("machineID","datetime","coinvalue")
);
CREATE TABLE IF NOT EXISTS "loadProduct" (
	"productid"	INTEGER,
	"machineid"	INTEGER,
	"date-time"	INTEGER,
	"ammount"	INTEGER NOT NULL,
	FOREIGN KEY("productid") REFERENCES "product"("id"),
	FOREIGN KEY("machineid") REFERENCES "CoffeMachine"("id"),
	PRIMARY KEY("productid","machineid","date-time")
);
CREATE TABLE IF NOT EXISTS "unloadCoins" (
	"coinid"	INTEGER,
	"machineid"	INTEGER,
	"datetime"	TEXT,
	"ammount"	INTEGER NOT NULL,
	FOREIGN KEY("coinid") REFERENCES "coin"("value"),
	FOREIGN KEY("machineid") REFERENCES "CoffeMachine"("id"),
	PRIMARY KEY("coinid","machineid","datetime")
);
CREATE TABLE IF NOT EXISTS "availableProducts" (
	"machineid"	INTEGER,
	"productid"	INTEGER,
	"quantity"	INTEGER,
	FOREIGN KEY("machineid") REFERENCES "product"("id"),
	FOREIGN KEY("productid") REFERENCES "CoffeMachine"("id"),
	PRIMARY KEY("machineid","productid")
);
INSERT INTO "coin" ("value","description") VALUES (10,'.10€'),
 (20,'.20€'),
 (100,'1€'),
 (200,'2€'),
 (500,'5€');
INSERT INTO "product" ("id","description","cost") VALUES (1,'Καφές',150),
 (2,'Καφές με γάλα',180),
 (3,'Σοκολάτα',210),
 (4,'Σοκολάτα με γάλα',240);
CREATE INDEX IF NOT EXISTS "buyIndex" ON "buy" (
	"machineid"	ASC
);
COMMIT;
