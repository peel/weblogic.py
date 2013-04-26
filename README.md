WLST Scripts
============

# Info
Following scripts are provided:
* Create DataSource
* Delete DataSource

# Usage
## Configuration
Scripts are configured via properties files (examples supplied with scripts)

**DataSource**
Properties for DataSources are named after WLS' parameters set in the web console.
To add several DSs with a single call simply add another named property (ie. DataSourceName2) and extend the `DATA_SOURCEARRAY` with the new one.


## Running scripts
Script usage is described in headers. 
Please refer to there for the detailed information.

The defacto standard for running scripts is:

        ./scriptname.py <properties file name>.properties
