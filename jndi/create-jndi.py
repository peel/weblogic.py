# A script for creating a Foreign JNDI Providers
#
# Usage:
# create-jndi.py <Properties File Name>

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
 
for foreignJNDI in FOREIGN_JNDI_ARRAY:
    if (foreignJNDI['TARGET_TYPE']=="SERVER"):
        targetMB=getMBean("/Servers/"+foreignJNDI['TARGET'])
    if (foreignJNDI['TARGET_TYPE']=="CLUSTER"):
        targetMB=getMBean("/Clusters/"+foreignJNDI['TARGET'])
    if targetMB is None:
        print "@@@ Invalid Foreign JNDI Provider Target '"+foreignJNDI['TARGET']+"'"
        exit()
    if getMBean("/ForeignJNDIProviders/"+foreignJNDI['NAME']) is None:      
        foreignJNDIInstance=create(foreignJNDI['NAME'],"ForeignJNDIProvider")
        foreignJNDIInstance.addTarget(targetMB)
        foreignJNDIInstance.setInitialContextFactory(foreignJNDI['INITIAL_CONTEXT_FACTORY'])
        foreignJNDIInstance.setProviderURL(foreignJNDI['PROVIDER_URL'])
        foreignJNDIInstance.setUser(foreignJNDI['USER'])
        foreignJNDIInstance.setPassword(foreignJNDI['PASSWORD'])
     
        for foreignLink in foreignJNDI['LINKS_ARRAY']:
            foreignLinkInstance=foreignJNDIInstance.createForeignJNDILink(foreignLink['NAME'])
            foreignLinkInstance.setLocalJNDIName(foreignLink['LOCAL_JNDI'])
            foreignLinkInstance.setRemoteJNDIName(foreignLink['REMOTE_JNDI'])
     
         
activate()
exit()