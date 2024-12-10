Name:		waagent
Version:	2.12.0.4
Release:	1
URL:		https://learn.microsoft.com/en-us/azure/virtual-machines/extensions/agent-linux
Source0:	https://github.com/Azure/WALinuxAgent/archive/refs/tags/v%{version}.tar.gz
Patch0:		https://github.com/berolinux/WALinuxAgent/commit/84bfbe4b36eb4564a99c705b68f817f668b83546.patch
Group:		Servers
License:	Apache-2.0
Summary:	Provisioning agent for running inside Azure
Requires:	openssh
Requires:	util-linux
Requires:	parted
Requires:	sed
Requires:	grep
Requires:	iproute2
BuildRequires:	python
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(distro)
BuildArch:	noarch

%description
The Microsoft Azure Linux Agent (waagent) manages Linux provisioning and VM
interaction with the Azure Fabric Controller. It provides the following
functionality for Linux IaaS deployments:

Image Provisioning
* Creation of a user account
* Configuring SSH authentication types
* Deployment of SSH public keys and key pairs
* Setting the host name
* Publishing the host name to the platform DNS
* Reporting SSH host key fingerprint to the platform
* Resource Disk Management
* Formatting and mounting the resource disk
* Configuring swap space

Networking
* Manages routes to improve compatibility with platform DHCP servers
* Ensures the stability of the network interface name

Kernel
* Configure virtual NUMA (disable for kernel <2.6.37)
* Configure SCSI timeouts for the root device (which could be remote)

Diagnostics
* Console redirection to the serial port

SCVMM Deployments
* Detect and bootstrap the VMM agent for Linux when running in a System Center
  Virtual Machine Manager 2012R2 environment

VM Extension
* Inject component authored by Microsoft and Partners into Linux VM (IaaS) to
  enable software and configuration automation
* VM Extension reference implementation on GitHub

Communication
The information flow from the platform to the agent occurs via two channels:

A boot-time attached DVD for IaaS deployments. This DVD includes an
OVF-compliant configuration file that includes all provisioning information
other than the actual SSH keypairs.

A TCP endpoint exposing a REST API used to obtain deployment and topology
configuration.

The agent will use an HTTP proxy if provided via the http_proxy (for http
requests) or https_proxy (for https requests) environment variables. The
HttpProxy.Host and HttpProxy.Port configuration variables (see below), if used,
will override the environment settings. Due to limitations of Python, the agent
does not support HTTP proxies requiring authentication.

%prep
%autosetup -p1 -n WALinuxAgent-%{version}

%build
%py_build

%install
%py_install
#%if "%{_sbindir}" != "%{_prefix}/sbin"
#mv %{buildroot}%{_prefix}/sbin %{buildroot}%{_sbindir}
#%endif

%files
%{py_puresitedir}/azurelinuxagent
%{py_puresitedir}/WALinuxAgent*.egg-info
%{_sbindir}/waagent*
%{_unitdir}/waagent.service
%{_sysconfdir}/logrotate.d/waagent.logrotate
%{_sysconfdir}/udev/rules.d/99-azure-product-uuid.rules
%{_sysconfdir}/udev/rules.d/66-azure-storage.rules
%{_sysconfdir}/waagent.conf
