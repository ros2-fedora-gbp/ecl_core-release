Name:           ros-indigo-ecl-core-apps
Version:        0.61.5
Release:        0%{?dist}
Summary:        ROS ecl_core_apps package

Group:          Development/Libraries
License:        BSD
URL:            http://wiki.ros.org/ecl_core_apps
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-ecl-build
Requires:       ros-indigo-ecl-command-line
Requires:       ros-indigo-ecl-config
Requires:       ros-indigo-ecl-containers
Requires:       ros-indigo-ecl-converters
Requires:       ros-indigo-ecl-devices
Requires:       ros-indigo-ecl-errors
Requires:       ros-indigo-ecl-exceptions
Requires:       ros-indigo-ecl-formatters
Requires:       ros-indigo-ecl-geometry
Requires:       ros-indigo-ecl-ipc
Requires:       ros-indigo-ecl-license
Requires:       ros-indigo-ecl-linear-algebra
Requires:       ros-indigo-ecl-sigslots
Requires:       ros-indigo-ecl-streams
Requires:       ros-indigo-ecl-threads
Requires:       ros-indigo-ecl-time-lite
Requires:       ros-indigo-ecl-type-traits
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-ecl-build
BuildRequires:  ros-indigo-ecl-command-line
BuildRequires:  ros-indigo-ecl-config
BuildRequires:  ros-indigo-ecl-containers
BuildRequires:  ros-indigo-ecl-converters
BuildRequires:  ros-indigo-ecl-devices
BuildRequires:  ros-indigo-ecl-errors
BuildRequires:  ros-indigo-ecl-exceptions
BuildRequires:  ros-indigo-ecl-formatters
BuildRequires:  ros-indigo-ecl-geometry
BuildRequires:  ros-indigo-ecl-ipc
BuildRequires:  ros-indigo-ecl-license
BuildRequires:  ros-indigo-ecl-linear-algebra
BuildRequires:  ros-indigo-ecl-sigslots
BuildRequires:  ros-indigo-ecl-streams
BuildRequires:  ros-indigo-ecl-threads
BuildRequires:  ros-indigo-ecl-time-lite
BuildRequires:  ros-indigo-ecl-type-traits

%description
This includes a suite of programs demo'ing various aspects of the ecl_core. It
also includes various benchmarking and utility programs for use primarily with
embedded systems.

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

