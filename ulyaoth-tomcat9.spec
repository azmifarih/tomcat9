
%define __jar_repack %{nil}
%define debug_package %{nil}
%define tomcat_home /opt/apache-tomcat-
%define tomcat_group sfe
%define tomcat_user sfe

# distribution specific definitions
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

%if 0%{?rhel}  == 6
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
%endif

%if 0%{?rhel}  == 7
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

%if 0%{?fedora} >= 18
Requires(pre): shadow-utils
Requires: systemd
BuildRequires: systemd
%endif

# end of distribution specific definitions

Summary:    apache-tomcat-9.0.40
Name:       tomcat
Version:    9.0.40
Release:    1
BuildArch:  x86_64
License:    Apache License version 2
Group:      Applications/Internet
URL:        https://tomcat.apache.org/
Vendor:     Apache Software Foundation
Packager:   Sjir Bagmeijer <sjir.bagmeijer@ulyaoth.com> edited by Azmi <azmi.farih@pareteum.com>
Source0:    http://apache.mirrors.spacedump.net/tomcat/tomcat-9/v%{version}/bin/apache-tomcat-%{version}.tar.gz
Source1:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.service
Source2:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.init
Source3:    https://raw.githubusercontent.com/ulyaoth/repository/master/ulyaoth-tomcat/SOURCES/tomcat.logrotate
BuildRoot:  %{_tmppath}/tomcat-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: tomcat
Provides: apache-tomcat
Provides: apache-tomcat9

%description
Apache Tomcat is an open source software implementation of the Java Servlet and JavaServer Pages technologies. The Java Servlet and JavaServer Pages specifications are developed under the Java Community Process.

Apache Tomcat is developed in an open and participatory environment and released under the Apache License version 2. Apache Tomcat is intended to be a collaboration of the best-of-breed developers from around the world. We invite you to participate in this open development project. To learn more about getting involved, click here.

Apache Tomcat powers numerous large-scale, mission-critical web applications across a diverse range of industries and organizations. Some of these users and their stories are listed on the PoweredBy wiki page.

Apache Tomcat, Tomcat, Apache, the Apache feather, and the Apache Tomcat project logo are trademarks of the Apache Software Foundation.

%prep
%setup -q -n apache-tomcat-%{version}

%build

%install
install -d -m 755 %{buildroot}/%{tomcat_home}%{version}/
cp -R * %{buildroot}/%{tomcat_home}%{version}/

%{__rm} -rf %{buildroot}/%{tomcat_home}%{version}/conf/*

# Put logging in /var/log and link back.
rm -rf %{buildroot}/%{tomcat_home}%{version}/logs
install -d -m 755 %{buildroot}/var/log/tomcat/
cd %{buildroot}/%{tomcat_home}%{version}/
ln -s /var/log/tomcat/ logs
cd -

%if %{use_systemd}
# install systemd-specific files
%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -m644 %SOURCE1 \
        $RPM_BUILD_ROOT%{_unitdir}/tomcat.service
%else
# install SYSV init stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_initrddir}
%{__install} -m755 %{SOURCE2} \
   $RPM_BUILD_ROOT%{_initrddir}/tomcat
%endif

# install log rotation stuff
%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE3} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/tomcat

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
cp -R /opt/tomcat /opt/tomcat_bak
rm -rf /etc/systemd/system/tomcat.service

%files
%defattr(-,%{tomcat_user},%{tomcat_group})
%{tomcat_home}%{version}/*
%dir %{tomcat_home}%{version}
%dir %{_localstatedir}/log/tomcat

%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/logrotate.d/tomcat
%{_unitdir}/tomcat.service

%post
# Register the tomcat service
cp -R /opt/tomcat_bak/webapps/* %{tomcat_home}%{version}/webapps/
cp -R /opt/tomcat_bak/lib/apps/ %{tomcat_home}%{version}/lib/
cp -R /opt/tomcat_bak/conf/* %{tomcat_home}%{version}/conf/
cp /opt/tomcat_bak/lib/mysql* %{tomcat_home}%{version}/lib/
cp /opt/tomcat_bak/lib/comsys* %{tomcat_home}%{version}/lib/
chown -R sfe:sfe %{tomcat_home}%{version}/ 
rm -Rf /opt/tomcat_bak
cd /opt/
rm -rf tomcat
ln -s apache-tomcat-%{version} tomcat
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 ||:
/usr/bin/systemctl restart tomcat >/dev/null 2>&1 ||:
