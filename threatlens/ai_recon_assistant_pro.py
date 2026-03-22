# ThreatLens Pro - Burp Suite Extension
# Enhanced AI-Powered Security Analysis
# Includes: Better prompts, payload generation, finding categorization, export

from burp import IBurpExtender, IHttpListener, ITab
from javax.swing import JPanel, JTextArea, JScrollPane, JSplitPane, JLabel, JCheckBox, JTextField, JButton, JComboBox, JTable
from javax.swing.table import DefaultTableModel
from java.awt import BorderLayout, GridLayout, Color, Font
from java.awt import Dimension
import json
import threading
import time
import re

try:
    import urllib2
    import urllib
except ImportError:
    import urllib.request as urllib2
    import urllib.parse as urllib

class BurpExtender(IBurpExtender, IHttpListener, ITab):
    
    def registerExtenderCallbacks(self, callbacks):
        """Initialize the extension"""
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        
        callbacks.setExtensionName("ThreatLens Pro")
        
        # Configuration
        self.api_key = ""
        self.enabled = True
        self.analyze_count = 0
        self.findings = []
        
        # Enhanced filtering
        self.filter_by_type = True
        self.filter_by_status = True
        self.filter_in_scope_only = False  # New: Only analyze in-scope targets
        self.min_response_size = 100
        self.max_response_size = 10000
        
        # Model selection
        self.model = "gpt-4o-mini"  # Default
        
        # Interesting content types
        self.interesting_types = [
            'application/json',
            'application/xml',
            'text/xml',
            'application/javascript',
            'text/javascript'
        ]
        
        # Severity tracking
        self.high_findings = []
        self.medium_findings = []
        self.low_findings = []
        
        # Create UI
        self.create_ui()
        
        # Register listeners
        callbacks.registerHttpListener(self)
        callbacks.addSuiteTab(self)
        
        self.log("🚀 ThreatLens Pro loaded!")
        self.log("⚙️  Enhanced features: Scope filtering, payload generation, export")
        
    def create_ui(self):
        """Create enhanced UI"""
        self.panel = JPanel(BorderLayout())
        
        # Configuration panel
        config_panel = JPanel(GridLayout(9, 2, 5, 5))
        
        # API Key
        config_panel.add(JLabel("OpenAI API Key:"))
        self.api_key_field = JTextField(30)
        config_panel.add(self.api_key_field)
        
        # Model selection
        config_panel.add(JLabel("Model:"))
        models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
        self.model_combo = JComboBox(models)
        config_panel.add(self.model_combo)
        
        # Enabled
        config_panel.add(JLabel("Analysis Enabled:"))
        self.enabled_checkbox = JCheckBox("", True)
        config_panel.add(self.enabled_checkbox)
        
        # Content type filter
        config_panel.add(JLabel("Filter by Content-Type:"))
        self.filter_type_checkbox = JCheckBox("Only JSON/API", True)
        config_panel.add(self.filter_type_checkbox)
        
        # Status filter
        config_panel.add(JLabel("Filter by Status:"))
        self.filter_status_checkbox = JCheckBox("Only 2xx", True)
        config_panel.add(self.filter_status_checkbox)
        
        # Scope filter (NEW)
        config_panel.add(JLabel("Scope Filter:"))
        self.scope_checkbox = JCheckBox("In-scope only", False)
        config_panel.add(self.scope_checkbox)
        
        # Stats
        config_panel.add(JLabel("Analyzed:"))
        self.stats_label = JLabel("0 (H:0 M:0 L:0)")
        config_panel.add(self.stats_label)
        
        # Export button
        config_panel.add(JLabel("Export Findings:"))
        export_button = JButton("Export to JSON", actionPerformed=self.export_findings)
        config_panel.add(export_button)
        
        # Save button
        config_panel.add(JLabel(""))
        save_button = JButton("Save Configuration", actionPerformed=self.save_config)
        config_panel.add(save_button)
        
        # Output area with color coding
        self.output_area = JTextArea()
        self.output_area.setEditable(False)
        self.output_area.setFont(Font("Monospaced", Font.PLAIN, 12))
        self.output_area.setBackground(Color(30, 30, 30))
        self.output_area.setForeground(Color(200, 200, 200))
        scroll_pane = JScrollPane(self.output_area)
        
        # Split pane
        split_pane = JSplitPane(JSplitPane.VERTICAL_SPLIT, config_panel, scroll_pane)
        split_pane.setDividerLocation(280)
        
        self.panel.add(split_pane)
        
    def save_config(self, event):
        """Save configuration"""
        self.api_key = self.api_key_field.getText().strip()
        self.enabled = self.enabled_checkbox.isSelected()
        self.filter_by_type = self.filter_type_checkbox.isSelected()
        self.filter_by_status = self.filter_status_checkbox.isSelected()
        self.filter_in_scope_only = self.scope_checkbox.isSelected()
        self.model = str(self.model_combo.getSelectedItem())
        
        if self.api_key:
            self.log("✅ Configuration saved! Model: " + self.model)
        else:
            self.log("⚠️  No API key set")
    
    def export_findings(self, event):
        """Export findings to JSON"""
        export_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_analyzed": self.analyze_count,
            "findings": {
                "high": self.high_findings,
                "medium": self.medium_findings,
                "low": self.low_findings
            }
        }
        
        filename = "threatlens_findings_" + time.strftime("%Y%m%d_%H%M%S") + ".json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            self.log("✅ Exported findings to: " + filename)
        except Exception as e:
            self.log("❌ Export failed: " + str(e))
    
    def getTabCaption(self):
        return "ThreatLens Pro"
    
    def getUiComponent(self):
        return self.panel
    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        """Process HTTP messages"""
        if messageIsRequest:
            return
        
        if not self.enabled_checkbox.isSelected():
            return
        
        if not self.api_key_field.getText().strip():
            return
        
        response = messageInfo.getResponse()
        if response is None:
            return
        
        # Check scope if enabled
        if self.scope_checkbox.isSelected():
            request = messageInfo.getRequest()
            request_info = self.helpers.analyzeRequest(request)
            url = request_info.getUrl()
            if not self.callbacks.isInScope(url):
                return  # Skip out-of-scope targets
        
        # Analyze in background
        thread = threading.Thread(target=self.analyze_response, args=(messageInfo, response))
        thread.daemon = True
        thread.start()
    
    def analyze_response(self, messageInfo, response):
        """Enhanced analysis with categorization"""
        try:
            request = messageInfo.getRequest()
            request_info = self.helpers.analyzeRequest(request)
            url = str(request_info.getUrl())
            method = str(request_info.getMethod())
            
            response_info = self.helpers.analyzeResponse(response)
            status_code = response_info.getStatusCode()
            headers = response_info.getHeaders()
            
            if not self.should_analyze(status_code, headers):
                return
            
            body_offset = response_info.getBodyOffset()
            body_bytes = response[body_offset:]
            body_str = self.helpers.bytesToString(body_bytes)
            
            if len(body_str) < self.min_response_size:
                return
            
            cleaned_data = self.clean_response(body_str, headers)
            context = self.build_enhanced_context(url, method, status_code, headers, cleaned_data)
            
            # Call AI with enhanced prompt
            ai_response = self.call_openai_enhanced(context)
            
            # Parse and categorize findings
            self.categorize_and_display(url, ai_response)
            
            self.analyze_count += 1
            self.update_stats()
            
        except Exception as e:
            self.log("Error: " + str(e))
    
    def should_analyze(self, status_code, headers):
        """Enhanced filtering logic"""
        if self.filter_by_status and not (200 <= status_code < 300):
            return False
        
        if self.filter_by_type:
            content_type = self.get_header_value(headers, "Content-Type")
            if content_type:
                is_interesting = any(ct in content_type.lower() for ct in self.interesting_types)
                if not is_interesting:
                    return False
        
        return True
    
    def get_header_value(self, headers, header_name):
        """Extract header value"""
        header_name_lower = header_name.lower()
        for header in headers:
            if ':' in header:
                name, value = header.split(':', 1)
                if name.strip().lower() == header_name_lower:
                    return value.strip()
        return None
    
    def clean_response(self, body, headers):
        """Clean response"""
        if len(body) > self.max_response_size:
            body = body[:self.max_response_size] + "\n[truncated]"
        
        try:
            parsed = json.loads(body)
            return json.dumps(parsed, indent=2)
        except:
            return body
    
    def build_enhanced_context(self, url, method, status_code, headers, body):
        """Build enhanced context with more security details"""
        security_headers = [
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'X-XSS-Protection',
            'Access-Control-Allow-Origin',
            'Set-Cookie',
            'Server',
            'X-Powered-By'
        ]
        
        header_analysis = {}
        for name in security_headers:
            value = self.get_header_value(headers, name)
            if value:
                header_analysis[name] = value
            else:
                header_analysis[name] = "MISSING"
        
        context = {
            'method': method,
            'url': url,
            'status': status_code,
            'security_headers': header_analysis,
            'body': body
        }
        
        return json.dumps(context, indent=2)
    
    def call_openai_enhanced(self, context):
        """Enhanced AI call with better prompting"""
        
        prompt = """You are a senior penetration tester. Analyze this HTTP response.

CRITICAL RULES:
1. Only report EXPLOITABLE findings (not theoretical)
2. Provide SPECIFIC attack vectors (exact payloads/techniques)
3. Focus on HIGH and MEDIUM severity only
4. Be concise - 2-3 sentences per finding max

ANALYZE FOR:

🔴 HIGH SEVERITY (Report these immediately):
- IDOR: Predictable IDs that allow unauthorized access
- Auth Bypass: Missing/weak authorization checks
- Injection: SQL/Command/XXE injection points
- Sensitive Data: Exposed passwords, tokens, API keys, internal IPs

🟡 MEDIUM SEVERITY (Worth investigating):
- Information Disclosure: Stack traces, debug info, version numbers
- Missing Security Headers: CSP, X-Frame-Options, HSTS
- Interesting Endpoints: Hidden APIs, admin panels, internal routes
- Weak Configurations: Predictable patterns, loose CORS

ATTACK VECTORS:
For each finding, provide:
- Specific payload to test
- Expected vulnerable behavior
- Remediation hint

FORMAT OUTPUT AS:
[HIGH] Finding title
Payload: <exact test>
Impact: <what attacker gains>

[MEDIUM] Finding title
Test: <how to verify>
---

Response to analyze:
{}

Remember: Focus on ACTIONABLE, TESTABLE vulnerabilities. No generic advice.
""".format(context)
        
        api_url = "https://api.openai.com/v1/chat/completions"
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert penetration tester. Provide only exploitable findings with specific attack payloads. No generic security advice."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 800
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key_field.getText().strip()
        }
        
        req = urllib2.Request(api_url, json.dumps(data).encode('utf-8'), headers)
        
        try:
            response = urllib2.urlopen(req, timeout=30)
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
        except Exception as e:
            return "API Error: " + str(e)
    
    def categorize_and_display(self, url, ai_response):
        """Categorize findings by severity and display"""
        timestamp = time.strftime("%H:%M:%S")
        
        # Parse severity
        high_count = ai_response.count("[HIGH]")
        medium_count = ai_response.count("[MEDIUM]")
        low_count = ai_response.count("[LOW]")
        
        # Store findings
        if high_count > 0:
            self.high_findings.append({"url": url, "timestamp": timestamp, "details": ai_response})
        if medium_count > 0:
            self.medium_findings.append({"url": url, "timestamp": timestamp, "details": ai_response})
        if low_count > 0:
            self.low_findings.append({"url": url, "timestamp": timestamp, "details": ai_response})
        
        # Color code output
        severity_indicator = ""
        if high_count > 0:
            severity_indicator = "🔴 " + str(high_count) + " HIGH"
        elif medium_count > 0:
            severity_indicator = "🟡 " + str(medium_count) + " MEDIUM"
        else:
            severity_indicator = "🟢 LOW/INFO"
        
        output = "\n" + "="*80 + "\n"
        output += "[{}] {} - {}\n".format(timestamp, severity_indicator, url)
        output += "="*80 + "\n"
        output += ai_response + "\n"
        
        self.output_area.append(output)
        self.output_area.setCaretPosition(self.output_area.getDocument().getLength())
    
    def update_stats(self):
        """Update statistics display"""
        stats = "{} (H:{} M:{} L:{})".format(
            self.analyze_count,
            len(self.high_findings),
            len(self.medium_findings),
            len(self.low_findings)
        )
        self.stats_label.setText(stats)
    
    def log(self, message):
        """Log message"""
        self.output_area.append("[*] " + message + "\n")
