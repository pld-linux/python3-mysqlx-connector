# TODO:
# - c extension build is done in install phase (http://bugs.mysql.com/bug.php?id=78621)
#
# Conditional build:
%bcond_with	tests		# build with tests (requires mysql server)

%ifarch %{x8664}
%define     mysql_ver   8.4
%else
%define     mysql_ver   8.0
%endif

%define		pname	mysqlx-connector
Summary:	The MySQL Client/Protocol implemented in Python
Summary(pl.UTF-8):	Protokół kliencki MySQL zaimplementowany w Pythonie
Name:		python3-%{pname}
# check documentation to see which version is GA (we don't want devel releases)
# https://dev.mysql.com/downloads/connector/python/
Version:	9.3.0
Release:	5
License:	GPL v2
Group:		Libraries/Python
Source0:	http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-%{version}-src.tar.gz
# Source0-md5:	b054e1caacdedeb76060793683ff3fae
#Source0:	https://pypi.debian.net/mysql-connector-python/mysql-connector-python-%{version}.tar.gz
Patch0:		force-capi.patch
Patch1:		tests.patch
Patch2:		protobuf.patch
URL:		http://dev.mysql.com/doc/connector-python/en/
BuildRequires:	mysql%{mysql_ver}-devel
BuildRequires:	protobuf-devel >= 3.0.0
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	mysql
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQLX Connector/Python is implementing the the MySQL X DevAPI protocol.

%description -l pl.UTF-8
MySQLX Connector/Python to implementacja protokołu MySQL X DevAPI.

%prep
%setup -q -n mysql-connector-python-%{version}-src
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
export MYSQL_CAPI=%{_bindir}/mysql_config%{mysql_ver}

cd mysqlx-connector-python

%py3_build
%if %{with tests}
export PYTHONPATH="$(pwd)/$(echo build-3/lib*)"
%{__python3} unittests.py \
	--verbosity 1 \
	--keep --stats \
	--skip-install \
	--with-mysql=%{_prefix} \
	--with-mysql-share=%{_datadir}/mysql
%endif

cd ..

%install
rm -rf $RPM_BUILD_ROOT

# see NOTE on beginning of the spec
export PROTOC=%{_bindir}/protoc
export PROTOBUF_INCLUDE_DIR=%{_includedir}
export PROTOBUF_LIB_DIR=%{_libdir}

export MYSQLXPB_PROTOC=%{_bindir}/protoc
export MYSQLXPB_PROTOBUF_INCLUDE_DIR=%{_includedir}
export MYSQLXPB_PROTOBUF_LIB_DIR=%{_libdir}

export MYSQL_CAPI=%{_bindir}/mysql_config%{mysql_ver}

cd mysqlx-connector-python
%py3_install
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt
%attr(755,root,root) %{py3_sitedir}/_mysqlxpb.cpython-*.so
%{py3_sitedir}/mysqlx*.egg-info
%{py3_sitedir}/mysqlx
