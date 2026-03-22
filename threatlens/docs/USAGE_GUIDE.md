# ThreatLens - Practical Usage Guide

## 🎯 Real-World Penetration Testing Scenarios

This guide shows you how to use ThreatLens effectively during actual security assessments.

---

## 📋 Pre-Assessment Setup

### 1. Configure Your Burp Scope

Before enabling the extension:

```
1. Define target scope in Burp
   → Target → Scope → Add
   → Add: *.target-domain.com
   
2. Enable "In-scope only" in ThreatLens tab
   → Prevents analyzing out-of-scope requests
   → Saves API costs
```

### 2. Recommended Settings by Assessment Type

**Quick Scan (1-2 hours)**
```
✅ Filter by Content-Type: ON
✅ Filter by Status: ON
✅ In-scope only: ON
Model: gpt-4o-mini (faster, cheaper)
```

**Deep Assessment (Full day)**
```
✅ Filter by Content-Type: ON
✅ Filter by Status: OFF (catch error messages)
✅ In-scope only: ON
Model: gpt-4o (better analysis)
```

**Bug Bounty / Continuous Testing**
```
✅ Filter by Content-Type: ON
✅ Filter by Status: ON
✅ In-scope only: OFF (explore widely)
Model: gpt-4o-mini
```

---

## 🔍 Scenario 1: API Endpoint Discovery

### Target: E-commerce API

**Workflow:**
1. Browse the application normally
2. Watch ThreatLens tab for interesting findings
3. Test suggested endpoints

**Example Output:**

```
[HIGH] IDOR Vulnerability Detected
URL: https://api.shop.com/orders/12345

Finding: Order ID is sequential and not tied to user session
Payload: GET /orders/12346, /orders/12347
Impact: Access to other users' order details (PII, addresses, payment info)

[MEDIUM] Hidden Admin Endpoint
URL: https://api.shop.com/products

Finding: Response contains reference to /api/admin/products
Test: Try accessing /api/admin/products directly
      Add header: X-Admin: true
Impact: Potential unauthorized admin access

[MEDIUM] Rate Limiting Missing
Finding: No rate limit headers detected
Test: Send 1000 requests to /orders/
Impact: User enumeration, data scraping possible
```

**What to do:**
1. Open Burp Repeater
2. Test `/orders/12346` → If accessible: HIGH severity IDOR confirmed
3. Test `/api/admin/products` → Document for manual testing
4. Run Intruder to test rate limits

---

## 🔍 Scenario 2: Authentication Testing

### Target: Login/Registration Flow

**Workflow:**
1. Create test account
2. Login and capture responses
3. Review AI findings for auth issues

**Example Output:**

```
[HIGH] JWT Token Contains Sensitive Data
URL: https://app.example.com/auth/login

Finding: JWT payload contains:
{
  "user_id": 123,
  "role": "user",
  "is_admin": false,
  "internal_id": "EMP_12345"
}

Payload: Decode JWT, change "role": "admin"
Test: Modify token with jwt.io, replay request
Impact: Privilege escalation to admin

[MEDIUM] Password Reset Token Predictable
URL: https://app.example.com/auth/reset

Finding: Reset token format: reset_<user_id>_<timestamp>
Test: Generate token for admin user
      POST /auth/reset with crafted token
Impact: Account takeover via predictable tokens
```

**What to do:**
1. Copy JWT to jwt.io
2. Modify claims: `"role": "admin"`, `"is_admin": true`
3. Re-encode and test with modified token
4. Test password reset with predicted tokens

---

## 🔍 Scenario 3: Data Exposure

### Target: User Profile APIs

**Workflow:**
1. View your own profile
2. Check what data is returned
3. Test for over-fetching

**Example Output:**

