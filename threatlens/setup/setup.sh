#!/bin/bash

# ThreatLens - Quick Setup Script
# Run this to automatically download dependencies and configure Burp

echo "================================================"
echo "  ThreatLens - Quick Setup"
echo "  See threats before they see you"
echo "================================================"
echo ""

# Check if running on supported OS
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ OS: $(uname -s)"
else
    echo "⚠️  Warning: This script is optimized for Linux/macOS"
fi

echo ""
echo "📋 Prerequisites Check:"
echo ""

# Check for Burp Suite
if command -v burpsuite &> /dev/null; then
    echo "✅ Burp Suite: Found"
elif [ -d "/Applications/Burp Suite Professional.app" ] || [ -d "/Applications/Burp Suite Community Edition.app" ]; then
    echo "✅ Burp Suite: Found (macOS)"
else
    echo "⚠️  Burp Suite: Not found in PATH"
    echo "   Please ensure Burp Suite is installed"
fi

# Check for Java
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
    echo "✅ Java: $JAVA_VERSION"
else
    echo "❌ Java: Not found"
    echo "   Install Java: sudo apt install default-jdk"
    exit 1
fi

# Check for wget or curl
if command -v wget &> /dev/null; then
    DOWNLOADER="wget"
    echo "✅ Downloader: wget"
elif command -v curl &> /dev/null; then
    DOWNLOADER="curl"
    echo "✅ Downloader: curl"
else
    echo "❌ No download tool found (need wget or curl)"
    exit 1
fi

echo ""
echo "================================================"
echo "  Step 1: Download Jython Standalone"
echo "================================================"
echo ""

JYTHON_VERSION="2.7.3"
JYTHON_JAR="jython-standalone-${JYTHON_VERSION}.jar"
JYTHON_URL="https://repo1.maven.org/maven2/org/python/jython-standalone/${JYTHON_VERSION}/${JYTHON_JAR}"

if [ -f "$JYTHON_JAR" ]; then
    echo "✅ Jython already downloaded: $JYTHON_JAR"
else
    echo "📥 Downloading Jython $JYTHON_VERSION..."
    
    if [ "$DOWNLOADER" = "wget" ]; then
        wget -q --show-progress "$JYTHON_URL" -O "$JYTHON_JAR"
    else
        curl -L -# "$JYTHON_URL" -o "$JYTHON_JAR"
    fi
    
    if [ -f "$JYTHON_JAR" ]; then
        echo "✅ Downloaded: $JYTHON_JAR"
    else
        echo "❌ Download failed"
        exit 1
    fi
fi

JYTHON_PATH="$(pwd)/$JYTHON_JAR"
echo ""
echo "📂 Jython JAR location: $JYTHON_PATH"

echo ""
echo "================================================"
echo "  Step 2: Verify Extension File"
echo "================================================"
echo ""

if [ -f "ai_recon_assistant.py" ]; then
    echo "✅ Extension file found: ai_recon_assistant.py"
    EXTENSION_PATH="$(pwd)/ai_recon_assistant.py"
else
    echo "❌ Extension file not found: ai_recon_assistant.py"
    echo "   Please ensure the file is in the current directory"
    exit 1
fi

echo ""
echo "================================================"
echo "  Step 3: Configuration Instructions"
echo "================================================"
echo ""

echo "Next steps to complete installation:"
echo ""
echo "1. Open Burp Suite"
echo ""
echo "2. Configure Jython:"
echo "   → Extensions → Extension Settings"
echo "   → Location of Jython standalone JAR file:"
echo "   → Paste this path: $JYTHON_PATH"
echo ""
echo "3. Load the extension:"
echo "   → Extensions → Installed → Add"
echo "   → Extension type: Python"
echo "   → Extension file: $EXTENSION_PATH"
echo "   → Click Next"
echo ""
echo "4. Configure API key:"
echo "   → Click 'ThreatLens' tab"
echo "   → Enter your OpenAI API key"
echo "   → Click 'Save Configuration'"
echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "📝 Quick reference:"
echo "   Jython JAR: $JYTHON_PATH"
echo "   Extension: $EXTENSION_PATH"
echo ""
echo "📚 See README.md for detailed usage instructions"
echo ""
echo "🎯 Happy hunting!"
echo ""
