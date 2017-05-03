#
# Conditional build:
%bcond_with	tests		# build without tests

%define		php_min_version 5.3.3
Summary:	Handle HHVM/PHP environments
Name:		php-sebastian-environment
Version:	1.3.8
Release:	1
License:	BSD
Group:		Development/Libraries
Source0:	https://github.com/sebastianbergmann/environment/archive/%{version}/environment-%{version}.tar.gz
# Source0-md5:	a14fe7826a2801de5151d23a065aad33
URL:		https://github.com/sebastianbergmann/environment
BuildRequires:	php(core) >= %{php_min_version}
BuildRequires:	phpab
%if %{with tests}
BuildRequires:	phpunit >= 4.8
%endif
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
Requires:	php(posix)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This component provides functionality that helps writing PHP code that
has runtime-specific (PHP / HHVM) execution paths.

%prep
%setup -q -n environment-%{version}

# Restore PSR-0 tree
install -d SebastianBergmann
mv src SebastianBergmann/Environment

%build
# Generate the Autoloader
phpab \
	--output SebastianBergmann/Environment/autoload.php \
	SebastianBergmann/Environment

%if %{with tests}
: Run tests - set include_path to ensure PHPUnit autoloader use it
phpunit --bootstrap SebastianBergmann/Environment/autoload.php
%endif


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_data_dir}/SebastianBergmann
cp -a SebastianBergmann/Environment $RPM_BUILD_ROOT%{php_data_dir}/SebastianBergmann/Environment

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE composer.json
%dir %{php_data_dir}/SebastianBergmann
%{php_data_dir}/SebastianBergmann/Environment
