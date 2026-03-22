# ThreatLens - Example Outputs & Troubleshooting

## 📊 Example Real Analysis Outputs

These are actual examples of what ThreatLens produces during penetration testing.

---

## Example 1: E-commerce API Analysis

### Input Response
```json
{
  "order_id": 12345,
  "user_id": 789,
  "items": [
    {"product": "Laptop", "price": 999.99}
  ],
  "shipping_address": "123 Main St",
  "payment_method": "****1234",
  "status": "pending",
  "internal_notes": "Rush order for VIP customer",
  "fulfillment_center": "DC-East-01"
}
```

### AI Analysis Output
```
================================================================================
[10:45:23] 🔴 2 HIGH - https://shop.example.com/api/orders/12345
================================================================================

[HIGH] IDOR Vulnerability - Predictable Order IDs
The order_id parameter uses sequential integers (12345), allowing enumeration
of all orders in the system without authentication.

Payload: 
  GET /api/orders/12344
  GET /api/orders/12346
  GET /api/orders/12347

Impact: 
  Full access to customer PII (addresses, phone numbers)
  Payment card last 4 digits exposed
  Business intelligence leakage (order volumes, VIP customers)

Test:
  1. Change order_id to sequential values
  2. Verify response contains other users' data
  3. Estimate: ~100,000 orders enumerable

[HIGH] Sensitive Internal Data Exposure
Response contains fields not meant for end-users:
- internal_notes: "Rush order for VIP customer"
- fulfillment_center: "DC-East-01"

Impact:
  Internal business processes revealed
  Fulfillment center locations mapped
  Could aid physical security attacks

Payload:
  Use internal_notes to identify high-value targets
  Map fulfillment centers via order patterns

---
```

---

## Example 2: Authentication API Analysis

### Input Response
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInJvbGUiOiJ1c2VyIiwiaXNfYWRtaW4iOmZhbHNlLCJleHAiOjE3MDk4NTAwMDB9.abc123",
  "user": {
    "id": 123,
    "email": "test@example.com",
    "role": "user",
    "is_admin": false,
    "created_at": "2024-01-01",
    "last_login_ip": "192.168.1.100"
  }
}
```

### AI Analysis Output
```
================================================================================
[10:46:15] 🔴 3 HIGH - https://auth.example.com/api/login
================================================================================

[HIGH] JWT Contains Exploitable Claims
Decoded JWT payload shows:
{
  "user_id": 123,
  "role": "user",
  "is_admin": false
}

Payload:
  1. Decode JWT at jwt.io
  2. Modify: "role": "admin", "is_admin": true
  3. Re-sign with algorithm confusion:
     - Change "alg": "HS256" to "alg": "none"
     - Remove signature
  4. Test with modified token

Impact:
  Privilege escalation to admin role
  Full application compromise

[HIGH] User Enumeration via Login Response
Success returns user_id: 123, failure returns generic error.
This allows mapping all valid user IDs.

Test:
  POST /api/login with random emails
  If response contains user_id → valid account
  If response is generic → no account

Payload:
  Enumerate emails:
    admin@example.com
    user1@example.com
    ...
  Build valid email list for further attacks

[MEDIUM] IP Address Logging Exposed
Response contains "last_login_ip": "192.168.1.100"

Impact:
  User location tracking
  If combined with IDOR: Track all users' IPs
  Privacy violation, potential stalking vector

---
```

---

## Example 3: GraphQL API Analysis

### Input Response
```json
{
  "data": {
    "__schema": {
      "types": [
        {
          "name": "User",
          "fields": [
            {"name": "id"},
            {"name": "email"},
            {"name": "password_hash"},
            {"name": "admin_secret_token"}
          ]
        }
      ]
    }
  }
}
```

### AI Analysis Output
```
================================================================================
[10:47:30] 🔴 2 HIGH - https://api.example.com/graphql
================================================================================

[HIGH] GraphQL Introspection Enabled
Full schema exposed via introspection query. This reveals:
- All available types and fields
- Hidden administrative queries
- Sensitive field names (password_hash, admin_secret_token)

Payload:
  query IntrospectionQuery {
    __schema {
      types {
        name
        fields {
          name
          type { name }
        }
      }
    }
  }

Impact:
  Complete API mapping
  Discovery of admin-only endpoints
  Information for targeted attacks

