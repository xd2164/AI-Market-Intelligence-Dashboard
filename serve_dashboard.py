#!/usr/bin/env python3
"""
Simple HTTP server to serve the AI Market Intelligence Dashboard locally
Run this script and share your local IP address with others on your network
"""

import http.server
import socketserver
import webbrowser
import socket
import os
from pathlib import Path

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def main():
    # Set the directory to serve
    os.chdir('data')
    
    # Choose port
    PORT = 8000
    
    # Create server
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            local_ip = get_local_ip()
            
            print("=" * 60)
            print("🚀 AI Market Intelligence Dashboard Server")
            print("=" * 60)
            print(f"📊 Dashboard URL: http://{local_ip}:{PORT}/dashboard_with_trends.html")
            print(f"💰 Deals Table: http://{local_ip}:{PORT}/deals_table.html")
            print(f"☁️ Hyperscaler Engagement: http://{local_ip}:{PORT}/hyperscaler_engagement_dashboard.html")
            print("=" * 60)
            print("📱 Share these URLs with others on your network!")
            print("🛑 Press Ctrl+C to stop the server")
            print("=" * 60)
            
            # Open the main dashboard
            webbrowser.open(f'http://{local_ip}:{PORT}/dashboard_with_trends.html')
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} is already in use. Try a different port.")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
