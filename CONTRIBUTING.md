# Contributing to ThreatLens

Thank you for your interest in contributing to ThreatLens! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior vs. actual behavior
- Burp Suite version
- Python/Jython version
- Error messages or logs

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Any implementation ideas

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and concise

### Testing

Before submitting:
- [ ] Test extension loads without errors
- [ ] Test on sample JSON/API responses
- [ ] Verify all filters work correctly
- [ ] Check error handling
- [ ] Test on both Burp Pro and Community

### Documentation

When adding features:
- Update README.md if needed
- Add usage examples
- Document any new configuration options
- Update troubleshooting guide if relevant

## 🔒 Security

### Responsible Disclosure

If you discover a security vulnerability:
1. **DO NOT** create a public issue
2. Email the maintainers directly
3. Provide detailed information
4. Allow time for a fix before disclosure

### Testing Ethics

- Only test on authorized systems
- Follow responsible disclosure practices
- Don't include real credentials or sensitive data in examples
- Respect API rate limits and terms of service

## 🎯 Priority Areas

We're especially interested in contributions for:

### High Priority
- [ ] Reduce false positives
- [ ] Support for additional AI models (Claude, Gemini)
- [ ] Better error handling
- [ ] Performance optimizations

### Medium Priority
- [ ] Export formats (CSV, PDF)
- [ ] Integration with Burp Scanner
- [ ] Custom security rules engine
- [ ] Historical findings database

### Nice to Have
- [ ] UI improvements
- [ ] Additional filters
- [ ] Payload generation
- [ ] Team collaboration features

## 📝 Pull Request Process

1. Update documentation for any new features
2. Add your changes to CHANGELOG.md (if exists)
3. Ensure code follows style guidelines
4. Test thoroughly on multiple scenarios
5. Provide clear description in PR

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Credited in release notes
- Mentioned in project documentation

## ❓ Questions?

- Create a GitHub issue for technical questions
- Check existing issues and documentation first
- Be specific and provide context

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Malicious use of the tool

## 🙏 Thank You!

Every contribution helps make ThreatLens better. Whether it's a bug report, feature suggestion, or code contribution - we appreciate your help!

---

**Happy Contributing! 🚀**