[HIGH] Sensitive Fields Accessible
Schema reveals fields that should be protected:
- password_hash: Hashed passwords accessible
- admin_secret_token: Admin authentication tokens

Test:
  query {
    users {
      password_hash
      admin_secret_token
    }
  }

Impact:
  Password hash extraction → offline cracking
  Admin token theft → account takeover

Remediation:
  1. Disable introspection in production
  2. Implement field-level authorization
  3. Remove sensitive fields from GraphQL schema

---
```

---

## Example 4: Error Message Analysis

### Input Response
```json
{
  "error": "SQL error: SELECT * FROM users WHERE id='123' OR '1'='1' AND password='invalid'",
  "status": 500,
  "stack_trace": [
    "at Database.query (database.js:45)",
    "at UserController.login (controllers/user.js:23)",
    "at /app/routes/auth.js:15"
  ]
}
```

### AI Analysis Output
```
================================================================================
[10:48:45] 🔴 3 HIGH - https://api.example.com/auth/login
================================================================================

[HIGH] SQL Injection Confirmed
Error message reveals successful SQL injection:
"SELECT * FROM users WHERE id='123' OR '1'='1' AND password='invalid'"

The payload '123' OR '1'='1' was successfully injected into the query.

Payload:
  Start with union-based injection:
    id=123' UNION SELECT 1,2,3,4,5--
  
  Then extract database:
    id=123' UNION SELECT table_name FROM information_schema.tables--
  
  Extract data:
    id=123' UNION SELECT email,password_hash FROM users--

Impact:
  Full database compromise
  All user data extractable
  Potential for OS command execution

[HIGH] Stack Trace Exposure
Full application paths revealed:
- /app/routes/auth.js
- controllers/user.js
- database.js

Impact:
  Application structure mapped
  Technology stack identified (Node.js)
  Aids in finding other vulnerabilities

[MEDIUM] Verbose Error Messages
Production server should not reveal:
- SQL queries
- Stack traces
- Internal file paths

Remediation:
  1. Fix SQL injection (use parameterized queries)
  2. Disable verbose errors in production
  3. Implement generic error messages

---
```

---

## Example 5: API Rate Limiting Test

### Input Response
```
HTTP/1.1 200 OK
Content-Type: application/json
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1709850000

{
  "users": [/* 100 user records */]
}
```

### AI Analysis Output
```
================================================================================
[10:50:10] 🟡 2 MEDIUM - https://api.example.com/users
================================================================================

[MEDIUM] Weak Rate Limiting
Rate limit headers present:
- X-RateLimit-Limit: 1000 requests
- X-RateLimit-Remaining: 999
- X-RateLimit-Reset: 1709850000

However, 1000 requests allows mass data extraction.

Test:
  1. Script to make 999 requests
  2. Extract all user data before limit
  3. Reset occurs in 1 hour → repeat

Impact:
  Complete user database scrapable
  1000 requests × 100 users/request = 100,000 user records
  Rate limit too generous for sensitive endpoint

[MEDIUM] No Authentication on /users Endpoint
Endpoint returns 100 user records per request with no auth.

Payload:
  while true; do
    curl https://api.example.com/users?page=$i
    i=$((i+1))
  done

Impact:
  Public data exposure
  Email harvesting for phishing
  User enumeration

Remediation:
  1. Require authentication
  2. Reduce rate limit (10-50 requests/hour)
  3. Implement pagination limits

---
```

---

## 🔧 Troubleshooting Guide

### Issue 1: Extension Won't Load

**Symptoms:**
```
Error: Failed to load extension
Output → Errors tab shows Python syntax error
```

**Solutions:**

1. **Check Jython Version**
```bash
# Must be 2.7.3
java -jar jython-standalone-2.7.3.jar --version
```

2. **Verify Python Syntax**
```bash
# Test file is valid Python
python2 -m py_compile ai_recon_assistant.py
```

3. **Check Burp Console**
```
Extensions → Errors tab
Look for actual error message
```

4. **Common Fixes**
- Ensure file encoding is UTF-8
- Remove any BOM (Byte Order Mark) from file
- Check for mixed tabs/spaces in indentation

---

### Issue 2: No Responses Being Analyzed

**Symptoms:**
```
Extension loaded
Browsing application
No output in ThreatLens tab
```

**Debug Checklist:**

```python
1. Is API key set?
   → ThreatLens tab → Check "OpenAI API Key" field
   → Click "Save Configuration"

