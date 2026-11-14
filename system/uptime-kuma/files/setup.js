// SPDX-License-Identifier: AGPL-3.0-or-later
// Sets up Uptime Kuma on its first start: SQLite as its database (only when
// Kuma still asks; a database chosen earlier stays), and the admin from
// KUMA_USERNAME and KUMA_PASSWORD, so its setup screen is never open to
// whoever finds it first and AutoKuma can sign in. Once set up, it does
// nothing.
// Runs with Kuma's own image, which ships socket.io-client. No dollar-brace
// placeholders in here: NepFleet would fill them in when it renders the file.
const { io } = require("socket.io-client");

const username = process.env.KUMA_USERNAME;
const password = process.env.KUMA_PASSWORD;
if (!username || !password) {
    console.error("KUMA_USERNAME and KUMA_PASSWORD are required");
    process.exit(1);
}

const kuma = process.env.KUMA_URL || "http://uptime-kuma:3001";

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// The database page answers only while Kuma has no database yet. Until Kuma
// answers at all (on Swarm nothing waits for it), keep asking.
async function chooseDatabase() {
    let res;
    for (;;) {
        try {
            res = await fetch(kuma + "/setup-database-info");
            break;
        } catch (e) {
            console.log("waiting for Uptime Kuma: " + e.message);
            await sleep(2000);
        }
    }
    const info = res.ok ? await res.json().catch(() => null) : null;
    if (!info || !info.needSetup) {
        return;
    }
    const chosen = await fetch(kuma + "/setup-database", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dbConfig: { type: "sqlite" } }),
    });
    if (!chosen.ok) {
        console.error("Uptime Kuma refused the database setup: " + (await chosen.text()));
        process.exit(1);
    }
    console.log("database: SQLite");
}

let socket;
const finish = (code, message) => {
    (code === 0 ? console.log : console.error)(message);
    if (socket) {
        socket.close();
    }
    process.exit(code);
};
setTimeout(() => finish(1, "Uptime Kuma didn't answer within 5 minutes"), 5 * 60 * 1000).unref();

function createAdmin() {
    // Kuma restarts into its main server after the database page; socket.io
    // keeps trying until it's there.
    socket = io(kuma, { reconnectionDelay: 2000 });
    socket.on("connect_error", (e) => console.log("waiting for Uptime Kuma: " + e.message));
    socket.on("connect", onConnect);
}

function onConnect() {
    socket.emit("setup", username, password, (res) => {
        if (res && res.ok) {
            finish(0, "admin " + username + " created");
        } else if (res && /initiali[sz]ed/i.test(String(res.msg))) {
            finish(0, "an admin exists already: nothing to do");
        } else {
            // Never the password: Kuma's message says why (too weak, for example).
            finish(1, "Uptime Kuma refused the setup: " + (res && res.msg));
        }
    });
}

chooseDatabase().then(createAdmin, (e) => finish(1, "database setup: " + e.message));
