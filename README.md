
# Install env
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Launch script
```python
python ./app/main.py
```

# Set script launch at startup
```shell
sudo cp /home/vinc/SwanSideEvents/swanside_daemon.service /etc/systemd/system/swanside_daemon.service
chmod +x /home/vinc/SwanSideEvents/run.sh

sudo systemctl daemon-reload
sudo systemctl reset-failed
sudo systemctl enable swanside_daemon.service
sudo systemctl start swanside_daemon.service

sudo systemctl status swanside_daemon.service
```
