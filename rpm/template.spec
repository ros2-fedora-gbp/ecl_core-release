Name:           ros-indigo-ecl-streams
Version:        0.61.8
Release:        0%{?dist}
Summary:        ROS ecl_streams package

Group:          Development/Libraries
License:        BSD
URL:            http://wiki.ros.org/ecl_streams
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-ecl-concepts
Requires:       ros-indigo-ecl-converters
Requires:       ros-indigo-ecl-devices
Requires:       ros-indigo-ecl-errors
Requires:       ros-indigo-ecl-license
Requires:       ros-indigo-ecl-time
Requires:       ros-indigo-ecl-type-traits
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-ecl-concepts
BuildRequires:  ros-indigo-ecl-converters
BuildRequires:  ros-indigo-ecl-devices
BuildRequires:  ros-indigo-ecl-errors
BuildRequires:  ros-indigo-ecl-license
BuildRequires:  ros-indigo-ecl-time
BuildRequires:  ros-indigo-ecl-type-traits

%description
These are lightweight text streaming classes that connect to standardised ecl
type devices.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Sun Jan 10 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.8-0
- Autogenerated by Bloom

* Sat Jan 09 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.7-0
- Autogenerated by Bloom

* Wed Jan 06 2016 Daniel Stonier <d.stonier@gmail.com> - 0.61.6-1
- Autogenerated by Bloom

* Tue Nov 24 2015 Daniel Stonier <d.stonier@gmail.com> - 0.61.5-0
- Autogenerated by Bloom

* Sat Oct 10 2015 Daniel Stonier <d.stonier@gmail.com> - 0.61.4-0
- Autogenerated by Bloom

* Sat Sep 05 2015 Daniel Stonier <d.stonier@gmail.com> - 0.61.3-0
- Autogenerated by Bloom

* Wed Aug 12 2015 Daniel Stonier <d.stonier@gmail.com> - 0.61.2-0
- Autogenerated by Bloom

* Wed Jul 22 2015 Daniel Stonier <d.stonier@gmail.com> - 0.61.1-0
- Autogenerated by Bloom

