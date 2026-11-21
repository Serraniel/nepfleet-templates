// Sets the server password from the stack's input before Actual is reachable,
// so nobody who opens the domain first can claim the server.
//
// Actual has no setting for the initial password, only its first-run API.
// It runs in the actual container before the real server starts: it starts
// the server on loopback (so the domain can't reach it), asks it whether a
// password is set, sets it with POST /account/bootstrap if not, and stops it.
// When a password is already set it changes nothing: the input is only taken
// on the first start.
import { spawn } from "node:child_process";

const password = process.env.SERVER_PASSWORD;
if (!password) {
  console.error("SERVER_PASSWORD is empty");
  process.exit(1);
}

const port = "5099";
const base = `http://127.0.0.1:${port}/account`;
const server = spawn("node", ["app.js"], {
  cwd: "/app",
  env: { ...process.env, ACTUAL_HOSTNAME: "127.0.0.1", ACTUAL_PORT: port, SERVER_PASSWORD: "" },
  stdio: ["ignore", "inherit", "inherit"],
});
let exited = false;
server.on("exit", () => { exited = true; });

// Stops the server and waits for it (up to 10s) so its database is closed.
async function finish(code) {
  if (!exited) {
    const stopped = new Promise((r) => server.once("exit", r));
    server.kill("SIGTERM");
    await Promise.race([stopped, new Promise((r) => setTimeout(r, 10000))]);
  }
  process.exit(code);
}

async function waitForServer() {
  for (let i = 0; i < 120; i++) {
    if (exited) throw new Error("the server stopped before it answered");
    try {
      const res = await fetch(`${base}/needs-bootstrap`);
      if (res.ok) return (await res.json()).data;
    } catch {
      // not listening yet
    }
    await new Promise((r) => setTimeout(r, 1000));
  }
  throw new Error("the server did not answer within 2 minutes");
}

try {
  const state = await waitForServer();
  if (state.bootstrapped) {
    console.log("setup: the server password is already set; nothing to do");
    await finish(0);
  }
  const res = await fetch(`${base}/bootstrap`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });
  const body = await res.json().catch(() => ({}));
  if (res.ok && body.status === "ok") {
    console.log("setup: server password set");
    await finish(0);
  }
  if (body.reason === "already-bootstrapped") {
    console.log("setup: the server password is already set; nothing to do");
    await finish(0);
  }
  console.error(`setup: bootstrap failed: ${res.status} ${JSON.stringify(body)}`);
  await finish(1);
} catch (err) {
  console.error(`setup: ${err.message}`);
  await finish(1);
}
