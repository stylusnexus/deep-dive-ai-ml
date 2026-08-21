# MCP servers — connecting and building

Two checklists. The first runs before you connect someone else's server;
the second before you ship your own. ☠ = miss it and the failure is a
security incident, not a bug.

---

## A · Before connecting a server

### Vet it
- [ ] ☠ **Read the startup command in full, untruncated** — it executes on your machine with your privileges
- [ ] Maintainer identified; is this an official server, a known org, or an anonymous package?
- [ ] Transitive dependencies checked — a server is a supply-chain surface
- [ ] Source read, or at least the tool handlers and anything doing network I/O
- [ ] No instructions in the server's own text directing the agent outward (fetch, upload, contact)

### Scope it
- [ ] ☠ Credentials scoped to the task, not to the account — this connection does not need every repo/table/mailbox
- [ ] ☠ Read-only first; widen only when a task needs write, then narrow back
- [ ] Production connected **last**, never first
- [ ] Minimal scopes requested; nothing granted "to avoid prompts later"

### Run it safely
- [ ] stdio transport for local servers — nothing listening on a port
- [ ] If HTTP locally: auth token required, or a unix socket
- [ ] Sandboxed where the server executes code
- [ ] All tool calls logged with arguments and results

### Operate it
- [ ] ☠ Human approval gate before anything irreversible or outward-facing — **regardless of what a tool's annotation claims about itself**
- [ ] Everything the server returns treated as untrusted input, never as instructions
- [ ] Periodic re-review: servers update, and the one you audited is not the one running now

---

## B · Before shipping a server

### Design
- [ ] Read-only data exposed as **resources**, not as tools that fetch it
- [ ] Deliberate workflows exposed as **prompts**, so a person invokes them rather than a model inferring them
- [ ] Few composite tools preferred over many granular ones — definitions cost context on every turn
- [ ] Tool descriptions written as prompt engineering, for someone who has never seen your system
- [ ] Return values shaped for a model, not passed through raw from your API
- [ ] Errors name the fix, not just the failure
- [ ] Destructive operations annotated and expected to be gated
- [ ] Example calls included in definitions — schemas give structure, examples give convention

### Security
- [ ] ☠ **Never accept a token that was not issued to this server** (token passthrough is forbidden, not discouraged)
- [ ] ☠ Sessions are **not** authentication — verify every inbound request independently
- [ ] Session IDs from a secure random source, bound to user identity (`<user_id>:<session_id>`)
- [ ] Minimal scopes published; challenge for elevation only when a privileged operation is attempted
- [ ] If proxying a third-party API: **your own per-client consent before forwarding** — this is the confused-deputy fix
- [ ] Redirect URIs matched exactly; no wildcards or patterns
- [ ] OAuth `state` generated securely, stored only after consent, single-use, short-lived
- [ ] HTTPS enforced; private and link-local IP ranges blocked on any URL you fetch

### Before release
- [ ] Handlers unit-tested without a model in the loop
- [ ] Five realistic agent tasks run end to end; trajectory read
- [ ] Wrong-tool, malformed-arguments and tool-ignored failures distinguished — three problems, three fixes
- [ ] README states what the server can reach and with what permissions

---

## The question that precedes both

- [ ] Does this need to be an MCP server at all? One client and one integration is simpler as a direct tool. The protocol earns its cost when the integration is reused — across clients, agents, or people.
