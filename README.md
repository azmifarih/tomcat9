# tomcat9
Build RPM package CentOS 7 for latest tomcat9

cloned from https://github.com/ulyaoth/repository/tree/master/ulyaoth-tomcat and edited for internal used.

How to build tomcat9 from spec file:

 - Install package needed
    
    ```
    yum install rpm-build
    
    yum install yum-utils
    
    yum install spectool
    
    ```

 - Create build environment
    
    ```
    rpmdev-setuptree    
    ```

 - Download spec file
 
   ```
   wget https://raw.githubusercontent.com/azmifarih/tomcat9/main/azmifarih-tomcat9.spec
   ```
   
 - Download additional files specified in spec file
 
   ```
    spectool azmifarih-tomcat9.spec -g -R
   ```
   
 - Build the rpm
   ```
    rpmbuild -ba azmifarih-tomcat9.spec
   ```
