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
moduleMBean=getMBean("/JMSSystemResources/")
sdMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/SubDeployments/")
cfMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ConnectionFactories/")
queueMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/Queues/")
topicMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/Topics/")
foreignServerMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/")
 
for subDeployment in JMS_SUB_DEPLOYMENT_ARRAY :
     
    for name,jndiName in subDeployment['XA_CONNECTION_FACTORY_ARRAY'].items():
        cfInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ConnectionFactories/"+name)
        if cfInstanceMBean != None:
            cfMBean.destroyConnectionFactory(cfInstanceMBean)   
     
    for name,jndiName in subDeployment['CONNECTION_FACTORY_ARRAY'].items():
        cfInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ConnectionFactories/"+name)
        if cfInstanceMBean != None:
            cfMBean.destroyConnectionFactory(cfInstanceMBean)   
         
     
    for name,jndiName in subDeployment['QUEUE_ARRAY'].items():
        qInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/Queues/"+name)
        if qInstanceMBean != None:
            queueMBean.destroyQueue(qInstanceMBean)
     
    for name,jndiName in subDeployment['TOPIC_ARRAY'].items():
        tInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/Topics/"+name)
        if tInstanceMBean != None:
            topicMBean.destroyTopic(tInstanceMBean)
     
    for foreignServer in subDeployment['FOREIGN_JMS_SERVER_ARRAY']:
        foreignCFMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/ForeignConnectionFactories/")
        foreignJMSDestMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/ForeignDestinations/")
        foreignPropertiesMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/JNDIProperties/")
        foreignPropertiesInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/JNDIProperties/"+foreignServer['FOREIGN_JMS_SERVER_JNDI_PROPERTY_KEY'])
         
        if foreignPropertiesInstanceMBean != None :
            foreignPropertiesMBean.destroyJNDIProperty(foreignPropertiesInstanceMBean)
         
        for  foreignCF in foreignServer['FOREIGN_JMS_CF_ARRAY']:
            foreignCFInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/ForeignConnectionFactories/"+foreignCF['NAME'])    
            if foreignCFInstanceMBean != None :
                foreignCFMBean.destroyForeignConnectionFactory(foreignCFInstanceMBean)
        for foreignDest in foreignServer['FOREIGN_JMS_DEST_ARRAY']:
            foreignJMSDestInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/ForeignDestinations/"+foreignDest['NAME'])
            if foreignJMSDestInstanceMBean != None :
                foreignJMSDestMBean.destroyForeignDestination(foreignJMSDestInstanceMBean)
         
        foreignServerInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME'])
        if foreignServerInstanceMBean != None:
            foreignServerMBean.destroyForeignServer(foreignServerInstanceMBean)
     
    sdInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/SubDeployments/"+subDeployment['JMS_SUB_DEPLOYMENT_NAME'])
    if sdInstanceMBean != None:
        sdMBean.destroySubDeployment(sdInstanceMBean)
     
moduleInstanceMBean=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME)
if moduleInstanceMBean != None:
    moduleMBean.destroyJMSSystemResource(moduleInstanceMBean)
     
activate()
exit()