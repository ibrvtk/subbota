BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "session" (
    "id" TEXT PRIMARY KEY,
    "p1_choice" TEXT,
    "p2_choice" TEXT,
    "attacker_side" INTEGER,
    "p1_id" INTEGER,
    "p2_id" INTEGER
);

COMMIT;