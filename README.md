# tomcat9
Build RPM package CentOS 7 for latest tomcat9

cloned from https://github.com/ulyaoth/repository/tree/master/ulyaoth-tomcat and edited for internal used.

How to build tomcat9 from spec file:

1. Install package needed
<br>
yum install rpm-build
<br>
yum install yum-utils
<br>
yum install spectool
<br>
2. Create build environment
<br>
rpmdev-setuptree
<br>
3. Download spec file
<br>
wget https://raw.githubusercontent.com/azmifarih/tomcat9/main/azmifarih-tomcat9.spec
<br>
4. Download additional files specified in spec file
<br>
spectool azmifarih-tomcat9.spec -g -R
<br>
5. Build the rpm
<br>
rpmbuild -ba azmifarih-tomcat9.spec
<br>
