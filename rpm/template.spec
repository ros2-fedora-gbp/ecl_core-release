Name:           ros-kinetic-ecl-streams
Version:        0.61.17
Release:        0%{?dist}
Summary:        ROS ecl_streams package

Group:          Development/Libraries
License:        BSD
URL:            http://wiki.ros.org/ecl_streams
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-kinetic-ecl-concepts
Requires:       ros-kinetic-ecl-converters
Requires:       ros-kinetic-ecl-devices
Requires:       ros-kinetic-ecl-errors
Requires:       ros-kinetic-ecl-license
Requires:       ros-kinetic-ecl-time
Requires:       ros-kinetic-ecl-type-traits
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-ecl-concepts
BuildRequires:  ros-kinetic-ecl-converters
BuildRequires:  ros-kinetic-ecl-devices
BuildRequires:  ros-kinetic-ecl-errors
BuildRequires:  ros-kinetic-ecl-license
BuildRequires:  ros-kinetic-ecl-time
BuildRequires:  ros-kinetic-ecl-type-traits

%description
These are lightweight text streaming classes that connect to standardised ecl
type devices.

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
* Sun Feb 05 2017 Daniel Stonier <d.stonier@gmail.com> - 0.61.17-0
- Autogenerated by Bloom

* Wed Nov 09 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.15-0
- Autogenerated by Bloom

* Thu Jun 16 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.14-0
- Autogenerated by Bloom

* Thu Jun 16 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.13-0
- Autogenerated by Bloom

* Sun May 01 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.9-2
- Autogenerated by Bloom

* Sun May 01 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.9-1
- Autogenerated by Bloom

* Sat Apr 23 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.9-0
- Autogenerated by Bloom

