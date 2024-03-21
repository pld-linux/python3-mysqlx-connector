# TODO:
# - c extension build is done in install phase (http://bugs.mysql.com/bug.php?id=78621)
#
# Conditional build:
%bcond_with	tests		# build with tests (requires mysql server)

%define		pname	mysql-connector
Summary:	The MySQL Client/Protocol implemented in Python
Summary(pl.UTF-8):	Protokół kliencki MySQL zaimplementowany w Pythonie
Name:		python3-%{pname}
# check documentation to see which version is GA (we don't want devel releases)
# https://dev.mysql.com/downloads/connector/python/
Version:	8.0.33
Release:	1
License:	GPL v2
Group:		Libraries/Python
Source0:	http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-%{version}-src.tar.gz
# Source0-md5:	97b96f27a08aff863a7fb4a15c8bcdd7
#Source0:	https://pypi.debian.net/mysql-connector-python/mysql-connector-python-%{version}.tar.gz
Patch0:		force-capi.patch
Patch1:		tests.patch
Patch2:		build.patch
URL:		http://dev.mysql.com/doc/connector-python/en/
BuildRequires:	mysql8.0-devel
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
MySQL Connector/Python is implementing the MySQL Client/Server
protocol completely in Python. No MySQL libraries are needed, and no
compilation is necessary to run this Python DB API v2.0 compliant
driver.

%description -l pl.UTF-8
MySQL Connector/Python to protokół klient-serwer MySQL-a
zaimplementowany całkowicie w Pythonie. Do uruchomienia tego
sterownika, zgodnego z DB API v2.0 Pythona, nie są potrzebne
biblioteki MySQL-a, ani żadna kompilacja.

%prep
%setup -q -n mysql-connector-python-%{version}-src
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export MYSQLXPB_PROTOC=%{_bindir}/protoc
export MYSQLXPB_PROTOBUF_INCLUDE_DIR=%{_includedir}
export MYSQLXPB_PROTOBUF_LIB_DIR=%{_libdir}

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

%install
rm -rf $RPM_BUILD_ROOT

# see NOTE on beginning of the spec
export MYSQLXPB_PROTOC=%{_bindir}/protoc
export MYSQLXPB_PROTOBUF_INCLUDE_DIR=%{_includedir}
export MYSQLXPB_PROTOBUF_LIB_DIR=%{_libdir}

%py3_install \
	--with-mysql-capi=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt
%attr(755,root,root) %{py3_sitedir}/_mysql_connector.cpython-*.so
%{py3_sitedir}/mysql*.egg-info
%dir %{py3_sitedir}/mysql
%{py3_sitedir}/mysql/*.py
%dir %{py3_sitedir}/mysql/__pycache__
%{py3_sitedir}/mysql/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector
%{py3_sitedir}/mysql/connector/py.typed
%{py3_sitedir}/mysql/connector/*.py
%dir %{py3_sitedir}/mysql/connector/__pycache__
%{py3_sitedir}/mysql/connector/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector/django
%{py3_sitedir}/mysql/connector/django/*.py
%dir %{py3_sitedir}/mysql/connector/django/__pycache__
%{py3_sitedir}/mysql/connector/django/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector/locales
%{py3_sitedir}/mysql/connector/locales/*.py
%dir %{py3_sitedir}/mysql/connector/locales/__pycache__
%{py3_sitedir}/mysql/connector/locales/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector/locales/eng
%{py3_sitedir}/mysql/connector/locales/eng/*.py
%dir %{py3_sitedir}/mysql/connector/locales/eng/__pycache__
%{py3_sitedir}/mysql/connector/locales/eng/__pycache__/*.py[co]
%{py3_sitedir}/mysql/connector/plugins
%dir %{py3_sitedir}/mysqlx
%{py3_sitedir}/mysqlx/py.typed
%{py3_sitedir}/mysqlx/*.py
%dir %{py3_sitedir}/mysqlx/__pycache__
%{py3_sitedir}/mysqlx/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysqlx/locales
%{py3_sitedir}/mysqlx/locales/*.py
%dir %{py3_sitedir}/mysqlx/locales/__pycache__
%{py3_sitedir}/mysqlx/locales/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysqlx/locales/eng
%{py3_sitedir}/mysqlx/locales/eng/*.py
%dir %{py3_sitedir}/mysqlx/locales/eng/__pycache__
%{py3_sitedir}/mysqlx/locales/eng/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysqlx/protobuf
%{py3_sitedir}/mysqlx/protobuf/*.py
%dir %{py3_sitedir}/mysqlx/protobuf/__pycache__
%{py3_sitedir}/mysqlx/protobuf/__pycache__/*.py[co]
