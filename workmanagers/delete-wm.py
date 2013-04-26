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
stMBean=getMBean("/SelfTuning/"+DOMAIN)
for workManager in WORK_MANAGER_ARRAY:
    wmMBean=getMBean("/SelfTuning/"+DOMAIN+"/WorkManagers/"+workManager['NAME'])
    if wmMBean != None: 
        stMBean.destroyWorkManager(wmMBean)
for mtConstraint in MAX_THREADS_CONSTRAINT_ARRAY:
     
    mtcMBean=getMBean("/SelfTuning/"+DOMAIN+"/MaxThreadsConstraints/"+mtConstraint['NAME'])
    if mtcMBean != None:
        print "destroying max threads constraints...."
        stMBean.destroyMaxThreadsConstraint(mtcMBean)
        print "destroyed max threads constraint"
 
activate()
exit()`