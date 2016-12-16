#!/bin/bash


#https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.5.1-Boron-SR1/distribution-karaf-0.5.1-Boron-SR1.zip

# setup sfc from pre-build. If DIST_URL is null, build sfc from scratch
#DIST_URL=https://nexus.opendaylight.org/content/repositories/opendaylight.snapshot/org/opendaylight/integration/distribution-karaf/0.5.1-SNAPSHOT/

DIST_URL="$1"
DEMO_DIR="$2"
ODL_ADDR="$3"


install_packages() 
{
    echo "Install os packages........................................"
    sudo apt-get install npm vim git git-review diffstat bridge-utils -y

    echo "Install java8......................................."
    #install java8
    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
    sudo add-apt-repository ppa:webupd8team/java -y
    sudo apt-get update -y
    sudo apt-get install oracle-java8-installer -y
    sudo update-java-alternatives -s java-8-oracle
    sudo apt-get install oracle-java8-set-default -y

    echo "Install maven............................................"
    #install maven
    sudo mkdir -p /usr/local/apache-maven; cd /usr/local/apache-maven
    curl https://www.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz | sudo tar -xzv
    sudo update-alternatives --install /usr/bin/mvn mvn /usr/local/apache-maven/apache-maven-3.3.9/bin/mvn 1
    sudo yes 0 | update-alternatives --config mvn 

    cat << EOF > $HOME/maven.env
export M2_HOME=/usr/local/apache-maven/apache-maven-3.3.9
export MAVEN_OPTS="-Xms256m -Xmx512m" # Very important to put the "m" on the end
export JAVA_HOME=/usr/lib/jvm/java-8-oracle # This matches sudo update-alternatives --config java
EOF

    echo "Install pip..........................................."
    # install docker compose
    sudo apt-get install -y python-pip
    sudo pip install docker-compose
}

install_sfc() 
{
    echo "Install sfc..........................................."
    cd $HOME
    if [ -n $DIST_URL ]; then
        #curl $DIST_URL/maven-metadata.xml | grep -A2 tar.gz | grep value | cut -f2 -d'>' | cut -f1 -d'<' | \
        #    xargs -I {} curl $DIST_URL/distribution-karaf-{}.tar.gz | tar xvz-
        curl $DIST_URL | tar xvz-
        rm -rf $HOME/$DEMO_DIR; mkdir -p $HOME/$DEMO_DIR/sfc-karaf/target
        mv distribution-karaf* $HOME/$DEMO_DIR/sfc-karaf/target/assembly
    else
        echo "Include steps to build from source ..."
    fi
}

echo "SFC DEMO: Packages installation"
install_packages

echo "SFC DEMO: SFC installation"
install_sfc
