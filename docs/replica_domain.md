# Client Replica Domain Model

## 1. Purpose of This Document

This document describes the **client‑side replica domain** used by the OPE DB system.

Its goal is to make explicit:

*   what the local PostgreSQL database represents,
*   what guarantees it provides,
*   how it is initialized and advanced,
*   and how it should be used by system code and users.

This document intentionally **does not describe SQL schemas or APIs**.  
It describes **domain intent and responsibilities**.

***

## 2. Core Architectural Principle

The OPE DB system is a **replicated‑state system**, not a classic CRUD backend.

### High‑level model

*   **Server PostgreSQL** is the authoritative source of truth.
*   **Client PostgreSQL** is a **materialized replica** of selected server state.
*   **HTTP APIs** act as a *replication transport*, not as the only persistence gateway.
*   **Direct SQL access is allowed on the client replica**, by design.

This architecture enables:

*   offline usage,
*   fast local queries,
*   deterministic synchronization,
*   and integration with external tools (e.g. FreeCAD).

***

## 3. “Cache” vs Replica (Terminology Clarification)

Although some parts of the codebase use the term *cache*, the local PostgreSQL database **is not a cache** in the conventional sense.

### Why it is not a cache

A traditional cache is:

*   best‑effort,
*   ephemeral,
*   discardable,
*   performance‑oriented.

The OPE client database is instead:

*   **persistent**,
*   **queryable via SQL**,
*   **semantically meaningful**,
*   **intentionally replicated**,
*   **safe for direct access**.

### Correct semantic meaning

> The local database is a **replica** (or materialized snapshot) of server state.

For clarity, this document refers to it as the **client replica**, even if existing code uses the word *cache*.

***

## 4. Client Replica Responsibilities

The client replica has **four explicit domain responsibilities**.  
All client‑side logic must align with these responsibilities.

***

### 4.1 Replica Initialization (Snapshot Application)

**Purpose**

Initialize the client replica to a consistent server state.

**Description**

*   Fetch an authoritative snapshot from the server.
*   Populate local LIVE tables.
*   Establish a known, consistent baseline.
*   Reset replication cursors as needed.

**Properties**

*   Idempotent when applied to an empty replica.
*   Establishes the starting point for future history replay.

**Conceptual responsibility**

> “Materialize authoritative server state locally.”

***

### 4.2 Replica Advancement (History Replay)

**Purpose**

Advance the client replica forward in time.

**Description**

*   Fetch incremental history batches from the server.
*   Apply CREATE / UPDATE / DELETE operations deterministically.
*   Preserve correct ordering and referential integrity.

**Properties**

*   Must be repeatable and deterministic.
*   Must not introduce gaps or duplication.
*   Must respect prior snapshot state.

**Conceptual responsibility**

> “Advance local state using authoritative change history.”

***

### 4.3 Replica Cursor & Metadata Management

**Purpose**

Track where the replica is in the replication stream.

**Description**

*   Maintain last‑synced timestamps / history IDs.
*   Ensure idempotency of history replay.
*   Prevent missed or duplicated changes.
*   Support resumable synchronization.

**Properties**

*   Authoritative for the replica only.
*   Must be updated atomically with history application.

**Conceptual responsibility**

> “Record replication progress safely.”

***

### 4.4 Replica Session Alignment

**Purpose**

Ensure server sessions are mirrored correctly on the client side.

**Description**

*   Register server sessions locally when needed.
*   Validate that replication happens in a valid session context.
*   Keep client and server session lifecycles aligned.

**Properties**

*   Required for integrity of history application.
*   Ties domain operations to session boundaries.

**Conceptual responsibility**

> “Mirror server session context locally.”

***

## 5. What the Client Replica Is Allowed to Do

The following are **explicitly allowed and supported**:

✅ Direct SQL queries on the client replica  
✅ External tools querying replica tables  
✅ Local analytics and exploration  
✅ Debugging via PostgreSQL clients

These do **not** violate architecture, because:

*   replication correctness is enforced by domain logic,
*   not by restricting SQL access.

***

## 6. Role of System Code vs User Access

### System code

*   Must follow the replica domain responsibilities.
*   Must use canonical synchronization paths.
*   Must preserve correctness guarantees.

### Users / tools

*   May query the client replica freely.
*   Are not expected to modify replica tables arbitrarily.
*   Are trusted to understand that the replica is read‑optimized state.

***

## 7. Repositories in This Architecture

In this system, repositories **do not exist to hide PostgreSQL**.

Instead, they represent:

> **Stable boundaries for replication‑critical state transitions.**

Examples include:

*   replication cursors,
*   session metadata,
*   snapshot persistence rules,
*   history application boundaries.

Repositories are an **internal discipline**, not an access control mechanism.

***

## 8. Server–Client Responsibility Boundary

| Responsibility       | Server             | Client |
| -------------------- | ------------------ | ------ |
| Authoritative truth  | ✅                  | ❌      |
| Snapshot generation  | ✅                  | ❌      |
| History emission     | ✅                  | ❌      |
| Snapshot application | ❌                  | ✅      |
| History replay       | ❌                  | ✅      |
| Replica metadata     | ❌                  | ✅      |
| Direct SQL access    | ⚠️ (internal only) | ✅      |

***

## 9. Design Implications

This model intentionally:

*   avoids fake abstractions,
*   supports offline‑first workflows,
*   allows powerful local tooling,
*   scales to multiple domains and clients,
*   keeps synchronization logic explicit and testable.

Any future work (API, infra, CI, refactors) should be judged by one question:

> **Does this preserve the correctness of the client replica domain?**

***

## 10. Status

This document describes the **current intended architecture**.  
It should evolve slowly and deliberately as the system grows.

***