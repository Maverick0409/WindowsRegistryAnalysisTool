#-----------------------------------------------------------
# dhcpinformation.pl
# 

# 

package dhcpinformation;
use strict;

my %config = (hive          => "System",
              hasShortDescr => 1,
              hasDescr      => 0,
              hasRefs       => 0,
              osmask        => 22,
              version       => 20200525);

sub getConfig{return %config}
sub getShortDescr {
	return "Gets NIC info from System hive";	
}
sub getDescr{}
sub getRefs {}
sub getHive {return $config{hive};}
sub getVersion {return $config{version};}

my $VERSION = getVersion();

sub pluginmain {
	my %outputname = (DhcpIPAddress => "DHCP IP Address",
              DhcpSubnetMask => "DHCP Subnet Mask",
              DhcpServer => "DHCP Server IP",
              LeaseObtainedTime => "DHCP Lease Obtained Time",
              LeaseTerminatesTime => "DHCP Terminate Time",
              DhcpDefaultGateway => "DHCP Default Gateway");
	my $class = shift;
	my $hive = shift;
	my %nics;
	my $ccs;
	#::logMsg("Launching nic2 v.".$VERSION);
	#::rptMsg("nic2 v.".$VERSION); # banner
  #::rptMsg("(".getHive().") ".getShortDescr()."\n"); # banner
	my $reg = Parse::Win32Registry->new($hive);
	my $root_key = $reg->get_root_key;
# First thing to do is get the ControlSet00x marked current...this is
# going to be used over and over again in plugins that access the system
# file
	my $current;
	eval {
		$current = $root_key->get_subkey("Select")->get_value("Current")->get_data();
	};
	my @nics;
	my $key_path = "ControlSet00".$current."\\Services\\Tcpip\\Parameters\\Interfaces";
	my $key;
	if ($key = $root_key->get_subkey($key_path)) {
		my @guids = $key->get_list_of_subkeys();
		if (scalar @guids > 0) {
			foreach my $g (@guids) {
				::rptMsg(sprintf "%-28s|%-40s","Adapter",$g->get_name());
				::rptMsg(sprintf "%-28s|%-40s","Last Write Time",::getDateFromEpoch($g->get_timestamp()));
				eval {
					my @vals = $g->get_list_of_values();
					foreach my $v (@vals) {
						my $name = $v->get_name();
						my $data = $v->get_data();
						$data = ::getDateFromEpoch($data) if ($name eq "T1" || $name eq "T2");
						$data = ::getDateFromEpoch($data) if ($name =~ m/Time$/);
						$data = pack("h*",reverse $data) if (uc($name) eq uc("DhcpNetworkHint")); # SSID nibbles reversed //YK
						if(uc($name) ne uc("DhcpInterfaceOptions") & uc($name) ne uc("DhcpGatewayHardware") & uc($name) ne uc("Domain") & uc($name) ne uc("AddressType") & uc($name) ne uc("IsServerNapAware")& uc($name) ne uc("DhcpConnForceBroadcastFlag")& uc($name) ne uc("DhcpSubnetMaskOpt")& uc($name) ne uc("EnableDHCP")& uc($name) ne uc("NameServer")& uc($name) ne uc("Lease")& uc($name) ne uc("T1")& uc($name) ne uc("T2") & uc($name) ne uc("DhcpNameServer")& uc($name) ne uc("DhcpGatewayHardwareCount")& uc($name) ne uc("InterfaceMetric")& uc($name) ne uc("MTU")) {
							if($name eq "DhcpIPAddress" | $name eq "DhcpSubnetMask" | $name eq "DhcpServer" | $name eq "LeaseObtainedTime" | $name eq "LeaseTerminatesTime" | $name eq "DhcpDefaultGateway"){
							::rptMsg(sprintf "%-28s|%-40s",$outputname{$name},$data); }
							else{
							::rptMsg(sprintf "%-28s|%-40s",$name,$data); }
						};
					}
					#::rptMsg("");
				};
				# Parse subfolders having similar data for different wifi access points , key name is SSID (nibbles reversed) //YK
				my @ssids = $g->get_list_of_subkeys();
				if (scalar @ssids > 0) {
					foreach my $ssid (@ssids) {
						::rptMsg(sprintf "%-28s|%-40s","Adapter",$g->get_name()."/".$ssid->get_name());
						my $ssid_realname = pack("h*",reverse $ssid->get_name());
						::rptMsg(sprintf "%-28s|%-40s","SSID",$ssid_realname);
						::rptMsg(sprintf "%-28s|%-40s","Last write Time",::getDateFromEpoch($ssid->get_timestamp()));
						eval {
							my @vals = $ssid->get_list_of_values();
							foreach my $v (@vals) {
								my $name = $v->get_name();
								my $data = $v->get_data();
								$data = ::getDateFromEpoch($data) if ($name eq "T1" || $name eq "T2");
								$data = ::getDateFromEpoch($data) if ($name =~ m/Time$/);
								$data = pack("h*",reverse $data) if (uc($name) eq uc("DhcpNetworkHint"));
								if($name eq "DhcpIPAddress" | $name eq "DhcpSubnetMask" | $name eq "DhcpServer" | $name eq "LeaseObtainedTime" | $name eq "LeaseTerminatesTime" | $name eq "DhcpDefaultGateway"){
								::rptMsg(sprintf "%-28s|%-40s",$outputname{$name},$data) if(uc($name) ne uc("DhcpInterfaceOptions") & uc($name) ne uc("DhcpGatewayHardware") & uc($name) ne uc("Domain") & uc($name) ne uc("AddressType") & uc($name) ne uc("IsServerNapAware")& uc($name) ne uc("DhcpConnForceBroadcastFlag")& uc($name) ne uc("DhcpSubnetMaskOpt")& uc($name) ne uc("EnableDHCP")& uc($name) ne uc("NameServer")& uc($name) ne uc("Lease")& uc($name) ne uc("T1")& uc($name) ne uc("T2") & uc($name) ne uc("DhcpNameServer")& uc($name) ne uc("DhcpGatewayHardwareCount")& uc($name) ne uc("InterfaceMetric")& uc($name) ne uc("MTU"));}
								else{
									::rptMsg(sprintf "%-28s|%-40s",$name,$data) if(uc($name) ne uc("DhcpInterfaceOptions") & uc($name) ne uc("DhcpGatewayHardware") & uc($name) ne uc("Domain") & uc($name) ne uc("AddressType") & uc($name) ne uc("IsServerNapAware")& uc($name) ne uc("DhcpConnForceBroadcastFlag")& uc($name) ne uc("DhcpSubnetMaskOpt")& uc($name) ne uc("EnableDHCP")& uc($name) ne uc("NameServer")& uc($name) ne uc("Lease")& uc($name) ne uc("T1")& uc($name) ne uc("T2") & uc($name) ne uc("DhcpNameServer")& uc($name) ne uc("DhcpGatewayHardwareCount")& uc($name) ne uc("InterfaceMetric")& uc($name) ne uc("MTU"));}
							}
							#::rptMsg("");
						};
					}
				}
				else {
					#::rptMsg($key_path." has no subkeys.");
				}	
			}
		}
		else {
			#::rptMsg($key_path." has no subkeys.");
		}	
	}
	else {
		#::rptMsg($key_path." not found.");
	}
}
1;