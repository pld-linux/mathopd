Summary:	A fast, lightweighte, non-forking HTTP server for UN*X systems
Summary(pl.UTF-8):	Szybki, nieduży, nie forkujący się serwer HTTP
Name:		mathopd
Version:	1.5
Release:	6
License:	BSD
Group:		Networking
Source0:	http://www.mathopd.org/dist/%{name}-%{version}p3.tar.gz
# Source0-md5:	6e0fea187134cb52509c2f98a8644d11
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	http://www.mathopd.org/dist/dir_cgi.c.txt
URL:		http://www.mathopd.org/
Patch0:		%{name}-getline.patch
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	sh-utils
Provides:	group(http)
Provides:	user(http)
Provides:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_datadir	/home/services/httpd

%description
Mathopd is a very small, yet very fast HTTP server for UN*X systems.
Mathopd is designed specifically to handle a large number of
connections with minimal fuss. It contains no unnecessary add-ons, but
it does the trick for most things.

%description -l pl.UTF-8
Mathopd jest bardzo małym, bardzo szybkim serwerem HTTP dla systemów
uniksowych. Jest zaprojektowany specjalnie do obsługi dużej liczby
połączeń. Nie ma niepotrzebnych dodatków, ale potrafi większość
rzeczy.

%prep
%setup -q -n %{name}-%{version}p3
%patch -P0 -p1

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
%groupadd -g 51 -r -f http
%useradd -u 51 -r -d %{_datadir} -s /bin/false -c "HTTP User" -g http http

%post
/sbin/chkconfig --add %{name}
%service mathopd restart "%{name} HTTP daemon"

%preun
if [ "$1" = "0" ]; then
	%service mathopd stop
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mathopd.conf
%attr(750,http,http) %dir %{_var}/log/mathopd
