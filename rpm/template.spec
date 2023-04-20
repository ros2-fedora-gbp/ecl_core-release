%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-ecl-core
Version:        1.2.1
Release:        4%{?dist}%{?release_suffix}
Summary:        ROS ecl_core package

License:        BSD
URL:            http://www.ros.org/wiki/ecl_core
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-iron-ecl-command-line
Requires:       ros-iron-ecl-concepts
Requires:       ros-iron-ecl-containers
Requires:       ros-iron-ecl-converters
Requires:       ros-iron-ecl-core-apps
Requires:       ros-iron-ecl-devices
Requires:       ros-iron-ecl-eigen
Requires:       ros-iron-ecl-exceptions
Requires:       ros-iron-ecl-formatters
Requires:       ros-iron-ecl-geometry
Requires:       ros-iron-ecl-ipc
Requires:       ros-iron-ecl-linear-algebra
Requires:       ros-iron-ecl-math
Requires:       ros-iron-ecl-mpl
Requires:       ros-iron-ecl-sigslots
Requires:       ros-iron-ecl-statistics
Requires:       ros-iron-ecl-streams
Requires:       ros-iron-ecl-threads
Requires:       ros-iron-ecl-time
Requires:       ros-iron-ecl-type-traits
Requires:       ros-iron-ecl-utilities
Requires:       ros-iron-ros-workspace
BuildRequires:  ros-iron-ament-cmake-ros
BuildRequires:  ros-iron-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
A set of tools and interfaces extending the capabilities of c++ to provide a
lightweight, consistent interface with a focus for control programming.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/iron" \
    -DAMENT_PREFIX_PATH="/opt/ros/iron" \
    -DCMAKE_PREFIX_PATH="/opt/ros/iron" \
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
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/iron

%changelog
* Thu Apr 20 2023 Daniel Stonier <d.stonier@gmail.com> - 1.2.1-4
- Autogenerated by Bloom

* Tue Mar 21 2023 Daniel Stonier <d.stonier@gmail.com> - 1.2.1-3
- Autogenerated by Bloom

