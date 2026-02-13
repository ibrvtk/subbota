BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "game" (
    "id" TEXT PRIMARY KEY,
    "start_date" INTEGER, -- int(datetime.now().timestamp())
    -- playerN_name (class Player self.name)
    "p1_name" TEXT,
    "p2_name" TEXT,
    -- 0 - нет действия, 1 - голова, 2 - корпус, 3 - ноги
    "p1_attack" INTEGER DEFAULT 0,
    "p2_attack" INTEGER DEFAULT 0,
    "p1_defense" INTEGER DEFAULT 0,
    "p2_defense" INTEGER DEFAULT 0
);

COMMIT;