%define name drqueue
%define version 0.64.4c1
%define release %mkrel 3

Summary: Render farm managing software
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}.%{version}.tgz
Source1: drqueue.profile
Source2: slave.conf
Source3: master.conf
Source4: drqman.conf
License: GPL 
Group: System/Cluster
Url: http://www.drqueue.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildrequires: pkgconfig gtk2-devel scons

%description
DrQueue is an Open Source render farm managing software. It distributes 
shell based tasks such as rendering images on a per frame basis. 
DrQueue works under Linux, FreeBSD, Irix, Mac OS X and Windows. 
It is distributed under GPL and is composed by three main tools: 
master, slave and drqman.

%prep
%setup -q -n DrQueue-%version

%build
echo "DESTDIR = '$RPM_BUILD_ROOT'" > scons.conf
echo "PREFIX = '%{_prefix}'" >> scons.conf
scons

%install
rm -rf $RPM_BUILD_ROOT
# create needed dir
install -d 755 $RPM_BUILD_ROOT/var/log/drqueue $RPM_BUILD_ROOT/var/tmp/drqueue
install -d 755 $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
install -d 755 $RPM_BUILD_ROOT/%{_sysconfdir}/%name
install -d 755 $RPM_BUILD_ROOT/%{_bindir}
install -d 755 $RPM_BUILD_ROOT/%_datadir/%name

# copy conf file from the source
cp -av etc/*.sg $RPM_BUILD_ROOT/%{_sysconfdir}/%name/
cp -av etc/*.rc $RPM_BUILD_ROOT/%{_sysconfdir}/%name/
cp -av etc/*.py $RPM_BUILD_ROOT/%{_sysconfdir}/%name/

# copy basic configuration file
cp -av %{SOURCE2} %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/%name/ 

# copy binaries
ARCH=`uname -m`
cp -av bin/* $RPM_BUILD_ROOT/%{_bindir}/
cp -av drqman/drqman $RPM_BUILD_ROOT/%{_bindir}/drqman.Linux.$ARCH
# copy wrappers
for bin in `ls blockhost cfgreader cjob compinfo delipc jobfinfo jobinfo master requeue sendjob slave`
do
cp -av $bin $RPM_BUILD_ROOT/%{_bindir}/$bin.Linux.$ARCH
done
cp -av contrib/sendjob.blender.py $RPM_BUILD_ROOT/%_datadir/%name
# copy profile
cp -av %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/%name.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING README* INSTALL AUTHORS
%config(noreplace) %{_sysconfdir}/%name/*.sg
%config(noreplace) %{_sysconfdir}/%name/*.rc
%config(noreplace) %{_sysconfdir}/%name/*.conf
%config(noreplace) %{_sysconfdir}/%name/*.py
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %_datadir/%name/
/var/log/drqueue
%attr(755,root,root) %{_sysconfdir}/profile.d/%name.sh
