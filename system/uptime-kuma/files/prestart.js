// SPDX-License-Identifier: AGPL-3.0-or-later
// Runs in Uptime Kuma's container before Kuma itself, on every start:
// - First start (no database yet): SQLite, so Kuma never shows its database
//   page, which whoever reaches it first could fill in (with their own
//   MariaDB, say).
// - Later starts: the admin gets KUMA_USERNAME and KUMA_PASSWORD, so they
//   are what you and AutoKuma sign in with even when the admin was made by
//   hand in Kuma's wizard, or the password was changed (here or in Kuma).
// It never stops Kuma from starting: on any problem it says why and exits,
// and Kuma starts as it would without it.
// No dollar-brace placeholders in here: NepFleet would fill them in when it
// renders the file.
const fs = require("fs");
const path = require("path");
const kumaRequire = require("module").createRequire("/app/server/server.js");

const username = (process.env.KUMA_USERNAME || "").trim();
const password = process.env.KUMA_PASSWORD || "";

// A database that doesn't answer (an external MariaDB that is down) must not
// hold Kuma back.
process.on("uncaughtException", (e) => {
    // Kuma's embedded MariaDB keeps a connection open that ends, with this
    // error, when it stops.
    if (e && e.code === "PROTOCOL_CONNECTION_LOST") {
        return;
    }
    console.error("[nepfleet] admin check failed: " + (e && e.message));
    process.exit(0);
});
setTimeout(() => {
    console.error("[nepfleet] admin check: no answer from the database within 60 s; skipped");
    process.exit(0);
}, 60 * 1000).unref();

async function main() {
    const Database = kumaRequire("./database");
    Database.initDataDir({});

    const configPath = path.join(Database.dataDir, "db-config.json");
    const sqlitePath = path.join(Database.dataDir, "kuma.db");
    if (!fs.existsSync(configPath) && !fs.existsSync(sqlitePath) && !process.env.UPTIME_KUMA_DB_TYPE) {
        Database.writeDBConfig({ type: "sqlite" });
        console.log("[nepfleet] database: SQLite");
        return;
    }
    if (!username || !password) {
        console.log("[nepfleet] admin check: KUMA_USERNAME or KUMA_PASSWORD is not set; skipped");
        return;
    }
    if (kumaRequire("check-password-strength").passwordStrength(password).value === "Too weak") {
        console.error("[nepfleet] admin check: KUMA_PASSWORD is too weak for Kuma (at least 6 characters, from at least two of: lowercase, uppercase, digits, symbols); the admin keeps its password");
        return;
    }

    const { R } = kumaRequire("redbean-node");
    const passwordHash = kumaRequire("./password-hash");
    await Database.connect(false, false, true);
    try {
        const users = await R.getAll("SELECT id, username, password, active FROM `user`");
        if (users.length === 0) {
            // Kuma isn't set up yet; the setup service creates the admin.
            return;
        }
        let user = users.find((u) => String(u.username).trim() === username);
        if (!user) {
            if (users.length > 1) {
                console.error("[nepfleet] admin check: Kuma has several users and none is " + username + "; nothing changed");
                return;
            }
            // Kuma has one user: the admin made in its wizard under another name.
            user = users[0];
            await R.exec("UPDATE `user` SET username = ? WHERE id = ?", [username, user.id]);
            console.log("[nepfleet] admin renamed from " + user.username + " to " + username);
        }
        if (!passwordHash.verify(password, user.password)) {
            await R.exec("UPDATE `user` SET password = ? WHERE id = ?", [await passwordHash.generate(password), user.id]);
            console.log("[nepfleet] admin " + username + ": password set from KUMA_PASSWORD");
        }
        if (!user.active) {
            await R.exec("UPDATE `user` SET active = 1 WHERE id = ?", [user.id]);
            console.log("[nepfleet] admin " + username + ": activated");
        }
    } finally {
        // An embedded MariaDB started for this check must be gone before Kuma
        // starts its own on the same files.
        const { EmbeddedMariaDB } = kumaRequire("./embedded-mariadb");
        const child = EmbeddedMariaDB.hasInstance() ? EmbeddedMariaDB.getInstance().childProcess : null;
        const exited = child ? new Promise((resolve) => child.once("close", resolve)) : null;
        await Database.close();
        if (exited) {
            // Kuma stops it with SIGINT, which mariadbd ignores.
            if (child.exitCode === null && child.signalCode === null) {
                child.kill("SIGTERM");
            }
            await exited;
            console.log("[nepfleet] admin check: embedded MariaDB stopped");
        }
    }
}

main().then(
    () => process.exit(0),
    (e) => {
        console.error("[nepfleet] admin check failed: " + e.message);
        process.exit(0);
    }
);
