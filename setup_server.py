"""
Setup Server - Configuration webpage for Boot_Lang initial setup.

Uses Python's built-in http.server - no external dependencies needed.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.parse

class SetupHandler(BaseHTTPRequestHandler):
    """Handle setup webpage requests."""
    
    def do_GET(self):
        """Serve the setup page."""
        if self.path == '/setup' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            template_path = os.path.join("templates", "setup.html")
            with open(template_path, 'rb') as f:
                self.wfile.write(f.read())
        
        elif self.path == '/progress':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Read progress log
            if os.path.exists('setup_progress.log'):
                with open('setup_progress.log', 'r') as f:
                    lines = f.readlines()
                
                progress = []
                complete_url = ""
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('PROGRESS:'):
                        task = line.replace('PROGRESS:', '')
                        progress.append({"task": task, "status": "running"})
                    elif line.startswith('DONE:'):
                        task = line.replace('DONE:', '')
                        # Update matching task to done
                        for p in progress:
                            if p["task"] == task:
                                p["status"] = "done"
                    elif line.startswith('COMPLETE:'):
                        complete_url = line.replace('COMPLETE:', '')
                
                self.wfile.write(json.dumps({
                    "progress": progress,
                    "complete": bool(complete_url),
                    "url": complete_url
                }).encode())
            else:
                self.wfile.write(json.dumps({
                    "progress": [],
                    "complete": False,
                    "url": ""
                }).encode())
                
        elif self.path == '/config':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if os.path.exists('user_config.json'):
                with open('user_config.json', 'r') as f:
                    self.wfile.write(f.read().encode())
            else:
                default_config = {
                    "setup_complete": False,
                    "git_initialized": False,
                    "user_identity": {"user_name": "", "project_name": ""},
                    "api_keys": {
                        "openai_api_key": "",
                        "anthropic_api_key": "",
                        "langsmith_api_key": ""
                    },
                    "azure_settings": {
                        "app_service_name": "",
                        "static_web_app_url": "",
                        "resource_group": "",
                        "subscription_id": "",
                        "region": "eastus2"
                    },
                    "git_deployment": {
                        "github_repo_url": "",
                        "deployment_branch": "main"
                    },
                    "preferences": {
                        "use_prd_tool": True,
                        "auto_deploy": False,
                        "openai_model_preference": "gpt-4",
                        "timezone": "UTC"
                    }
                }
                self.wfile.write(json.dumps(default_config).encode())
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle save requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/save-progress':
                # Save partial config
                config_dict = {
                    "setup_complete": False,
                    "git_initialized": False,
                    "user_identity": {
                        "user_name": data.get("user_name", ""),
                        "project_name": data.get("project_name", "")
                    },
                    "api_keys": {
                        "openai_api_key": data.get("openai_api_key", ""),
                        "anthropic_api_key": data.get("anthropic_api_key", ""),
                        "langsmith_api_key": data.get("langsmith_api_key", "")
                    },
                    "azure_settings": {
                        "app_service_name": data.get("app_service_name", ""),
                        "static_web_app_url": data.get("static_web_app_url", ""),
                        "resource_group": data.get("resource_group", ""),
                        "subscription_id": data.get("subscription_id", ""),
                        "region": data.get("region", "eastus2")
                    },
                    "git_deployment": {
                        "github_repo_url": data.get("github_repo_url", ""),
                        "deployment_branch": "main"
                    },
                    "preferences": {
                        "use_prd_tool": data.get("use_prd_tool", True),
                        "auto_deploy": data.get("auto_deploy", False),
                        "openai_model_preference": data.get("openai_model_preference", "gpt-4"),
                        "timezone": data.get("timezone", "UTC")
                    }
                }
                
                with open('user_config.json', 'w') as f:
                    json.dump(config_dict, f, indent=2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "message": "Progress saved"}).encode())
                
            elif self.path == '/init-git':
                # Initialize Git and push to GitHub
                github_url = data.get('github_repo_url', '')
                
                if not github_url:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": False,
                        "message": "GitHub URL required"
                    }).encode())
                    return
                
                try:
                    import subprocess
                    
                    # Remove existing origin if any
                    subprocess.run(['git', 'remote', 'remove', 'origin'], 
                                 stderr=subprocess.DEVNULL, check=False)
                    
                    # Add new origin
                    result = subprocess.run(
                        ['git', 'remote', 'add', 'origin', github_url],
                        capture_output=True, text=True, check=True
                    )
                    
                    # Create initial commit if needed
                    subprocess.run(['git', 'add', '.'], check=False)
                    subprocess.run(
                        ['git', 'commit', '-m', 'Initial Boot_Lang scaffold setup'],
                        check=False
                    )
                    
                    # Push to GitHub
                    result = subprocess.run(
                        ['git', 'push', '-u', 'origin', 'main'],
                        capture_output=True, text=True
                    )
                    
                    if result.returncode != 0:
                        # Try creating main branch first
                        subprocess.run(['git', 'branch', '-M', 'main'], check=False)
                        result = subprocess.run(
                            ['git', 'push', '-u', 'origin', 'main'],
                            capture_output=True, text=True, check=True
                        )
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    # Save git_initialized flag to config
                    if os.path.exists('user_config.json'):
                        with open('user_config.json', 'r') as f:
                            config = json.load(f)
                        config['git_initialized'] = True
                        with open('user_config.json', 'w') as f:
                            json.dump(config, f, indent=2)
                    
                    self.wfile.write(json.dumps({
                        "success": True,
                        "message": "Git initialized and pushed to GitHub"
                    }).encode())
                    
                except subprocess.CalledProcessError as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": False,
                        "message": f"Git command failed: {e.stderr if hasattr(e, 'stderr') else str(e)}"
                    }).encode())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "success": False,
                        "message": str(e)
                    }).encode())
                
            elif self.path == '/complete-setup':
                # Debug: print received data
                print("Received data:", json.dumps(data, indent=2))
                
                # Validate required fields
                required = ['user_name', 'project_name', 'openai_api_key', 'github_repo_url', 'app_service_name', 'resource_group']
                missing = [f for f in required if not data.get(f) or not str(data.get(f)).strip()]
                
                print(f"Missing fields: {missing}")
                
                if missing:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "detail": f"Required fields missing: {', '.join(missing)}"
                    }).encode())
                    return
                
                # Save complete config
                config_dict = {
                    "setup_complete": True,
                    "git_initialized": True,
                    "user_identity": {
                        "user_name": data.get("user_name"),
                        "project_name": data.get("project_name")
                    },
                    "api_keys": {
                        "openai_api_key": data.get("openai_api_key"),
                        "anthropic_api_key": data.get("anthropic_api_key", ""),
                        "langsmith_api_key": data.get("langsmith_api_key", "")
                    },
                    "azure_settings": {
                        "app_service_name": data.get("app_service_name"),
                        "static_web_app_url": data.get("static_web_app_url", ""),
                        "resource_group": data.get("resource_group"),
                        "subscription_id": data.get("subscription_id", ""),
                        "region": data.get("region", "eastus2")
                    },
                    "git_deployment": {
                        "github_repo_url": data.get("github_repo_url"),
                        "deployment_branch": "main"
                    },
                    "preferences": {
                        "use_prd_tool": data.get("use_prd_tool", True),
                        "auto_deploy": data.get("auto_deploy", False),
                        "openai_model_preference": data.get("openai_model_preference", "gpt-4"),
                        "timezone": data.get("timezone", "UTC")
                    }
                }
                
                with open('user_config.json', 'w') as f:
                    json.dump(config_dict, f, indent=2)
                
                print("✓ Configuration saved successfully")
                print("✓ Starting automation in background...")
                
                # Trigger automation script in background
                import subprocess
                subprocess.Popen(
                    ['bash', 'automation.sh'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "success": True,
                    "message": "Configuration complete!",
                    "config": config_dict
                }).encode())
                
                # Server stays alive to serve /progress during automation
            else:
                self.send_error(404)
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": str(e)}).encode())
    
    def log_message(self, format, *args):
        """Suppress log messages."""
        pass


if __name__ == "__main__":
    print("=" * 60)
    print("Boot_Lang Configuration Webpage")
    print("=" * 60)
    print("\nOpen your browser to: http://localhost:8001/setup")
    print("\nFill in your configuration details and click 'Save & Complete Setup'")
    print("=" * 60)
    print()
    
    server = HTTPServer(('0.0.0.0', 8001), SetupHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Setup server stopped")
        server.shutdown()
