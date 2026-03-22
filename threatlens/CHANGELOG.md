# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-03-22

### Added
- Initial release of ThreatLens
- AI-powered security analysis using OpenAI GPT models
- Real-time HTTP response analysis with "see threats before they see you" approach
- Smart filtering system (content-type, status code, response size)
- Custom Burp Suite UI tab with configuration panel
- Severity-based finding categorization (High/Medium/Low)
- Async/threaded processing to avoid blocking Burp
- JSON export functionality for findings
- Comprehensive documentation and setup guides
- Cross-platform setup scripts (Linux/macOS/Windows)
- Two versions: Basic and Pro (with enhanced features)

### Features - Basic Version
- HTTP response interception and analysis
- OpenAI API integration (GPT-4o-mini/GPT-4o)
- Content-Type filtering
- Status code filtering
- Response size limits
- Real-time output display
- Configuration saving

### Features - Pro Version
- All basic version features
- Scope-based filtering (analyze only in-scope targets)
- Model selection (choose between GPT models)
- Enhanced statistics tracking (High/Medium/Low counts)
- JSON export of findings
- Dark theme UI
- Better error handling
- Improved performance

### Documentation
- Complete installation guide
- Real-world usage scenarios
- Example outputs and troubleshooting
- CV-ready project descriptions
- Contributing guidelines

## [Unreleased]

### Planned Features
- Integration with Burp Scanner
- Automatic payload generation
- Custom security rules engine
- Support for Claude API
- Support for Gemini API
- Historical findings database
- Enhanced false positive detection
- CSV/PDF export formats
- Team collaboration features

---

## Version History

- **1.0.0** - Initial public release with core features
- **0.9.0** - Beta testing phase
- **0.5.0** - Alpha development with basic analysis
- **0.1.0** - Proof of concept

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to this changelog.
