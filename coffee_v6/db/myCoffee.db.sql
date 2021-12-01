BEGIN TRANSACTION;
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
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("machineid") REFERENCES "coffeMachine"("id"),
	FOREIGN KEY("productid") REFERENCES "product"("id")
);
CREATE TABLE IF NOT EXISTS "product" (
	"id"	INTEGER,
	"description"	TEXT,
	"cost"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "coffeMachine" (
	"id"	INTEGER,
	"place"	TEXT,
	"coordX"	REAL,
	"coordY"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "capacity" (
	"machineID"	INTEGER,
	"value"	INTEGER,
	"max"	INTEGER,
	"current"	INTEGER,
	PRIMARY KEY("machineID","value"),
	FOREIGN KEY("machineID") REFERENCES "coffeMachine"("id"),
	FOREIGN KEY("value") REFERENCES "coin"("value")
);
CREATE TABLE IF NOT EXISTS "insertCoins" (
	"machineID"	INTEGER,
	"datetime"	TEXT,
	"coinvalue"	INTEGER,
	"quantity"	INTEGER,
	PRIMARY KEY("machineID","datetime","coinvalue")
);
INSERT INTO "coin" ("value","description") VALUES (10,'.10€'),
 (20,'.20€'),
 (50,'.50€'),
 (100,'1€'),
 (200,'2€'),
 (500,'5€');
INSERT INTO "product" ("id","description","cost") VALUES (1,'Καφές',150),
 (2,'Καφές με γάλα',180),
 (3,'Σοκολάτα',210),
 (4,'Σοκολάτα με γάλα',240);
INSERT INTO "coffeMachine" ("id","place","coordX","coordY") VALUES (1,'myCoffee',0.0,0.0);
INSERT INTO "capacity" ("machineID","value","max","current") VALUES (1,10,10,10),
 (1,20,10,10),
 (1,50,10,10),
 (1,100,10,10),
 (1,200,10,10),
 (1,500,10,10);
CREATE INDEX IF NOT EXISTS "buyIndex" ON "buy" (
	"machineid"	ASC
);
COMMIT;
