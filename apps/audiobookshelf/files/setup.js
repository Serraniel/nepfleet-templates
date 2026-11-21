// SPDX-License-Identifier: AGPL-3.0-or-later
// Creates Audiobookshelf's root user from ADMIN_USER and ADMIN_PASSWORD
// before the app is reachable, so its "create the root user" screen is never
// open to whoever finds the domain first.
//
// Audiobookshelf has no setting for an initial user; it takes one through
// POST /init, and only while it has no root user yet. So, before the real
// server starts in this container, this starts it privately (localhost only,
// on the stack's own config volume), asks it, and stops it again. Once a
// root user exists it leaves a marker in /config and later starts skip all
// of this.
//
// Runs with Audiobookshelf's own image (Node, global fetch). No dollar-brace
// placeholders in here: NepFleet would fill them in when it renders the file.
const { spawn } = require("child_process");
const fs = require("fs");

const marker = "/config/.nepfleet-root-user";
if (fs.existsSync(marker)) {
    process.exit(0);
}

const username = process.env.ADMIN_USER;
const password = process.env.ADMIN_PASSWORD;
if (!username || !password) {
    console.error("setup: ADMIN_USER and ADMIN_PASSWORD are required");
    process.exit(1);
}

const port = "13378";
const abs = "http://127.0.0.1:" + port;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const server = spawn("node", ["/app/dist-server/index.js"], {
    cwd: "/app",
    env: { ...process.env, PORT: port, HOST: "127.0.0.1" },
    stdio: ["ignore", "inherit", "inherit"],
});
let exited = null;
const done = new Promise((resolve) => {
    server.on("exit", (code, signal) => {
        exited = signal || code;
        resolve();
    });
});

// SIGINT is Audiobookshelf's clean shutdown (it closes the database).
async function stop(code) {
    if (exited === null) {
        server.kill("SIGINT");
        const timeout = sleep(30000).then(() => server.kill("SIGKILL"));
        await Promise.race([done, timeout]);
    }
    if (code === 0) {
        fs.writeFileSync(marker, "root user set up; delete to check again on the next start\n");
    }
    process.exit(code);
}

// GET /status says whether a root user exists.
async function status() {
    for (let i = 0; i < 150; i++) {
        if (exited !== null) {
            throw new Error("Audiobookshelf exited before it answered: " + exited);
        }
        try {
            const res = await fetch(abs + "/status");
            if (res.ok) {
                return await res.json();
            }
        } catch (e) {
            // not listening yet
        }
        await sleep(2000);
    }
    throw new Error("Audiobookshelf did not answer within 5 minutes");
}

async function main() {
    if ((await status()).isInit) {
        console.log("setup: Audiobookshelf already has its root user, nothing to do");
        return;
    }
    const res = await fetch(abs + "/init", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ newRoot: { username, password } }),
    });
    if (!res.ok) {
        throw new Error("Audiobookshelf refused to create the root user: HTTP " + res.status);
    }
    const login = await fetch(abs + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });
    if (!login.ok) {
        throw new Error("the new root user cannot sign in: HTTP " + login.status);
    }
    console.log("setup: root user created: " + username);
}

main().then(
    () => stop(0),
    (e) => {
        console.error("setup: " + e.message);
        return stop(1);
    },
);
