# A script for creating Data Sources in WLS domain
#
# Usage:
# create-ds.py <Properties File Name>

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
connect(USER,PASSWORD,ADMIN_URL)
edit()
dsCount=0
successCount=0
for dataSource in DATASOURCE_ARRAY:
    startEdit()
    jdbcSystemResource=getMBean("/JDBCSystemResources/"+dataSource['NAME'])
    if jdbcSystemResource is None:
        jdbcSystemResource=create(dataSource['NAME'],"JDBCSystemResource")
     
        if (dataSource['TARGET_TYPE']=="SERVER"):
            targetMB=getMBean("/Servers/"+dataSource['TARGET'])
        if (dataSource['TARGET_TYPE']=="CLUSTER"):
            targetMB=getMBean("/Clusters/"+dataSource['TARGET'])
 
        if targetMB is None:
            print "@@@ Invalid DataSource Target '"+dataSource['TARGET']+"'"
            exit()
     
        jdbcSystemResource.addTarget(targetMB)
        jdbcResource=jdbcSystemResource.getJDBCResource()
        jdbcResource.setName(dataSource['NAME'])
        jdbcResource.JDBCDataSourceParams.setJNDINames(jarray.array([String(dataSource['JNDI_NAME'])], String))
        jdbcResource.JDBCDriverParams.setUrl(dataSource['URL'])
        jdbcResource.JDBCDriverParams.setDriverName(dataSource['DRIVER_NAME'])
        property=jdbcResource.JDBCDriverParams.getProperties().createProperty("USER")
        property.setValue(dataSource['USER'])
        jdbcResource.JDBCDriverParams.setPassword(dataSource['PASSWORD'])
        jdbcResource.JDBCConnectionPoolParams.setTestConnectionsOnReserve(true)
        jdbcResource.JDBCConnectionPoolParams.setTestTableName("SQL SELECT 1 FROM DUAL\r\n\r\n")
         
    else:
        if (dataSource['TARGET_TYPE']=="SERVER"):
            targetMB=getMBean("/Servers/"+dataSource['TARGET'])
        if (dataSource['TARGET_TYPE']=="CLUSTER"):
            targetMB=getMBean("/Clusters/"+dataSource['TARGET'])
        if targetMB is None:
            print "@@@ Invalid DataSource Target '"+dataSource['TARGET']+"'"
            exit() 
        if getMBean("/JDBCSystemResources/"+dataSource['NAME']+"/Targets/"+dataSource['TARGET']) is None:  
            jdbcSystemResource.addTarget(targetMB)
    try:
        activate()
        successCount=successCount+1
    except:        
        undo(defaultAnswer='y')
    dsCount=dsCount+1      
         
print str(successCount)+" DataSources out of "+str(dsCount)+"had successful connection during testing"
         
exit(defaultAnswer='y')