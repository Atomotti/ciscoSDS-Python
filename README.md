# ciscoSDS-Python
 Cisco UCSM Configuration for Scale-Out Object Storage based on Python. Prerequistes for the script is

 - All servers are connected to FI ports and ports are configured
 - C220 and S3260 server have identical hardware
 - Port Channels and FI Uplinks are configured

## ucsm.json
Environment file for most configurations in UCS Manager

## ucsm_query.py
Queries the environment to get the most information about the connected servers

## ucsm_sds_config.py
Main script to configure the whole UCSM environment
