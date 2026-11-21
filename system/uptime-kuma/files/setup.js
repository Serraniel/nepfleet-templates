// SPDX-License-Identifier: AGPL-3.0-or-later
// Sets up Uptime Kuma on its first start: the admin from KUMA_USERNAME and
// KUMA_PASSWORD, so its setup screen is never open to whoever finds it first
// and AutoKuma can sign in. Then, and on every later run, it signs in with
// them, so AutoKuma starts only when it can sign in too; a failure says why.
// SQLite as the database is prestart.js's job (before Kuma starts); the
// database page is answered here too, in case Kuma still shows it.
// Runs with Kuma's own image, which ships socket.io-client. No dollar-brace
// placeholders in here: NepFleet would fill them in when it renders the file.
const { io } = require("socket.io-client");
const { passwordStrength } = require("check-password-strength");

const username = process.env.KUMA_USERNAME;
const password = process.env.KUMA_PASSWORD;
if (!username || !password) {
    console.error("KUMA_USERNAME and KUMA_PASSWORD are required");
    process.exit(1);
}
// Kuma's own rule; it refuses such a password for the admin.
if (passwordStrength(password).value === "Too weak") {
    console.error("KUMA_PASSWORD is too weak for Uptime Kuma: use at least 6 characters, from at least two of lowercase, uppercase, digits and symbols");
    process.exit(1);
}

const kuma = process.env.KUMA_URL || "http://uptime-kuma:3001";

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// The database page answers only while Kuma has no database yet. Until Kuma
// answers at all (nothing waits for its health check), keep asking.
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

function connect() {
    // Kuma restarts into its main server after the database page; socket.io
    // keeps trying until it's there.
    socket = io(kuma, { reconnectionDelay: 2000 });
    socket.on("connect_error", (e) => console.log("waiting for Uptime Kuma: " + e.message));
    socket.once("connect", onConnect);
}

function onConnect() {
    socket.emit("setup", username, password, (res) => {
        if (res && res.ok) {
            console.log("admin " + username + " created");
        } else if (!(res && /initiali[sz]ed/i.test(String(res.msg)))) {
            // Never the password: Kuma's message says why (too weak, for example).
            finish(1, "Uptime Kuma refused the setup: " + (res && res.msg));
            return;
        }
        signIn();
    });
}

function signIn() {
    socket.emit("login", { username, password, token: "" }, (res) => {
        if (res && res.ok) {
            finish(0, "signed in as " + username + ": AutoKuma can too");
        } else if (res && res.tokenRequired) {
            finish(1, "the admin " + username + " has two-factor authentication on, so AutoKuma can't sign in: turn it off in Kuma's settings");
        } else {
            // prestart.js gives the admin these credentials when Kuma starts;
            // its lines at the top of Kuma's log say why it didn't.
            finish(1, "can't sign in to Uptime Kuma as " + username + " (" + (res && res.msg) + "): see the first lines of the uptime-kuma log");
        }
    });
}

chooseDatabase().then(connect, (e) => finish(1, "database setup: " + e.message));
