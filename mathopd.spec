Summary:	A fast, lightweighte, non-forking HTTP server for UN*X systems
Summary(pl):	Szybki, niedu�y, nie forkuj�cy si� serwer HTTP
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
Requires(pre):	user-http
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mathopd is a very small, yet very fast HTTP server for UN*X systems.
Mathopd is designed specifically to handle a large number of
connections with minimal fuss. It contains no unnecessary add-ons, but
it does the trick for most things.

%description -l pl
Mathopd jest bardzo ma�ym, bardzo szybkim serwerem HTTP dla system�w
uniksowych. Jest zaprojektowany specjalnie do obs�ugi du�ej liczby
po��cze�. Nie ma niepotrzebnych dodatk�w, ale potrafi wi�kszo��
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

%files
%defattr(644,root,root,755)
%doc [A-Z]* doc/*
%attr(755,root,root) %{_sbindir}/mathopd
%attr(-, http, http) /home/httpd/*
%attr(0755, root, root) /etc/rc.d/init.d/mathopd
%config %{_sysconfdir}/mathopd.conf
%attr(750,http,http) %dir %{_var}/log/mathopd
