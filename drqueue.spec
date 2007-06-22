%define name drqueue
%define version 0.64.1
%define release %mkrel 2

Summary: DrQueue is an Open Source render farm managing software
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}.%{version}.tar.bz2
Source1: drqueue.profile
Patch0: drqueue-Makefile.patch
License: GPL 
Group: System/Cluster
Url: http://www.drqueue.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Buildrequires: pkgconfig gtk2-devel

%description
DrQueue is an Open Source render farm managing software. It distributes 
shell based tasks such as rendering images on a per frame basis. 
DrQueue works under Linux, FreeBSD, Irix, Mac OS X and Windows. 
It is distributed under GPL and is composed by three main tools: 
master, slave and drqman.

%prep
%setup -q -n %name-%version
%patch0 -p0 -b .installdir

%build
%make INSTUID=root INSTGID=root INSTROOT=$RPM_BUILD_ROOT PREFIX=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
install -d 755 $RPM_BUILD_ROOT/var/log/drqueue $RPM_BUILD_ROOT/var/tmp/drqueue
install -d 755 $RPM_BUILD_ROOT/etc/profile.d
%makeinstall INSTROOT=$RPM_BUILD_ROOT INSTUID=root INSTGID=root PREFIX=%{_prefix}
cp -av %{SOURCE1} $RPM_BUILD_ROOT/etc/profile.d/drqueue

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING CREDITS README 
%config(noreplace) %{_sysconfdir}/*.sg
%config(noreplace) %{_sysconfdir}/*.rc
%config(noreplace) %{_sysconfdir}/*.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /usr/share/%name/
%attr(755,root,root) /usr/share/%name/contrib
/var/log/drqueue
%attr(755,root,root) /etc/profile.d/drqueue


