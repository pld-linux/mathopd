Summary:	A fast, lightweighte, non-forking HTTP server for UN*X systems
Summary(pl):	Szybki, niedu¿y, nie forkuj±cy siê serwer HTTP
Name:		mathopd
Version:	1.5
Release:	1
Group:		Networking
License:	BSD
Source0:	http://www.mathopd.org/dist/%{name}-%{version}p3.tar.gz
# Source0-md5:	6e0fea187134cb52509c2f98a8644d11
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	http://www.mathopd.org/dist/dir_cgi.c.txt
URL:		http://www.mathopd.org/
BuildRequires:	rpmbuild(macros) >= 1.159
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	sh-utils
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(post,preun):	/sbin/chkconfig
Provides:	group(http)
Provides:	httpd
Provides:	user(http)
Provides:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	/home/services/httpd

%description
Mathopd is a very small, yet very fast HTTP server for UN*X systems.
Mathopd is designed specifically to handle a large number of
connections with minimal fuss. It contains no unnecessary add-ons, but
it does the trick for most things.

%description -l pl
Mathopd jest bardzo ma³ym, bardzo szybkim serwerem HTTP dla systemów
uniksowych. Jest zaprojektowany specjalnie do obs³ugi du¿ej liczby
po³±czeñ. Nie ma niepotrzebnych dodatków, ale potrafi wiêkszo¶æ
rzeczy.

%prep
%setup -q -n %{name}-1.5p3

cp -f %{SOURCE3}  dir_cgi.c

%build
CFLAGS="%{rpmcflags}"; export CFLAGS

%{__cc} %{rpmcflags} %{rpmldflags} -o mathopd-dir_cgi dir_cgi.c

cd src
%{__make} CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/cgi-bin \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT{%{_sbindir},%{_var}/log/mathopd}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mathopd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install src/mathopd $RPM_BUILD_ROOT%{_sbindir}
install mathopd-dir_cgi $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid http`" ]; then
	if [ "`getgid http`" != "51" ]; then
		echo "Error: group http doesn't have gid=51. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 51 -r -f http
fi
if [ -n "`id -u http 2>/dev/null`" ]; then
	if [ "`id -u http`" != "51" ]; then
		echo "Error: user http doesn't have uid=51. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -u 51 -r -d %{_datadir} -s /bin/false -c "HTTP User" -g http http 1>&2
fi

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/mathopd ]; then
	/etc/rc.d/init.d/mathopd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/mathopd start\" to start %{name} HTTP daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mathopd ]; then
		/etc/rc.d/init.d/mathopd stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove http
	%groupremove http
fi

%files
%defattr(644,root,root,755)
%doc [A-Z]* doc/*
%attr(755,root,root) %{_sbindir}/mathopd*
%attr(755,http,http) %{_datadir}
%attr(754,root,root) /etc/rc.d/init.d/mathopd
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mathopd.conf
%attr(750,http,http) %dir %{_var}/log/mathopd
