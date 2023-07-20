# update_was_targets
Update Tenable Web App targets based on tagged assets in Tenable.io. This is a sample and not officially supported by Tenable.

## Installation
After creating a virtaul environment, clone this repository and run 'pip install .' in the cloned folder.

```
git clone https://github.com/agroome/update_was_targets.git ./update_was_targets
cd update_was_targets
pip install .

```

Next put your Tenable.io API keys in a file in the working folder called '.env'.  It should look like this:
```
TIO_ACCESS_KEY=32dbc3c49db...your access key
TIO_SECRET_KEY=f01c3bbfe83...your secret key
```

## Usage
Tag assets using the category 'web-app-targets' and the tag value the name of the scan that the target should be added to.

The script will build a URL by prefixing the fqdn with 'https://'. If the fqdn is not defined, then it will use the ipv4 address. (It will use the first value in the list of fqnds or ipv4s defined for the asset.)

The script then searches for the WebAppScan config with the name defined in the tag value. For example, to add an target the scan 'Example Scan', tag the asset with 'web-app-targets:Example Scan'. The scan configuration must exist before running the script.  URL targets will be overwritten on each run with URLs based on the tagged assets.

Once the assets are tagged and the scan configuration created, run the script as follows.
```
python3 ./update_was_targets
```