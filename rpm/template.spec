Name:           ros-kinetic-ecl-devices
Version:        0.61.13
Release:        0%{?dist}
Summary:        ROS ecl_devices package

Group:          Development/Libraries
License:        BSD
URL:            http://wiki.ros.org/ecl_devices
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-kinetic-ecl-config
Requires:       ros-kinetic-ecl-containers
Requires:       ros-kinetic-ecl-errors
Requires:       ros-kinetic-ecl-license
Requires:       ros-kinetic-ecl-mpl
Requires:       ros-kinetic-ecl-threads
Requires:       ros-kinetic-ecl-type-traits
Requires:       ros-kinetic-ecl-utilities
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-ecl-config
BuildRequires:  ros-kinetic-ecl-containers
BuildRequires:  ros-kinetic-ecl-errors
BuildRequires:  ros-kinetic-ecl-license
BuildRequires:  ros-kinetic-ecl-mpl
BuildRequires:  ros-kinetic-ecl-threads
BuildRequires:  ros-kinetic-ecl-type-traits
BuildRequires:  ros-kinetic-ecl-utilities

%description
Provides an extensible and standardised framework for input-output devices.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/kinetic" \
        -DCMAKE_PREFIX_PATH="/opt/ros/kinetic" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/kinetic

%changelog
* Thu Jun 16 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.13-0
- Autogenerated by Bloom

* Sun May 01 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.9-2
- Autogenerated by Bloom

* Sun May 01 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.9-1
- Autogenerated by Bloom

* Sat Apr 23 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.9-0
- Autogenerated by Bloom

