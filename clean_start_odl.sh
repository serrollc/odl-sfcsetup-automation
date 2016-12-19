#!/bin/bash

DIST_URL="$1"
DEMO_DIR="$2"
ODL_ADDR="$3"

stop_sfc () 
{
    retries=3
    while [ $retries -gt 0 ]
    do
        ODL_STATUS=`$HOME/$DEMO_DIR/sfc-karaf/target/assembly/bin/status`
        if [ "" = "$ODL_STATUS" ];
        then 
            ODL_STATUS="Not Running ..."
        fi

        IS_ODL_RUNNING=`echo $ODL_STATUS | grep "Not Running ...\|The container is not running" | wc -l`
        if [ "1" = "$IS_ODL_RUNNING"  ] ; then     
            echo "Odl not running ..."
            return 
        fi
        cd $HOME/$DEMO_DIR/sfc-karaf/target/assembly/
        bin/stop
        sleep 30
        retries=$(( $retries - 1 ))
    done

    if [ $retries -eq 0 ]; then
        echo "Karaf not stopped. Exit immediately"
        exit 1
    fi
}

start_sfc () 
{
    cd $HOME/$DEMO_DIR/sfc-karaf/target/assembly/
    if grep -q "odl-sfc-provider,odl-sfc-core,odl-sfc-ui,odl-sfc-openflow-renderer,odl-sfc-scf-openflow,odl-sfc-sb-rest,odl-sfc-ovs,odl-sfc-netconf" etc/org.apache.karaf.features.cfg; 
    then
       echo "Boot feature already added ..."
    else
    sed -i "/^featuresBoot[ ]*=/ s/$/,odl-sfc-provider,odl-sfc-core,odl-sfc-ui,odl-sfc-openflow-renderer,odl-sfc-scf-openflow,odl-sfc-sb-rest,odl-sfc-ovs,odl-sfc-netconf/" etc/org.apache.karaf.features.cfg;
    fi

    if grep -q "ovsdb.address" etc/custom.properties; then 
        sed -i "s/ovsdb.address.*/ovsdb.address=${ODL_ADDR}/" etc/custom.properties;
    else
        echo "ovsdb.address=${ODL_ADDR}" >> etc/custom.properties;
    fi    

    echo "log4j.logger.org.opendaylight.sfc = DEBUG" >> etc/org.ops4j.pax.logging.cfg;
    rm -rf journal snapshots; bin/start
    #wait for sfc ready
    retries=2
    while [ $retries -gt 0 ]
    do
        sleep 30
        sfcfeatures=$($HOME/$DEMO_DIR/sfc-karaf/target/assembly/bin/client -u karaf 'feature:list -i' 2>&1 | grep odl-sfc | wc -l)
        if [ $sfcfeatures -eq 9 ]; then
            break
        fi
        retries=$(( $retries - 1 ))
    done
    if [ $retries -eq 0 ]; then
        echo "Karaf not started. Exit immediately"
        exit 1
    fi
    IS_ODL_RUNNING=`$HOME/$DEMO_DIR/sfc-karaf/target/assembly/bin/status`
    echo "Karaf...........$IS_ODL_RUNNING"
}

if test -f "$HOME/$DEMO_DIR/sfc-karaf/target/assembly/version.properties"; 
then 
    #STOP ODL karaf
    ODL_STATUS=`$HOME/$DEMO_DIR/sfc-karaf/target/assembly/bin/status`
    if [ "" = "$ODL_STATUS" ];
    then 
        ODL_STATUS="Not Running ..."
    fi

    IS_ODL_RUNNING=`echo $ODL_STATUS | grep "Not Running ...\|The container is not running" | wc -l`
    if [ "1" = "$IS_ODL_RUNNING"  ] ; then 
        echo "Odl not running ..."
    else 
        echo "Stopping karaf ...  "
        ssh-keygen -f "$HOME/.ssh/known_hosts" -R [$ODL_ADDR]:8101
        stop_sfc
    fi

    #START ODL karaf
    echo "Starting karaf ...  "
    start_sfc
fi
