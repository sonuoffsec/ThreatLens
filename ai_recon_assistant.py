# ThreatLens - Burp Suite Extension
# AI-Powered Security Analysis Extension
# Description: See threats before they see you - AI-powered HTTP response analyzer

from burp import IBurpExtender, IHttpListener, ITab
from javax.swing import JPanel, JTextArea, JScrollPane, JSplitPane, JLabel, JCheckBox, JTextField, JButton
from java.awt import BorderLayout, GridLayout, Color, Font
from java.awt import Dimension
import json
import threading
import time

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
        
        # Set extension name
        callbacks.setExtensionName("ThreatLens")
        
        # Configuration
        self.api_key = ""  # Will be set via UI
        self.enabled = True
        self.analyze_count = 0
        self.findings = []
        
        # Filtering settings (to save API costs)
        self.filter_by_type = True  # Only analyze JSON/API responses
        self.filter_by_status = True  # Only 200-299 responses
        self.min_response_size = 100  # Skip tiny responses
        self.max_response_size = 10000  # Truncate large responses
        
        # Interesting content types for pen-testing
        self.interesting_types = [
            'application/json',
            'application/xml',
            'text/xml',
            'application/javascript'
        ]
        
        # Create UI
        self.create_ui()
        
        # Register HTTP listener
        callbacks.registerHttpListener(self)
        
        # Add custom tab
        callbacks.addSuiteTab(self)
        
        self.log("ThreatLens loaded successfully!")
        self.log("⚠️  Please set your OpenAI API key in the config panel")
        
    def create_ui(self):
        """Create the UI tab"""
        self.panel = JPanel(BorderLayout())
        
        # Top panel - Configuration
        config_panel = JPanel(GridLayout(6, 2, 5, 5))
        
        # API Key input
        config_panel.add(JLabel("OpenAI API Key:"))
        self.api_key_field = JTextField(30)
        config_panel.add(self.api_key_field)
        
        # Enable/Disable
        config_panel.add(JLabel("Analysis Enabled:"))
        self.enabled_checkbox = JCheckBox("", True)
        config_panel.add(self.enabled_checkbox)
        
        # Filter by content type
        config_panel.add(JLabel("Filter by Content-Type:"))
        self.filter_type_checkbox = JCheckBox("Only JSON/API responses", True)
        config_panel.add(self.filter_type_checkbox)
        
        # Filter by status
        config_panel.add(JLabel("Filter by Status:"))
        self.filter_status_checkbox = JCheckBox("Only 2xx responses", True)
        config_panel.add(self.filter_status_checkbox)
        
        # Stats
        config_panel.add(JLabel("Requests Analyzed:"))
        self.stats_label = JLabel("0")
        config_panel.add(self.stats_label)
        
        # Save button
        config_panel.add(JLabel(""))
        save_button = JButton("Save Configuration", actionPerformed=self.save_config)
        config_panel.add(save_button)
        
        # Output area
        self.output_area = JTextArea()
        self.output_area.setEditable(False)
        self.output_area.setFont(Font("Monospaced", Font.PLAIN, 12))
        scroll_pane = JScrollPane(self.output_area)
        
        # Split pane
        split_pane = JSplitPane(JSplitPane.VERTICAL_SPLIT, config_panel, scroll_pane)
        split_pane.setDividerLocation(200)
        
        self.panel.add(split_pane)
        
    def save_config(self, event):
        """Save configuration from UI"""
        self.api_key = self.api_key_field.getText().strip()
        self.enabled = self.enabled_checkbox.isSelected()
        self.filter_by_type = self.filter_type_checkbox.isSelected()
        self.filter_by_status = self.filter_status_checkbox.isSelected()
        
        if self.api_key:
            self.log("✅ Configuration saved! Extension is ready.")
        else:
            self.log("⚠️  Warning: No API key set. Analysis will not work.")
    
    def getTabCaption(self):
        """Return tab name"""
        return "ThreatLens"
    
    def getUiComponent(self):
        """Return UI component"""
        return self.panel
    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        """Process HTTP messages"""
        # Only process responses
        if messageIsRequest:
            return
        
        # Check if enabled
        if not self.enabled_checkbox.isSelected():
            return
        
        # Check if API key is set
        if not self.api_key_field.getText().strip():
            return
        
        # Get response
        response = messageInfo.getResponse()
        if response is None:
            return
        
        # Analyze in background thread to avoid blocking Burp
        thread = threading.Thread(target=self.analyze_response, args=(messageInfo, response))
        thread.daemon = True
        thread.start()
    
    def analyze_response(self, messageInfo, response):
        """Analyze HTTP response with AI"""
        try:
            # Get request info for context
            request = messageInfo.getRequest()
            request_info = self.helpers.analyzeRequest(request)
            url = str(request_info.getUrl())
            
            # Analyze response
            response_info = self.helpers.analyzeResponse(response)
            status_code = response_info.getStatusCode()
            headers = response_info.getHeaders()
            
            # Apply filters
            if not self.should_analyze(status_code, headers):
                return
            
            # Extract body
            body_offset = response_info.getBodyOffset()
            body_bytes = response[body_offset:]
            body_str = self.helpers.bytesToString(body_bytes)
            
            # Skip if too small or too large
            if len(body_str) < self.min_response_size:
                return
            
            # Clean and prepare data
            cleaned_data = self.clean_response(body_str, headers)
            
            # Build context
            context = self.build_context(url, status_code, headers, cleaned_data)
            
            # Call AI
            ai_response = self.call_openai(context)
            
            # Display results
            self.display_results(url, ai_response)
            
            # Update stats
            self.analyze_count += 1
            self.stats_label.setText(str(self.analyze_count))
            
        except Exception as e:
            self.log("Error analyzing response: " + str(e))
    
    def should_analyze(self, status_code, headers):
        """Determine if response should be analyzed"""
        # Check status code filter
        if self.filter_by_status and not (200 <= status_code < 300):
            return False
        
        # Check content type filter
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
        """Clean and extract relevant data from response"""
        # Truncate if too large
        if len(body) > self.max_response_size:
            body = body[:self.max_response_size] + "\n... [truncated]"
        
        # Try to parse as JSON for better formatting
        try:
            parsed = json.loads(body)
            return json.dumps(parsed, indent=2)
        except:
            # Not JSON, return as is (might be XML, HTML, etc.)
            return body
    
    def build_context(self, url, status_code, headers, body):
        """Build context for AI analysis"""
        # Extract important headers
        important_headers = {}
        header_names = ['Content-Type', 'Server', 'X-Powered-By', 'Set-Cookie', 
                       'Access-Control-Allow-Origin', 'X-Frame-Options', 'Content-Security-Policy']
        
        for name in header_names:
            value = self.get_header_value(headers, name)
            if value:
                important_headers[name] = value
        
        context = {
            'url': url,
            'status': status_code,
            'headers': important_headers,
            'body': body
        }
        
        return json.dumps(context, indent=2)
    
    def call_openai(self, context):
        """Call OpenAI API for analysis"""
        prompt = """You are a senior penetration tester analyzing HTTP responses during a security assessment.

Analyze this response and provide:

1. **VULNERABILITIES** - Specific security issues (IDOR, injection, auth bypass, etc.)
2. **SENSITIVE DATA** - Exposed credentials, tokens, internal paths, PII
3. **INTERESTING ENDPOINTS** - Hidden APIs, admin panels, debug endpoints
4. **ATTACK IDEAS** - Specific payloads or techniques to try

Keep findings SHORT, ACTIONABLE, and SECURITY-FOCUSED.
Only report HIGH and MEDIUM severity issues - skip noise.

Response data:
{}

Format output as:
[SEVERITY] Finding
- Attack vector/payload
""".format(context)
        
        # Prepare API request
        api_url = "https://api.openai.com/v1/chat/completions"
        
        data = {
            "model": "gpt-4o-mini",  # Cost-effective model
            "messages": [
                {"role": "system", "content": "You are a penetration testing assistant. Provide concise, actionable security findings only."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,  # Lower temperature for more focused output
            "max_tokens": 500  # Limit response length
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key_field.getText().strip()
        }
        
        # Make request
        req = urllib2.Request(api_url, json.dumps(data).encode('utf-8'), headers)
        
        try:
            response = urllib2.urlopen(req, timeout=30)
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
        except Exception as e:
            return "API Error: " + str(e)
    
    def display_results(self, url, ai_response):
        """Display analysis results"""
        timestamp = time.strftime("%H:%M:%S")
        
        output = "\n" + "="*80 + "\n"
        output += "[{}] Analysis for: {}\n".format(timestamp, url)
        output += "="*80 + "\n"
        output += ai_response + "\n"
        
        self.output_area.append(output)
        
        # Auto-scroll to bottom
        self.output_area.setCaretPosition(self.output_area.getDocument().getLength())
    
    def log(self, message):
        """Log message to output"""
        self.output_area.append("[*] " + message + "\n")
