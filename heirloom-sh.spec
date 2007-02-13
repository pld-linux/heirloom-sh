#
# Conditional build:
%bcond_without	static	# don't build static version of jsh
#
%define snap	050706
Summary:	The Heirloom Bourne Shell
Summary(pl.UTF-8):	Powłoka Heirloom Bourne Shell
Name:		heirloom-sh
Version:	0.1
Release:	0.%{snap}.1
License:	CCDL
Group:		Applications/Shells
Source0:	http://dl.sourceforge.net/heirloom/%{name}-%{snap}.tar.bz2
# Source0-md5:	9169d9b3b845cb63c598ea29b8d2dfa0
URL:		http://heirloom.sourceforge.net/sh.html
%{?with_static:BuildRequires:	glibc-static}
Requires(preun):	sed >= 4.1.5-1.2
Requires:	setup >= 2.4.6-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix		/
%define		_bindir			/bin

%description
The Heirloom Bourne Shell is a portable variant of the traditional
Unix shell. It has been derived from OpenSolaris code and thus
implements the SVR4/SVID3 level of the shell.

%description -l pl.UTF-8
Heirloom Bourne Shell to przenośna wersja tradycyjnej powłoki
uniksowej. Wywodzi się z kodu OpenSolarisa, więc implementuje powłokę
poziomu SVR4/SVID3.

%package static
Summary:	Statically linked Heirloom Bourne Shell
Summary(pl.UTF-8):	Statycznie zlinkowana powłoka Heirloom Bourne Shell
Group:		Applications/Shells
Requires(preun):	sed >= 4.1.5-1.2
Requires:	%{name} = %{version}-%{release}

%description static
The Heirloom Bourne Shell is a portable variant of the traditional
Unix shell. It has been derived from OpenSolaris code and thus
implements the SVR4/SVID3 level of the shell.

This packege contains statically linked version of Heirloom Bourne
Shell.

%description static -l pl.UTF-8
Heirloom Bourne Shell to przenośna wersja tradycyjnej powłoki
uniksowej. Wywodzi się z kodu OpenSolarisa, więc implementuje powłokę
poziomu SVR4/SVID3.

Ten pakiet zawiera statycznie zlinkowaną wersję powłoki Heirloom
Bourne Shell.

%prep
%setup  -q -n %{name}-%{snap}

%build
%if %{with static}
%{__make} \
	DEFBIN=%{_bindir} \
	SV3BIN=%{_bindir} \
	MANDIR=%{_mandir} \
	CC="%{__cc}" \
	CFLAGS="-static %{rpmcflags}" \
	LNS="ln" \
	UCBINST=install
mv jsh jsh.static
%endif

%{__make} \
	DEFBIN=%{_bindir} \
	SV3BIN=%{_bindir} \
	MANDIR=%{_mandir} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LNS="ln" \
	UCBINST=install

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	DEFBIN=%{_bindir} \
	SV3BIN=%{_bindir} \
	MANDIR=%{_mandir} \
	LNS="ln" \
	UCBINST=install

%if %{with static}
install jsh.static $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shells ]; then
	umask 022
	echo "%{_bindir}/jsh" > /etc/shells
else
	while read SHNAME; do
		if [ "$SHNAME" = "%{_bindir}/jsh" ]; then
			HAS_KSH=1
		fi
	done < /etc/shells
	[ -n "$HAS_KSH" ] || echo "%{_bindir}/jsh" >> /etc/shells
fi

%preun
if [ "$1" = "0" ]; then
	%{__sed} -i -e '
		/^\/bin\/jsh$/d
	' /etc/shells
fi

%post static
if [ ! -f /etc/shells ]; then
	umask 022
	echo "%{_bindir}/jsh.static" > /etc/shells
else
	while read SHNAME; do
	if [ "$SHNAME" = "%{_bindir}/jsh.static" ]; then
		HAS_KSH_STATIC=1
	fi
	done < /etc/shells
	[ -n "$HAS_KSH_STATIC" ] || echo "%{_bindir}/jsh.static" >> /etc/shells
fi

%preun static
if [ "$1" = "0" ]; then
	%{__sed} -i -e '
		/^\/bin\/jsh\.static$/d
	' /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc *.LICENSE CHANGES README
%attr(755,root,root) %{_bindir}/jsh
%{_mandir}/man1/jsh*

%if %{with static}
%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jsh.static
%endif