```
[HIGH] Excessive Data Exposure
URL: https://api.social.com/users/me

Finding: Response contains 50+ fields including:
- password_hash (MD5 - crackable)
- email_verified_token
- internal_notes
- ip_addresses (login history)
- payment_methods (last 4 digits)

Payload: Access other user profiles: /users/<id>
Test: Check if same data exposed for other users
Impact: Mass PII harvesting, password cracking

[MEDIUM] GraphQL Introspection Enabled
URL: https://api.social.com/graphql

Finding: Introspection query successful
Test: Query { __schema { types { name fields { name } } } }
Impact: Discover all available queries, hidden fields
```

**What to do:**
1. Save response as reference
2. Test `/users/1`, `/users/2` for IDOR
3. If GraphQL: Run introspection to map entire API
4. Check if password_hash is actually exploitable

---

## 🔍 Scenario 4: Parameter Manipulation

### Target: Search/Filter Endpoints

**Workflow:**
1. Use search functionality
2. Observe parameter handling
3. Test injection points

**Example Output:**

```
[HIGH] SQL Injection Possible
URL: https://shop.com/api/search?q=laptop&sort=price

Finding: Error message when testing sort parameter:
"SQL error: ORDER BY 'price' DESC"

Payload: ?sort=price' OR '1'='1
         ?sort=price'; DROP TABLE users--
Test: Boolean-based blind SQLi
      Time-based: ?sort=price' AND SLEEP(5)--
Impact: Database compromise

[MEDIUM] NoSQL Injection Vector
URL: https://app.com/api/users?filter={"role":"user"}

Finding: MongoDB-style filter parameter
Payload: {"role": {"$ne": "user"}}
         {"$where": "this.role == 'admin'"}
Test: Bypass authentication, access admin users
Impact: Unauthorized access to admin accounts
```

**What to do:**
1. Test basic SQLi: `' OR '1'='1`
2. If vulnerable: Use SQLMap for deeper exploitation
3. For NoSQL: Test operator injection systematically
4. Document exact vulnerable parameters

---

## 🔍 Scenario 5: File Upload Testing

### Target: Profile Picture Upload

**Workflow:**
1. Upload test image
2. Check response for paths, validation
3. Test for insecure handling

**Example Output:**

```
[HIGH] Unrestricted File Upload
URL: https://app.com/api/upload

Finding: Server accepts any file type
Response: {"path": "/uploads/shell.php"}
No content-type validation detected

Payload: Upload PHP web shell
         Test: curl https://app.com/uploads/shell.php?cmd=whoami
Impact: Remote code execution (RCE)

[MEDIUM] Path Traversal in Filename
Finding: Filename parameter not sanitized
Payload: Upload with filename: ../../shell.php
Test: Check if file written outside upload directory
Impact: Arbitrary file write
```

**What to do:**
1. **CRITICAL**: Only test on authorized targets
2. Upload harmless test file (text file with unique string)
3. Try to access uploaded file
4. If accessible: Test with actual payload ONLY if authorized
5. Report immediately if RCE possible

---

## 🛠️ Advanced Techniques

### Combining AI with Manual Testing

**Workflow:**
```
1. Browse application → AI identifies interesting endpoint
2. Send to Repeater → Manual parameter testing
3. Send to Intruder → Automated payload fuzzing
4. AI analyzes error responses → Finds new vulnerabilities
5. Rinse and repeat
```

### Using AI for Payload Generation

When AI suggests a finding, ask it for specific payloads:

**Example conversation:**
```
You: The AI found a potential IDOR in /api/orders/{id}. 
     What payloads should I test?

AI Response might suggest:
- Sequential IDs: 1, 2, 3, ..., 999999
- UUID enumeration (if UUIDs)
- Negative IDs: -1, -999
- Special chars: ../orders, orders/../../admin
```

### Exporting and Reporting

At end of assessment:

```
1. Click "Export to JSON" in ThreatLens tab
2. Review all [HIGH] findings first
3. Verify each finding manually
4. Add to final report with:
   - Original AI finding
   - Manual verification steps
   - Proof of concept
   - Remediation advice
```

---

## 📊 Interpreting Results

### Severity Levels

