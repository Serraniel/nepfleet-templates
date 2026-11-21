// SPDX-License-Identifier: AGPL-3.0-or-later
// Creates Kutt's admin from ADMIN_EMAIL and ADMIN_PASSWORD on its first start,
// before Kutt serves anything, so its "create admin" page is never open to
// whoever finds the domain first. It does what Kutt's own create-admin does
// (a verified ADMIN, bcrypt with 12 rounds), and only while there is no user
// at all: once anyone exists, it does nothing.
// Runs inside Kutt's container, after its migrations and before it starts,
// with Kutt's own database settings and modules. No dollar-brace placeholders
// in here: NepFleet would fill them in when it renders the file.
const bcrypt = require("/kutt/node_modules/bcryptjs");
const knex = require("/kutt/server/knex");

const email = (process.env.ADMIN_EMAIL || "").trim();
const password = process.env.ADMIN_PASSWORD || "";

async function main() {
    const anyone = await knex("users").select("id").first();
    if (anyone) {
        console.log("setup: a user exists, nothing to do");
        return;
    }
    if (!email || !password) {
        throw new Error("ADMIN_EMAIL and ADMIN_PASSWORD are required");
    }
    // Kutt's sign-in accepts only these lengths.
    if (password.length < 8 || password.length > 64) {
        throw new Error("ADMIN_PASSWORD must be 8 to 64 characters long");
    }
    const hash = await bcrypt.hash(password, await bcrypt.genSalt(12));
    await knex("users").insert({
        email,
        password: hash,
        role: "ADMIN",
        verified: true,
        banned: false,
    });
    console.log("setup: created the admin " + email);
}

main()
    .then(() => knex.destroy())
    .catch((err) => {
        console.error("setup: " + err.message);
        process.exit(1);
    });
