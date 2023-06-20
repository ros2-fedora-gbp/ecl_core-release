%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-ecl-containers
Version:        1.2.1
Release:        3%{?dist}%{?release_suffix}
Summary:        ROS ecl_containers package

License:        BSD
URL:            http://wiki.ros.org/ecl_containers
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-rolling-ecl-config
Requires:       ros-rolling-ecl-converters
Requires:       ros-rolling-ecl-errors
Requires:       ros-rolling-ecl-exceptions
Requires:       ros-rolling-ecl-formatters
Requires:       ros-rolling-ecl-license
Requires:       ros-rolling-ecl-mpl
Requires:       ros-rolling-ecl-type-traits
Requires:       ros-rolling-ecl-utilities
Requires:       ros-rolling-ros-workspace
BuildRequires:  ros-rolling-ament-cmake-ros
BuildRequires:  ros-rolling-ecl-build
BuildRequires:  ros-rolling-ecl-config
BuildRequires:  ros-rolling-ecl-converters
BuildRequires:  ros-rolling-ecl-errors
BuildRequires:  ros-rolling-ecl-exceptions
BuildRequires:  ros-rolling-ecl-formatters
BuildRequires:  ros-rolling-ecl-license
BuildRequires:  ros-rolling-ecl-mpl
BuildRequires:  ros-rolling-ecl-type-traits
BuildRequires:  ros-rolling-ecl-utilities
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-cmake-gtest
BuildRequires:  ros-rolling-ament-lint-auto
BuildRequires:  ros-rolling-ament-lint-common
%endif

%description
The containers included here are intended to extend the stl containers. In all
cases, these implementations are designed to implement c++ conveniences and
safety where speed is not sacrificed. Also includes techniques for memory
debugging of common problems such as buffer overruns.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Tue Jun 20 2023 Daniel Stonier <d.stonier@gmail.com> - 1.2.1-3
- Autogenerated by Bloom
