# SWIM - Gossip protocol implementation

## Objective

To implement and understand how SWIM works

## How to run
```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m swim.node node-1 5001 6001 node-2:localhost:5002

python swim/dashboard/server.py

http://localhost:8000/dashboard
```
