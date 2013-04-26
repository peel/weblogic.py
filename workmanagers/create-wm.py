# A script for creating Work Managers in WLS domain
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
wmMBean=getMBean("/SelfTuning/"+DOMAIN)
if wmMBean is None:
        print "@@@ Invalid DOMAIN Name '"+DOMAIN+"'"
        exit()
 
for maxThreadsConst in MAX_THREADS_CONSTRAINT_ARRAY :
    if (maxThreadsConst['TARGET_TYPE']=="SERVER"):
        targetMB=getMBean("/Servers/"+maxThreadsConst['TARGET'])
    if (maxThreadsConst['TARGET_TYPE']=="CLUSTER"):
        targetMB=getMBean("/Clusters/"+maxThreadsConst['TARGET'])
    if targetMB is None:
        print "@@@ Invalid MAX THREADS CONSTRAINT Target '"+maxThreadsConst['TARGET']+"'"
        exit()
    if getMBean("/SelfTuning/"+DOMAIN+"/MaxThreadsConstraints/"+maxThreadsConst['NAME']) is None:       
        maxThreadConstInstance=wmMBean.createMaxThreadsConstraint(maxThreadsConst['NAME'])
        maxThreadConstInstance.addTarget(targetMB)
        maxThreadConstInstance.setCount(maxThreadsConst['COUNT'])
 
for workManager in WORK_MANAGER_ARRAY :
    if (workManager['TARGET_TYPE']=="SERVER"):
        targetMB=getMBean("/Servers/"+workManager['TARGET'])
    if (workManager['TARGET_TYPE']=="CLUSTER"):
        targetMB=getMBean("/Clusters/"+workManager['TARGET'])
    if targetMB is None:
        print "@@@ Invalid Work Manager Target '"+workManager['TARGET']+"'"
        exit()
    if getMBean("/SelfTuning/"+DOMAIN+"/WorkManagers/"+workManager['NAME']) is None:        
        workManagerInstance=wmMBean.createWorkManager(workManager['NAME'])
        workManagerInstance.addTarget(targetMB)
        workManagerInstance.setMaxThreadsConstraint(wmMBean.lookupMaxThreadsConstraint(workManager['MAX_THREADS_CONSTRAINT']))
     
activate()
exit()