***

# ✅ Assumptions for Tests

Before running tests, assume:

```text
BASE_URL=http://127.0.0.1:8000
PROJECT_CODE=XYZ
DOMAIN=DESI
```

Also assume your **client (user machine)** generates IDs.

Example IDs used below (replace freely):

```text
SESSION_ID=90000000000001
DATA_ID=90000000010001
OVERLAY_ID=90000000020001
HISTORY_ID=90000000030001
NODE_ID=5001
ATTRIBUTE_ID=101
```

***

# 🔹 1️⃣ Session Lifecycle Tests

***

## ✅ 1.1 Start Session

```bash
curl -X POST \
"$BASE_URL/$PROJECT_CODE/session/start?session_id=90000000000001&username=atul&hostname=dev-machine"
```
```
curl -X POST \
"http://127.0.0.1:8000/XYZ/session/start?session_id=90000000000001&username=atul&hostname=dev-machine"
```

### ✅ Expected Response

```json
{
  "session_id": 90000000000001,
  "username": "atul",
  "hostname": "dev-machine",
  "active": true
}
```

***

## ✅ 1.2 Get Active Session

```bash
curl "$BASE_URL/$PROJECT_CODE/session/active?username=atul&hostname=dev-machine"
```

✅ Should return the same session.

***

## ✅ 1.3 List Sessions

```bash
curl "$BASE_URL/$PROJECT_CODE/session?username=atul"
```

✅ Should list current and historical sessions.

***

# 🔹 2️⃣ Overlay CRUD Tests

Overlay represents **draft state only**.

***

## ✅ 2.1 Stage CREATE

```bash
curl -X POST \
"$BASE_URL/$PROJECT_CODE/$DOMAIN/overlay/create" \
-H "Content-Type: application/json" \
-d '{
  "overlay_id": 90000000020001,
  "session_id": 90000000000001,
  "node_id": 5001,
  "attribute_id": 101,
  "value": {
    "name": "Pump-A",
    "pressure": 12.5
  }
}'
```

```
curl -X POST \
"http://127.0.0.1:8000/XYZ/DESI/overlay/create" \
-H "Content-Type: application/json" \
-d '{
  "overlay_id": 200000001,
  "session_id": 90000000000011,
  "node_id": 5001,
  "attribute_id": 101,
  "value": {
    "name": "Pump-A",
    "pressure": 10
  }
}'
```

✅ This **does not touch live tables yet**.

***

## ✅ 2.2 Preview Overlay (Session View)

```bash
curl \
"$BASE_URL/$PROJECT_CODE/$DOMAIN/overlay/90000000000001"
```

### ✅ Expected

```json
[
  {
    "overlay_id": 90000000020001,
    "session_id": 90000000000001,
    "node_id": 5001,
    "attribute_id": 101,
    "value": {
      "name": "Pump-A",
      "pressure": 12.5
    }
  }
]
```

***

## ✅ 2.3 Stage UPDATE

```bash
curl -X PUT \
"$BASE_URL/$PROJECT_CODE/$DOMAIN/overlay/update/90000000020001" \
-H "Content-Type: application/json" \
-d '{
  "value": {
    "name": "Pump-A1",
    "pressure": 15.0
  }
}'
```

```bash
curl -X PUT \
"http://127.0.0.1:8000/XYZ/DESI/overlay/update" \
-H "Content-Type: application/json" \
-d '{
  "overlay_id": 200000001,
  "session_id": 90000000000011,
  "value": {
    "name": "Pump-A1",
    "pressure": 15.0
  }
}'
```

✅ Overlay row updated, live still untouched.

***

## ✅ 2.4 Stage DELETE

```bash
curl -X DELETE \
"$BASE_URL/$PROJECT_CODE/$DOMAIN/overlay/delete/90000000020001"
```

✅ This sets `value = null` internally (DELETE intent).

***

# 🔹 3️⃣ Commit Tests (Critical)

***

## ✅ 3.1 Commit Session

```bash
curl -X POST \
"$BASE_URL/$PROJECT_CODE/$DOMAIN/commit/90000000000001"
```

### ✅ Expected Response

```json
{
  "status": "committed",
  "session_id": 90000000000001,
  "domain": "DESI"
}
```

***

## ✅ What must happen internally

| Component     | Result                          |
| ------------- | ------------------------------- |
| Live table    | Row created / updated / deleted |
| History table | One row written                 |
| Overlay table | Cleared                         |
| Session       | Marked inactive                 |

***

# 🔹 4️⃣ Post‑Commit Validation Tests

***

## ✅ 4.1 Overlay Should Be Empty

```bash
curl \
"$BASE_URL/$PROJECT_CODE/$DOMAIN/overlay/90000000000001"
```

✅ Response should be:

```json
[]
```

***

## ✅ 4.2 Session Should Be Inactive

```bash
curl "$BASE_URL/$PROJECT_CODE/session/active?username=atul"
```

✅ Should return `null` or no active session.

***

# 🔹 5️⃣ Error Case Tests (Very Important)

***

## ❌ 5.1 Commit Inactive Session

```bash
curl -X POST \
"$BASE_URL/$PROJECT_CODE/$DOMAIN/commit/90000000000001"
```

✅ Expected Error:

```json
{
  "detail": "Session is not active"
}
```

***

## ❌ 5.2 Invalid Domain

```bash
curl \
"$BASE_URL/$PROJECT_CODE/INVALID/overlay/create"
```

✅ Expected:

```json
{
  "detail": "Invalid domain: INVALID"
}
```

***

## ❌ 5.3 Update Non‑existent Overlay

```bash
curl -X PUT \
"$BASE_URL/$PROJECT_CODE/$DOMAIN/overlay/update/999999999" \
-H "Content-Type: application/json" \
-d '{"value": {"x": 1}}'
```

✅ Expected error:

```json
{
  "detail": "Overlay row not found"
}
```

***

# 🔹 6️⃣ Manual DB Validation (Recommended)

After commit, verify directly:

```sql
SELECT * FROM desi_data;
SELECT * FROM desi_data_history;
SELECT * FROM desi_data_overlay;
SELECT * FROM sessions;
```

✅ `desi_data_overlay` → empty  
✅ `session.active = false`  
✅ `history` rows ordered by `history_id`

***

# ✅ ✅ COMPLETE TEST COVERAGE SUMMARY

✅ Session lifecycle  
✅ Overlay CREATE / UPDATE / DELETE  
✅ Overlay preview  
✅ Commit atomicity  
✅ Error handling  
✅ Domain safety

This is **full functional testing via cURL**.

***