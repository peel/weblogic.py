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
bdgDestMBean=getMBean("/JMSBridgeDestinations/")
bdgMBean=getMBean("/MessagingBridges/")
for msgBridge in MSGBRIDGE_ARRAY:
      
    destinations = (msgBridge['SOURCE_DEST'],msgBridge['TARGET_DEST'])
     
    bdgInstanceMBean=getMBean("/MessagingBridges/"+msgBridge['NAME'])
    if bdgInstanceMBean != None:
        bdgMBean.destroyMessagingBridge(bdgInstanceMBean)
         
    for dest in destinations :
        destMBean=getMBean("/JMSBridgeDestinations/"+dest['NAME'])
        if destMBean != None: 
            bdgDestMBean.destroyJMSBridgeDestination(destMBean)
         
activate()
exit()