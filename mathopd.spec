Summary:	A fast, lightweighte, non-forking HTTP server for UN*X systems
Summary(pl):	Szybki, niedu¿y, nie forkuj±cy siê serwer HTTP
Name:		mathopd
Version:	1.4gamma
Release:	2
Group:		Networking
License:	BSD
Source0:	http://www.mathopd.org/dist/%{name}-1.4-gamma.tar.gz
Source1:	%{name}.init
Source2:	%{name}.conf
URL:		http://www.mathopd.org/
Provides:	httpd
Provides:	webserver
Requires(pre):	sh-utils
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/userdel
Requires(postun):	/usr/sbin/groupdel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -n %{name}-1.4

%build
CFLAGS="%{rpmcflags}"; export CFLAGS
cd src
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/home/httpd/cgi-bin \
	$RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT{%{_sbindir},%{_var}/log/mathopd}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mathopd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install src/mathopd $RPM_BUILD_ROOT%{_sbindir}

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
	/usr/sbin/useradd -u 51 -r -d /home/httpd -s /bin/false -c "HTTP User" -g http http 1>&2
fi

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/mathopd ]; then
	/etc/rc.d/init.d/mathopd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/mathopd start\" to start %{name} daemon."
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
	/usr/sbin/userdel http
	/usr/sbin/groupdel http
fi

%files
%defattr(644,root,root,755)
%doc [A-Z]* doc/*
%attr(755,root,root) %{_sbindir}/mathopd
%attr(-, http, http) /home/httpd/*
%attr(0755, root, root) /etc/rc.d/init.d/mathopd
%config %{_sysconfdir}/mathopd.conf
%attr(750,http,http) %dir %{_var}/log/mathopd
