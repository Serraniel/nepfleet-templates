// SPDX-License-Identifier: AGPL-3.0-or-later
// Does what `openclaw onboard` would ask for, before the gateway starts:
//  - on the first start, onboarding without prompts (upstream's headless
//    bootstrap): local gateway, its token from OPENCLAW_GATEWAY_TOKEN, and
//    the model provider whose API key the stack has. Keys stay references
//    to the environment, so a changed key needs no new onboarding;
//  - Telegram, when the stack has a bot token: the channel, and on every
//    start, who may write to it (TELEGRAM_ALLOWED_USERS). Without a list,
//    OpenClaw's default applies: strangers get a pairing code.
// A configuration made earlier (by hand or by this) is kept: onboarding runs
// only while there is none, or no model provider and now a key.
// Runs with OpenClaw's own image. No dollar-brace placeholders in here:
// NepFleet would fill them in when it renders the file.

const fs = require("node:fs");
const { spawnSync } = require("node:child_process");

function openclaw(...args) {
    const res = spawnSync(process.execPath, ["dist/index.js", ...args], { stdio: "inherit" });
    if (res.status !== 0) {
        console.error("setup: openclaw " + args.slice(0, 2).join(" ") + " failed (exit " + res.status + ")");
        process.exit(1);
    }
}

function readConfig() {
    try {
        return JSON.parse(fs.readFileSync(process.env.OPENCLAW_CONFIG_PATH, "utf8"));
    } catch (e) {
        if (e.code === "ENOENT") {
            return null;
        }
        // JSON5 with comments, written by hand: someone set it up.
        return { gateway: { mode: "unknown" } };
    }
}

// The first provider whose key is set, as onboarding's --auth-choice.
const providers = [
    ["ANTHROPIC_API_KEY", "apiKey"],
    ["OPENROUTER_API_KEY", "openrouter-api-key"],
    ["GEMINI_API_KEY", "gemini-api-key"],
];
const provider = providers.find(([env]) => process.env[env]);

// Onboarding sets gateway.mode; without it, the gateway only starts with
// --allow-unconfigured (and its startup doctor may have written other parts).
// It runs again once a key is given to a stack that has no model provider
// yet (onboarded without a key); a provider set up earlier is kept.
let config = readConfig();
const onboarded = config && config.gateway && config.gateway.mode;
const hasProvider = config && config.auth && config.auth.profiles && Object.keys(config.auth.profiles).length > 0;
if (onboarded && (hasProvider || !provider)) {
    console.log("onboarding done earlier: kept");
} else {
    openclaw(
        "onboard", "--non-interactive", "--accept-risk", "--skip-health",
        "--mode", "local",
        "--auth-choice", provider ? provider[1] : "skip",
        "--secret-input-mode", "ref",
        "--gateway-auth", "token",
        "--gateway-token-ref-env", "OPENCLAW_GATEWAY_TOKEN",
        "--gateway-bind", "loopback",
        "--skip-channels", "--skip-skills", "--skip-search", "--skip-ui",
        "--no-install-daemon",
    );
    console.log("onboarded, model provider: " + (provider ? provider[0] : "none"));
    config = readConfig() || {};
}

if (process.env.TELEGRAM_BOT_TOKEN) {
    if (!(config.channels && config.channels.telegram)) {
        // --use-env: the token stays in the environment, not in the file.
        openclaw("channels", "add", "--channel", "telegram", "--use-env");
        console.log("Telegram added");
    }
    const allowed = (process.env.TELEGRAM_ALLOWED_USERS || "")
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
    if (allowed.length > 0) {
        openclaw("config", "set", "--batch-json", JSON.stringify([
            { path: "channels.telegram.dmPolicy", value: "allowlist" },
            { path: "channels.telegram.allowFrom", value: allowed },
        ]));
        console.log("Telegram: only " + allowed.join(", ") + " may write");
    }
}
