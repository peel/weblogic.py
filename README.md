Weblogic Resource Management Scripts
====================================

## Info
The repository contains framework for standalone scripts used for resource management in WLS domains.  

## Configuration
Scripts are configured via properties files (examples supplied with scripts)

**DataSource**
Properties for DataSources are named after WLS' parameters set in the web console.
To add several DSs with a single call simply add another named property (ie. DataSourceName2) and extend the `DATA_SOURCEARRAY` with the new one.

## Main script
```
Usage: ./runscript.sh [-w <directory>] [-d <directory>] -s <file> -p <properties>

        -w      Define your WL_HOME (the directory of your domain)
        -d      Define your SCRIPT_HOME (the directory where your scripts are located)
        -s      The script you want to run via WLST
        -p      Properties file passed to WLST script
```

## Running scripts directly
Script usage is described in headers. 
Please refer to there for the detailed information.

The defacto standard for running scripts is:

        ./scriptname.py <properties file name>.properties
