# A script for deleting Foreign JNDI Providers in WLS domain
#
# Usage:
# create-wm.py <Properties File Name>

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
startEdit()
forJNDIProviderMBean=getMBean("/ForeignJNDIProviders/")
for foreignJNDI in FOREIGN_JNDI_ARRAY:
    jndiProviderInstance=getMBean("/ForeignJNDIProviders/"+foreignJNDI['NAME'])
    if jndiProviderInstance != None: 
        forJNDIProviderMBean.destroyForeignJNDIProvider(jndiProviderInstance)
         
activate()
exit()