2. Is analysis enabled?
   → Check "Analysis Enabled" checkbox is ON

3. Do responses match filters?
   → Check response Content-Type
   → Must be: application/json, application/xml, etc.
   → Status must be 2xx if filter enabled

4. Is response large enough?
   → Minimum 100 bytes by default
   → Check actual response size in Burp HTTP history

5. Check Burp Console
   → Look for error messages
   → "API Error" indicates API issues
```

**Quick Test:**
```
1. Visit: https://jsonplaceholder.typicode.com/posts/1
2. Should see analysis of JSON response
3. If not, API key or filters are the issue
```

---

### Issue 3: API Errors

**Error: "API Error: 401 Unauthorized"**

**Cause:** Invalid API key

**Fix:**
```
1. Get new key: https://platform.openai.com/api-keys
2. Verify key format: sk-proj-...
3. Re-enter in extension
4. Click "Save Configuration"
```

---

**Error: "API Error: 429 Too Many Requests"**

**Cause:** OpenAI rate limit exceeded

**Fix:**
```
1. Wait 60 seconds and try again
2. Upgrade OpenAI plan if needed
3. Enable more aggressive filtering
4. Use gpt-4o-mini instead of gpt-4o
```

---

**Error: "API Error: Timeout"**

**Cause:** Response too large or network slow

**Fix:**
```python
# Edit extension code
# Increase timeout in call_openai:
response = urllib2.urlopen(req, timeout=60)  # was 30
```

---

### Issue 4: Poor Quality Findings

**Symptoms:**
```
AI returns generic advice
No specific payloads
Lots of false positives
```

**Solutions:**

1. **Use Better Model**
```python
# Change in extension config
"model": "gpt-4o"  # Better than gpt-4o-mini
```

2. **Improve Filtering**
```
Only analyze:
✅ JSON responses (APIs)
✅ Status 200
✅ Response size > 500 bytes
```

3. **Provide More Context**
```python
# Edit prompt to include request details
context = {
    'method': method,
    'url': url,
    'request_params': params,  # Add this
    'request_headers': req_headers,  # Add this
}
```

---

### Issue 5: High API Costs

**Symptoms:**
```
OpenAI bill is $50+ for small assessment
```

**Cost Reduction:**

1. **Enable All Filters**
```
✅ Content-Type filter → Saves 70-80%
✅ Status filter → Saves 30-40%
✅ Scope filter → Saves 50-60%
```

2. **Use Cheaper Model**
```
gpt-4o-mini: ~$0.15 per 1M tokens
gpt-4o: ~$5.00 per 1M tokens
```

3. **Analyze Selectively**
```
Don't leave extension running during:
- Passive browsing
- Clicking around UI
- Testing same endpoints repeatedly

Enable only when:
- Testing new endpoints
- Focused vulnerability hunting
- Analyzing API responses
```

---

### Issue 6: Extension Crashes Burp

**Symptoms:**
```
Burp freezes when extension enabled
High CPU usage
Out of memory errors
```

**Fixes:**

1. **Reduce Thread Count**
```python
# Limit concurrent analyses
if self.active_threads > 3:
    return  # Skip this response
```

2. **Increase Burp Memory**
```bash
# Start Burp with more RAM
java -jar -Xmx4g burpsuite.jar
```

3. **Disable During Scanning**
```
Turn off extension when using:
- Burp Scanner
- Burp Intruder (high-speed attacks)
- Passive scanning
```

---

## 📊 Performance Benchmarks

### Typical Analysis Times

```
Small JSON (1 KB):     2-3 seconds
Medium JSON (5 KB):    3-5 seconds
Large JSON (10 KB):    5-8 seconds

Using gpt-4o-mini:     Faster
Using gpt-4o:          Slower but better quality
```

### Cost Estimates

```
Assessment Size         Requests    Cost (gpt-4o-mini)
Small (50 endpoints)    50          $0.20
Medium (500 endpoints)  500         $2.00
Large (5000 endpoints)  5000        $20.00
```

---

## 🎯 Final Checklist

Before starting your assessment:

```
✅ Jython installed and configured
✅ Extension loaded without errors
✅ API key entered and saved
✅ Filters configured appropriately
✅ Scope defined in Burp
✅ Tested on sample endpoint
✅ Budget allocated for API costs
✅ Ready to verify findings manually
```

**You're ready to hunt! 🎯**
