# A script for creating datasources in WLS domain
#
# Usage:
# delete-ds.py <Properties File Name>

import sys

# Set up properties
if len(sys.argv) != 2:
    print "Usage: create-ds.py <Properties File Name>"
    exit()
try:
    print "Loading properties..."
    properties=sys.argv[1]

    print "Reading properties..."
    file=open(properties, 'r')

    print "Executing properties..."
    exec file

    file.close()

except:
    exit()

# Obtain connection
connect(USER, PASSWORD, ADMIN_URL)
edit()
startEdit()

jdbcSysResourceMBean=getMBean("/JDBCSystemResources/")
for dataSource in DATASOURCE_ARRAY:
    dataSourceMBean=getMBean("/JDBCSystemResources/"+dataSource['NAME'])
    if dataSourceMBean != None:
        if (dataSource['TARGET_TYPE']=="SERVER"):
            targetMB=getMBean("/Servers/"+dataSource['TARGET'])
        if (dataSource['TARGET_TYPE']=="CLUSTER"):
            targetMB=getMBean("/Clusters/"+dataSource['TARGET'])
        if targetMB != None:   
            dataSourceMBean.removeTarget(targetMB)
        if len(dataSourceMBean.getTargets()) ==0: #No Targets
            jdbcSysResourceMBean.destroyJDBCSystemResource(dataSourceMBean)
 
activate()     
exit()