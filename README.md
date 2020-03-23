# COVID-19 contact tracing
This is an open source project for contact tracing of COVID-19 virus by leveraging your personal Location History recorded by Google.

## How to Contribute
All contributions are welcome! Please check [how to contribute](CONTRIBUTING.md) for details.

## Code of Conduct
Please check [code of conduct](CODE_OF_CONDUCT.md) for developers for details.

## License
This software is released under the [BSD3 License](LICENSE).

## For Developers
### How to setup environment
```
# Create conda environment from environment.yml file
conda env create -f ml/environment.yml

# Activate environment
conda activate covid-19

# Check if they are running
systemctl status gunicorn
systemctl status nginx

# Restart application server
sudo systemctl restart gunicorn

# Check access error log
sudo tail -F /var/log/nginx/error.log

# Check app log
journalctl -u gunicorn --no-pager
```