**🔴 HIGH - Test Immediately**
- IDOR, Auth bypass, Injection, RCE, Sensitive data exposure
- These are often exploitable with minimal effort
- Verify within 15 minutes of finding

**🟡 MEDIUM - Investigate**
- Missing security headers, info disclosure, weak configs
- May require chaining with other issues
- Document for comprehensive testing

**🟢 LOW/INFO - Context Dependent**
- Informational findings, version info, debug data
- Useful for reconnaissance
- May help with social engineering

### False Positives

AI can hallucinate. Always verify:

```
❌ AI says: "SQL injection in parameter X"
✅ You verify: Actually just URL-encoded characters

❌ AI says: "Admin panel found at /admin"
✅ You test: 404 Not Found

❌ AI says: "Weak password policy"
✅ You check: Based on error message, not actual policy
```

**Rule**: Don't report a finding until you've manually confirmed it.

---

## 💰 Cost Management

### Typical API Costs

**Using gpt-4o-mini** (recommended for pen-testing):

```
Small assessment (50 endpoints):   ~$0.20
Medium assessment (500 endpoints):  ~$2.00
Large assessment (5000 endpoints):  ~$20.00
```

### Optimization Tips

1. **Enable all filters** during initial browsing
2. **Disable filters** only when targeting specific areas
3. **Use scope filtering** to exclude CDN, analytics
4. **Review findings in batches** - don't analyze every single request
5. **Turn off during passive reconnaissance** - only enable during active testing

---

## 🎓 Pro Tips

### 1. Baseline First
```
1. Browse application WITHOUT AI enabled
2. Map out key endpoints in Burp
3. THEN enable AI for targeted analysis
4. This saves costs and reduces noise
```

### 2. Focus on Change
```
When application updates:
1. Enable AI
2. Test new/modified endpoints
3. Compare findings with baseline
4. Identify new vulnerabilities
```

### 3. Chain Findings
```
AI finding #1: Hidden endpoint /api/internal
AI finding #2: Missing authentication on /api/users
You combine: Access /api/internal/users without auth
Result: Escalated finding
```

### 4. Use for Learning
```
AI explains WHY something is vulnerable
You learn attack patterns
Apply to manual testing
Become better pen-tester
```

---

## 📝 Sample Report Template

When documenting AI-discovered findings:

```markdown
### Finding: IDOR in Order Management

**Severity**: High
**Endpoint**: GET /api/orders/{order_id}

**Discovery Method**: 
ThreatLens identified predictable order IDs during 
normal application browsing.

**Vulnerability Description**:
The application exposes order details via predictable sequential 
IDs without proper authorization checks.

**Steps to Reproduce**:
1. Authenticate as user A (order ID: 12345)
2. Request: GET /api/orders/12346
3. Observe: User B's order details returned
4. Impact: PII exposure (name, address, phone, email)

**Proof of Concept**:
[Include screenshot of successful IDOR]

**AI Original Finding**:
"[HIGH] IDOR Vulnerability - Sequential order IDs allow 
unauthorized access. Test: /orders/<id+1>"

**Manual Verification**:
Confirmed exploitable. Tested 100 consecutive IDs, 95% success rate.

**Remediation**:
Implement proper authorization checks. Use UUIDs instead of 
sequential IDs.
```

---

## 🚨 Responsible Disclosure

When you find real vulnerabilities:

1. **Document thoroughly** with screenshots and steps
2. **Don't exploit** beyond proof-of-concept
3. **Report immediately** to security team or bug bounty platform
4. **Give reasonable time** for remediation (90 days standard)
5. **Don't publish** until fixed or deadline passed

---

## 🎯 Next Steps

Now that you know how to use it:

1. ✅ Test on a practice target (OWASP Juice Shop, DVWA)
2. ✅ Run on a small authorized assessment
3. ✅ Review accuracy of findings
4. ✅ Build your own prompt variations
5. ✅ Contribute improvements back to community

**Happy hunting! 🎯**
