#!/bin/bash
cd "$(dirname "$0")"
echo "Starting TJ Math Quiz Server..."
echo "================================"
echo ""
echo "Opening http://localhost:8000 in your browser..."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 -m http.server 8000
