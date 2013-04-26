# A script for creating JMS Modules in WLS domain
#
# Usage:
# create-jms.py <Properties File Name>

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

if (JMS_MODULE_TARGET_TYPE=="SERVER"):
    defTargetMB=getMBean("/Servers/"+JMS_MODULE_TARGET)

if (JMS_MODULE_TARGET_TYPE=="CLUSTER"):
    defTargetMB=getMBean("/Clusters/"+JMS_MODULE_TARGET)

if (JMS_MODULE_TARGET_TYPE=="JMS"):
    defTargetMB=getMBean("/JMSServers/"+JMS_MODULE_TARGET)
 
if defTargetMB is None:
    print "@@@ Invalid JMS Module Target '"+JMS_MODULE_TARGET+"'"
    exit()
 
# Create Module
if getMBean("/JMSSystemResources/"+JMS_MODULE_NAME) is None:
    jmsModule = create(JMS_MODULE_NAME, "JMSSystemResource")
    jmsModule.addTarget(defTargetMB)
else:
    jmsModule=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME)
jmsResource = jmsModule.getJMSResource()
 
# Create JMS sub deployment 
for subDeployment in JMS_SUB_DEPLOYMENT_ARRAY :
    jmsSubDeployment=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/SubDeployments/"+subDeployment["JMS_SUB_DEPLOYMENT_NAME"])
    
    if jmsSubDeployment is None:
        jmsSubDeployment=jmsModule.createSubDeployment(subDeployment["JMS_SUB_DEPLOYMENT_NAME"])
     
        if (subDeployment['JMS_SUB_DEPLOYMENT_TARGET_TYPE']=="SERVER"):
            sdTargetMB=getMBean("/Servers/"+subDeployment['JMS_SUB_DEPLOYMENT_TARGET'])
        if (subDeployment['JMS_SUB_DEPLOYMENT_TARGET_TYPE']=="CLUSTER"):
            sdTargetMB=getMBean("/Clusters/"+subDeployment['JMS_SUB_DEPLOYMENT_TARGET'])
        if (subDeployment['JMS_SUB_DEPLOYMENT_TARGET_TYPE']=="JMS"):
            sdTargetMB=getMBean("/JMSServers/"+subDeployment['JMS_SUB_DEPLOYMENT_TARGET'])   
        if sdTargetMB is None:
            print "@@@ Invalid JMS Sub Deployment Target '"+subDeployment['JMS_SUB_DEPLOYMENT_TARGET']+"'"
            exit()
        jmsSubDeployment.addTarget(sdTargetMB)
     
# Create & Target CF
    for name,jndiName in subDeployment['XA_CONNECTION_FACTORY_ARRAY'].items():
        newConnectionFactory=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ConnectionFactories/"+name)
        if newConnectionFactory is None:
            newConnectionFactory = jmsResource.createConnectionFactory(name)
        newConnectionFactory.setJNDIName(jndiName)
        newConnectionFactory.setSubDeploymentName(subDeployment['JMS_SUB_DEPLOYMENT_NAME'])
        newConnectionFactory.transactionParams.setXAConnectionFactoryEnabled(true)
 
    for name,jndiName in subDeployment['CONNECTION_FACTORY_ARRAY'].items():
        newConnectionFactory=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ConnectionFactories/"+name)
        if newConnectionFactory  is None:
            newConnectionFactory = jmsResource.createConnectionFactory(name)
        newConnectionFactory.setJNDIName(jndiName)
        newConnectionFactory.setSubDeploymentName(subDeployment['JMS_SUB_DEPLOYMENT_NAME'])
        newConnectionFactory.transactionParams.setXAConnectionFactoryEnabled(false)
         
# Create & Target Queues
    for name,jndiName in subDeployment['QUEUE_ARRAY'].items():
        newQueue=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/Queues/"+name)
        if newQueue is None:
            newQueue = jmsResource.createQueue(name)
        newQueue.setJNDIName(jndiName)
        newQueue.setSubDeploymentName(subDeployment['JMS_SUB_DEPLOYMENT_NAME'])
 
# Create & Target Topics
    for name,jndiName in subDeployment['TOPIC_ARRAY'].items():
        newTopic=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/Topics/"+name)
        if newTopic is None:
            newTopic = jmsResource.createTopic(name)
        newTopic.setJNDIName(jndiName)
        newTopic.setSubDeploymentName(subDeployment['JMS_SUB_DEPLOYMENT_NAME'])
 
# Create & Target ForeignJMS
    for foreignServer in subDeployment['FOREIGN_JMS_SERVER_ARRAY']:
        foreignJMS=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME'])
        if foreignJMS is None:
            foreignJMS =jmsResource.createForeignServer(foreignServer['FOREIGN_JMS_SERVER_NAME'])
        foreignJMS.setSubDeploymentName(subDeployment['JMS_SUB_DEPLOYMENT_NAME'])
        foreignJMS.setInitialContextFactory(foreignServer['FOREIGN_JMS_SERVER_INITIAL_CONTEXT_FACTORY'])
        foreignJMS.setConnectionURL(foreignServer['FOREIGN_JMS_SERVER_PROVIDER_URL'])  
        foreignJMS.unSet('JNDIPropertiesCredentialEncrypted')
        jndiProperty=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/JNDIProperties/"+foreignServer['FOREIGN_JMS_SERVER_JNDI_PROPERTY_KEY'])
        if jndiProperty is None:
            jndiProperty=foreignJMS.createJNDIProperty(foreignServer['FOREIGN_JMS_SERVER_JNDI_PROPERTY_KEY'])
        jndiProperty.setValue(foreignServer['FOREIGN_JMS_SERVER_JNDI_PROPERTY_VALUE'])      
    # Create ForeignJMS Connection Factory
        for foreignCF in foreignServer['FOREIGN_JMS_CF_ARRAY']:
            foreignJMSConnectionFactory=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/ForeignConnectionFactories/"+foreignCF['NAME'])
            if foreignJMSConnectionFactory is None:
                foreignJMSConnectionFactory = foreignJMS.createForeignConnectionFactory(foreignCF['NAME']);
            foreignJMSConnectionFactory.setLocalJNDIName(foreignCF['LOCAL_JNDI'])
            foreignJMSConnectionFactory.setRemoteJNDIName(foreignCF['REMOTE_JNDI'])
     
    # Create ForeignJMS Destinations
        for foreignDest in foreignServer['FOREIGN_JMS_DEST_ARRAY']:
            foreignJMSDest=getMBean("/JMSSystemResources/"+JMS_MODULE_NAME+"/JMSResource/"+JMS_MODULE_NAME+"/ForeignServers/"+foreignServer['FOREIGN_JMS_SERVER_NAME']+"/ForeignDestinations/"+foreignDest['NAME'])
            if foreignJMSDest is None :
                foreignJMSDest = foreignJMS.createForeignDestination(foreignDest['NAME']);
            foreignJMSDest.setLocalJNDIName(foreignDest['LOCAL_JNDI'])
            foreignJMSDest.setRemoteJNDIName(foreignDest['REMOTE_JNDI'])
     
activate()
exit()
