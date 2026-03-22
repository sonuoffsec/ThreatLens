# Security Policy

## 🔒 Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🐛 Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in ThreatLens, please report it privately:

### For Vulnerabilities in the Extension

1. **Email**: Send details to the project maintainers (contact via GitHub profile)
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)
3. **Response Time**: We aim to respond within 48 hours
4. **Disclosure**: We'll work with you on a responsible disclosure timeline

### For Security Issues in Dependencies

If the vulnerability is in a dependency (OpenAI API, Burp Suite, Jython):
- Report to the respective project
- Notify us so we can track the issue

## 🛡️ Security Considerations for Users

### API Key Security

**CRITICAL**: Your OpenAI API key is sensitive

- ✅ Never commit API keys to version control
- ✅ Use environment variables or secure key management
- ✅ Rotate keys regularly
- ✅ Monitor API usage for anomalies
- ❌ Don't share screenshots with API keys visible
- ❌ Don't paste API keys in issues or PRs

### Data Privacy

**What gets sent to OpenAI:**
- HTTP request URL
- Response headers (selected)
- Response body (truncated)

**What does NOT get sent:**
- Your Burp project files
- Other requests/responses
- Session tokens (unless in analyzed response)
- Credentials (unless in analyzed response)

**Recommendations:**
- Use a separate API key for security testing
- Be aware of sensitive data in responses
- Review prompts before sending sensitive assessments
- Consider using local LLM alternatives for highly sensitive work

### Target System Security

**Legal and Ethical Use Only:**
- ✅ Only test systems you have permission to test
- ✅ Follow rules of engagement
- ✅ Document authorization
- ❌ Never use on production systems without explicit authorization
- ❌ Never use for malicious purposes

### Extension Security

**We take security seriously:**
- Code is open source and reviewable
- No telemetry or data collection
- API keys stored in memory only (not persisted to disk)
- All network requests are to OpenAI API only

## 🔐 Security Features

### Current Security Controls

1. **Input Validation**
   - Response size limits (prevents large payload attacks)
   - Content-type filtering
   - URL validation

2. **API Security**
   - HTTPS only for API calls
   - Proper error handling
   - Rate limit awareness

3. **Code Security**
   - No eval() or exec() usage
   - No shell command execution on untrusted data
   - Proper exception handling

### Known Limitations

1. **False Positives**: AI may incorrectly identify vulnerabilities
2. **False Negatives**: AI may miss vulnerabilities
3. **Context Understanding**: AI lacks full application context
4. **Prompt Injection**: Malicious responses could attempt to manipulate AI

**Mitigation**: Always manually verify findings before reporting

## 🚨 Security Best Practices

### For Users

```python
# Good: API key from environment
api_key = os.getenv('OPENAI_API_KEY')

# Bad: API key hardcoded
api_key = "sk-proj-abc123..."  # DON'T DO THIS
```

### For Contributors

- Review all external dependencies
- Validate all user inputs
- Use parameterized queries (if adding database features)
- Follow principle of least privilege
- Document security assumptions
- Add security tests for new features

## 📋 Security Checklist for Deployments

Before using in production assessments:

- [ ] API key is properly secured
- [ ] Scope is correctly configured
- [ ] Target authorization is documented
- [ ] Filters are enabled (cost and privacy)
- [ ] You understand what data is sent to OpenAI
- [ ] You have a plan for handling sensitive findings
- [ ] You've reviewed the output for accuracy

## 🔄 Vulnerability Disclosure Timeline

Our commitment to responsible disclosure:

1. **Day 0**: Vulnerability reported
2. **Day 1-2**: Initial response and triage
3. **Day 3-7**: Investigation and reproduction
4. **Day 7-14**: Develop and test fix
5. **Day 14-21**: Release patched version
6. **Day 21-90**: Public disclosure (coordinated with reporter)

## 🏆 Hall of Fame

We recognize security researchers who help improve this project:

<!-- Contributors who report security issues will be listed here -->
- *Be the first to report a security issue!*

## 📧 Contact

For security concerns:
- Open a security advisory on GitHub (preferred)
- Contact maintainers via GitHub profile

For general questions:
- Use GitHub issues (non-security related)
- Join discussions

## 📜 Legal

This tool is provided "as is" without warranty. Users are solely responsible for:
- Obtaining proper authorization
- Complying with laws and regulations
- Any consequences of misuse

See [LICENSE](LICENSE) for full terms.

---

**Thank you for helping keep ThreatLens secure!**
