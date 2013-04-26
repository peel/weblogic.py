#!/bin/bash
# Author: Christian Boerner, mailto: loci [at] locimotive.de
# NWL-Licence... do whatever you want with it. ;-)


DOMAIN_HOME="/u01/app/oracle/middleware12c/user_projects/domains/NEMIS_SC"
SCRIPT_HOME="/home/weblogic/bin/wlst"
SCRIPT_NAME=""
SETDOMAIN_OPTIONS=""

usage () {
	echo -e "Usage: $0 [-w <directory>] [-d <directory>] -s <file> -p <properties>"
	echo
	echo -e "\t-w\tDefine your WL_HOME (the directory of your domain)"
	echo -e "\t-d\tDefine your SCRIPT_HOME (the directory where your scripts are located)"
	echo -e "\t-s\tThe script you want to run via WLST"
	echo -e "\t-p\tProperties file passed to WLST script"
	echo
	echo -e "Current defaults:"
	echo -e "\tWebLogic domain  = $DOMAIN_HOME"
	echo -e "\tScript directory = $SCRIPT_HOME"
	exit 0;
}

while getopts ":hw:s:d:p:" opt; do
	case $opt in
		h)	usage
			exit 1
			;;
		w)
			if [[ "$OPTARG" == "" ]]; then
				echo "Option -$opt requires an argument" >&2
				exit 1;
			fi
			DOMAIN_HOME="$OPTARG"
			;;
		s)
			if [[ "$OPTARG" == "" ]]; then
				echo "Option -$opt requires an argument" >&2
				exit 1;
			fi
			SCRIPT_NAME="$OPTARG"
			;;
		d)
			if [[ "$OPTARG" == "" ]]; then
				echo "Option -$opt requires an argument" >&2
				exit 1;
			fi
			SCRIPT_HOME="$OPTARG"
			;;
		p)
			if [[ "$OPTARG" == "" ]]; then
				echo "Option -$opt requires an argument" >&2
				exit 1;
			fi
			SCRIPT_PROPS="$OPTARG"
			;;
		*)
			echo "Invalid option. Try \"-h\" for help" >&2
			exit 1
			;;
	esac
done

if [[ "${DOMAIN_HOME}" == "" ]]; then
	echo "Error: DOMAIN_HOME is not set!" >&2
	exit 1;
else
	if [[ ! -d ${DOMAIN_HOME} ]]; then
		echo "Error: ${DOMAIN_HOME} does not exist or is not readable" >&2
		exit 1;
	fi
fi

if [[ "${SCRIPT_HOME}" == "" ]]; then
	echo "Error: SCRIPT_HOME is not set!" >&2
	exit 1;
else
	if [[ ! -d ${DOMAIN_HOME} ]]; then
		echo "Error: ${SCRIPT_HOME} does not exist or is not readable" >&2
		exit 1;
	fi
fi

if [[ "${SCRIPT_NAME}" == "" ]]; then
	echo "Error: SCRIPT_NAME is not set!" >&2
	exit 1;
else
	if [[ ! -r ${SCRIPT_HOME}/${SCRIPT_NAME} ]]; then
		echo "Error: ${SCRIPT_HOME}/${SCRIPT_NAME} does not exist or is not readable"
		exit 1;
	fi
fi

if [[ "${SCRIPT_PROPS}" == "" ]]; then
	echo "Error: SCRIPT_PROPS is not set!" >&2
	exit 1;
fi

# ************* Setting the Environment ***********************
. ${DOMAIN_HOME}/bin/setDomainEnv.sh ${SET_DOMAIN_OPTIONS}
if [ $0 -eq 0 ]; then
	echo "Environment has been set....."
else
	echo "Error setting environment"
fi

# ************* Changing the directory where all the related files are needed ***********************
cd ${SCRIPT_HOME}

# ************* Calling the WLST script  *****************
echo "Calling the PYTHON script....."
java weblogic.WLST ${SCRIPT_NAME} ${SCRIPT_PROPS}
