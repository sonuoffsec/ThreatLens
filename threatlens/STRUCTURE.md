# Repository Structure

```
threatlens/
│
├── 📄 README.md                    # Main documentation and quick start
├── 📄 LICENSE                      # MIT License
├── 📄 CHANGELOG.md                 # Version history and updates
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 CODE_OF_CONDUCT.md           # Community standards
├── 📄 SECURITY.md                  # Security policy and reporting
├── 📄 .gitignore                   # Git ignore rules
│
├── 🐍 ai_recon_assistant.py        # Main extension (basic version)
├── 🐍 ai_recon_assistant_pro.py    # Enhanced extension (pro version)
│
├── 📁 assets/                      # Images and branding
│   └── logo.png                   # ThreatLens logo
│
├── 📁 docs/                        # Documentation
│   ├── USAGE_GUIDE.md             # Real-world usage examples
│   ├── EXAMPLES_AND_TROUBLESHOOTING.md  # Sample outputs and fixes
│   └── PROJECT_OVERVIEW.md        # Technical details and CV-ready info
│
├── 📁 setup/                       # Installation scripts
│   ├── setup.sh                   # Linux/macOS setup
│   └── setup.bat                  # Windows setup
│
└── 📁 .github/                     # GitHub configuration
    ├── pull_request_template.md  # PR template
    └── ISSUE_TEMPLATE/            # Issue templates
        ├── bug_report.md          # Bug report template
        └── feature_request.md     # Feature request template
```

## File Descriptions

### Root Level Files

**README.md**
- Main project documentation
- Quick start guide
- Installation instructions
- Usage examples
- Links to detailed docs

**LICENSE**
- MIT License
- Usage disclaimer
- Legal terms

**CHANGELOG.md**
- Version history
- Release notes
- Planned features

**CONTRIBUTING.md**
- How to contribute
- Development guidelines
- Code style standards
- Pull request process

**CODE_OF_CONDUCT.md**
- Community standards
- Expected behavior
- Reporting procedures

**SECURITY.md**
- Security policy
- Vulnerability reporting
- Data privacy info
- Best practices

**.gitignore**
- Excludes API keys
- Ignores build artifacts
- Prevents sensitive data commits

### Extension Files

**ai_recon_assistant.py**
- Basic version (12KB)
- Core features
- Real-time analysis
- Smart filtering
- Good for learning

**ai_recon_assistant_pro.py**
- Enhanced version (15KB)
- All basic features plus:
  - Scope filtering
  - Model selection
  - JSON export
  - Better statistics
  - Enhanced UI

### Documentation (docs/)

**USAGE_GUIDE.md**
- Real penetration testing scenarios
- Step-by-step workflows
- Example outputs
- Pro tips and techniques
- Cost management strategies

**EXAMPLES_AND_TROUBLESHOOTING.md**
- Sample AI analysis outputs
- Common issues and fixes
- Error message explanations
- Performance benchmarks
- FAQ section

**PROJECT_OVERVIEW.md**
- Technical architecture
- Innovation highlights
- CV-ready descriptions
- Skills demonstrated
- Interview talking points

### Setup Scripts (setup/)

**setup.sh**
- Automated setup for Linux/macOS
- Downloads Jython
- Verifies prerequisites
- Provides configuration steps

**setup.bat**
- Automated setup for Windows
- Downloads Jython
- Verifies prerequisites
- Provides configuration steps

### GitHub Configuration (.github/)

**pull_request_template.md**
- Standardized PR format
- Testing checklist
- Documentation requirements

**ISSUE_TEMPLATE/**
- **bug_report.md**: Structured bug reporting
- **feature_request.md**: Feature proposal template

## File Sizes

```
ai_recon_assistant.py             12 KB
ai_recon_assistant_pro.py         15 KB
README.md                         9 KB
USAGE_GUIDE.md                    11 KB
EXAMPLES_AND_TROUBLESHOOTING.md   13 KB
PROJECT_OVERVIEW.md               12 KB
setup.sh                          4 KB
setup.bat                         3 KB
```

**Total Project Size**: ~80 KB (excluding Jython JAR)

## Quick Access

- **Want to install?** → Start with `README.md`
- **Need help using?** → Check `docs/USAGE_GUIDE.md`
- **Found a bug?** → Use `.github/ISSUE_TEMPLATE/bug_report.md`
- **Want to contribute?** → Read `CONTRIBUTING.md`
- **Security concern?** → See `SECURITY.md`
- **Check updates?** → Review `CHANGELOG.md`

## Development Workflow

```
1. Clone repository
2. Run setup script (setup/setup.sh or setup.bat)
3. Load extension in Burp
4. Configure API key
5. Start testing!
```

## Contribution Workflow

```
1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Update documentation
6. Submit pull request (using PR template)
```

---

**This structure is designed for professional open-source projects and GitHub best practices.**
