// SPDX-License-Identifier: AGPL-3.0-or-later
// Creates Immich's admin from ADMIN_EMAIL, ADMIN_PASSWORD and ADMIN_NAME on
// the first start, so the "create admin account" page is never open to
// whoever finds the domain first. Immich takes this only while it has no
// admin; once one exists, this does nothing more than finish the welcome
// steps for that admin when it can sign in with these credentials.
// Runs with the Immich server's own image (Node with fetch). No dollar-brace
// placeholders in here: NepFleet would fill them in when it renders the file.

const email = process.env.ADMIN_EMAIL;
const password = process.env.ADMIN_PASSWORD;
const name = process.env.ADMIN_NAME || "Admin";
if (!email || !password) {
    console.error("ADMIN_EMAIL and ADMIN_PASSWORD are required");
    process.exit(1);
}

const immich = (process.env.IMMICH_URL || "http://immich-server:2283") + "/api";

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
setTimeout(() => {
    console.error("Immich didn't answer within 10 minutes");
    process.exit(1);
}, 10 * 60 * 1000).unref();

async function call(method, path, body, token) {
    const headers = { "Content-Type": "application/json" };
    if (token) {
        headers.Authorization = "Bearer " + token;
    }
    const res = await fetch(immich + path, {
        method,
        headers,
        body: body === undefined ? undefined : JSON.stringify(body),
    });
    const text = await res.text();
    let data = null;
    try {
        data = JSON.parse(text);
    } catch {
        data = text;
    }
    return { status: res.status, ok: res.ok, data };
}

// Until Immich answers (on Swarm nothing waits for it, and it migrates its
// database first), keep asking.
async function serverConfig() {
    for (;;) {
        try {
            const res = await call("GET", "/server/config");
            if (res.ok && res.data && typeof res.data.isInitialized === "boolean") {
                return res.data;
            }
            console.log("waiting for Immich: HTTP " + res.status);
        } catch (e) {
            console.log("waiting for Immich: " + e.message);
        }
        await sleep(3000);
    }
}

async function main() {
    const config = await serverConfig();
    if (!config.isInitialized) {
        const res = await call("POST", "/auth/admin-sign-up", { email, password, name });
        if (res.ok) {
            console.log("admin " + email + " created");
        } else if (res.status === 400 && /not available/i.test(String(res.data && res.data.message))) {
            // Someone (or an earlier run) was faster: an admin exists.
            console.log("an admin exists already");
        } else {
            // Never the password: Immich's message says why.
            console.error("Immich refused the admin sign-up (HTTP " + res.status + "): " + JSON.stringify(res.data));
            process.exit(1);
        }
    }

    const login = await call("POST", "/auth/login", { email, password });
    if (!login.ok) {
        // An admin made by hand, or the password was changed in Immich.
        console.log("an admin exists already and these credentials don't sign in: nothing to do");
        return;
    }
    const token = login.data.accessToken;
    // The password is the stack's input, which the user typed: no forced change.
    if (login.data.shouldChangePassword && login.data.isAdmin) {
        await expectOk("password change prompt", call("PUT", "/admin/users/" + login.data.userId, { shouldChangePassword: false }, token));
    }
    // The welcome steps (theme, privacy, storage template) keep their defaults
    // and stay changeable under Administration.
    if (login.data.isAdmin) {
        const admin = await call("GET", "/system-metadata/admin-onboarding", undefined, token);
        if (admin.ok && !admin.data.isOnboarded) {
            await expectOk("server welcome steps", call("POST", "/system-metadata/admin-onboarding", { isOnboarded: true }, token));
        }
    }
    if (!login.data.isOnboarded) {
        await expectOk("user welcome steps", call("PUT", "/users/me/onboarding", { isOnboarded: true }, token));
    }
    await call("POST", "/auth/logout", undefined, token).catch(() => {});
    console.log("Immich is set up: sign in as " + email);
}

async function expectOk(what, pending) {
    const res = await pending;
    if (!res.ok) {
        console.error("Immich refused to skip the " + what + " (HTTP " + res.status + "): " + JSON.stringify(res.data));
        process.exit(1);
    }
}

main().then(
    () => process.exit(0),
    (e) => {
        console.error("setup: " + e.message);
        process.exit(1);
    },
);
