%define snapshot git20100101

%define	rname	network-manager-applet
Name:		networkmanager-applet
Summary:	Network connection manager applet for GNOME
Version:	0.7.997
Release:	%mkrel 0.%{snapshot}.1
Group:		System/Configuration/Networking
License:	GPLv2+
URL:		http://www.gnome.org/projects/NetworkManager/
Source0:	network-manager-applet-%{version}.%{snapshot}.tar.xz
BuildRequires:	intltool
BuildRequires:	libnm-glib-devel
BuildRequires:	libnm-glib-vpn-devel
BuildRequires:	libGConf2-devel
BuildRequires:	libglade2-devel
BuildRequires:	libgnome-keyring-devel
#BuildRequires:	gnome-bluetooth-devel
BuildRequires:	libiw-devel
BuildRequires:	libnotify-devel
BuildRequires:	polkit-1-devel
Requires:	networkmanager
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Network-manager-applet is a system tray applet which lets you easily
connect to different networks. It is created for GNOME's notification area
but it also works for other desktop environments which provide a system
tray like KDE or XFCE. It displays the available networks and allows to
easily switch between them. For encrypted networks it will prompt the user
for the key/passphrase and it can optionally store them in the
gnome-keyring.

%prep
%setup -q -n %{rname}-%{version}

%build
autoreconf -fis
%configure2_5x	--disable-static \
		--enable-more-warnings=yes 
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang nm-applet

%clean
rm -rf %{buildroot}

%files -f nm-applet.lang
%defattr(-,root,root)
%doc ChangeLog CONTRIBUTING
%{_bindir}/nm-connection-editor
%{_bindir}/nm-applet
%{_datadir}/applications/nm-connection-editor.desktop
%{_iconsdir}/hicolor/*/apps/*
%dir %{_datadir}/nm-applet/
%{_datadir}/nm-applet/*.glade
%{_datadir}/nm-applet/*.png
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_sysconfdir}/dbus-1/system.d/nm-applet.conf
%{_sysconfdir}/gconf/schemas/nm-applet.schemas

