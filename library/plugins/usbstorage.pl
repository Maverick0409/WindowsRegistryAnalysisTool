#-----------------------------------------------------------
# usbstorage
#
package usbstorage;
use strict;

my %config = (hive          => "System",
              osmask        => 22,
              hasShortDescr => 1,
              hasDescr      => 0,
              hasRefs       => 0,
              version       => 20200515);

sub getConfig{return %config}

sub getShortDescr {
	return "Get USBStor key info";	
}
sub getDescr{}
sub getRefs {}
sub getHive {return $config{hive};}
sub getVersion {return $config{version};}

my $VERSION = getVersion();

sub pluginmain {
	my $class = shift;
	my $hive = shift;
	#::logMsg("Launching usbstor v.".$VERSION);
	#::rptMsg("usbstor v.".$VERSION); 
  #::rptMsg("(".getHive().") ".getShortDescr()."\n"); 
	my $reg = Parse::Win32Registry->new($hive);
	my $root_key = $reg->get_root_key;

# Code for System file, getting CurrentControlSet
	my $current;
	my $ccs;
	my $key_path = 'Select';
	my $key;
	if ($key = $root_key->get_subkey($key_path)) {
		$current = $key->get_value("Current")->get_data();
		$ccs = "ControlSet00".$current;
	}
	else {
		#::rptMsg($key_path." not found.");
		return;
	}

	my $key_path = $ccs."\\Enum\\USBStor";
	my $key;
	if ($key = $root_key->get_subkey($key_path)) {
		#::rptMsg("USBStor");
		#::rptMsg($key_path);
		#::rptMsg("");
		
		my @subkeys = $key->get_list_of_subkeys();
		if (scalar(@subkeys) > 0) {
			foreach my $s (@subkeys) {
				#::rptMsg($s->get_name()." [".::getDateFromEpoch($s->get_timestamp())."]");
				::rptMsg(sprintf "%-25s|%-30s","USB Device Name",$s->get_name());
				
				
				my @sk = $s->get_list_of_subkeys();
				if (scalar(@sk) > 0) {
					foreach my $k (@sk) {
						my $serial = $k->get_name();
						::rptMsg(sprintf "%-25s|%-30s","USB Serial Number",$serial);
# added 20141015; updated 20141111						
						eval {
							#::rptMsg(sprintf "%-30s %-30s","Device Parameters Date Time |".::getDateFromEpoch($k->get_subkey("Device Parameters")->get_timestamp()));
						};
						eval {
							#::rptMsg("  LogConf LastWrite          : [".::getDateFromEpoch($k->get_subkey("LogConf")->get_timestamp())."Z]");
						};
						eval {
							#::rptMsg("  Properties LastWrite       : [".::getDateFromEpoch($k->get_subkey("Properties")->get_timestamp())."Z]");
						};
						my $friendly;
						eval {
							$friendly = $k->get_value("FriendlyName")->get_data();
						};
					::rptMsg(sprintf "%-25s|%-30s","USB Device Friendly Name",$friendly) if ($friendly ne "N/A");
						my $parent;
						eval {
							$parent = $k->get_value("ParentIdPrefix")->get_data();
						};
						#::rptMsg("    ParentIdPrefix: ".$parent) if ($parent ne "");
# Attempt to retrieve InstallDate/FirstInstallDate from Properties subkeys	
# http://studioshorts.com/blog/2012/10/windows-8-device-property-ids-device-enumeration-pnpobject/		
# https://www.swiftforensics.com/2013/11/windows-8-new-registry-artifacts-part-1.html			
						my $t;
						eval {
							$t = $k->get_subkey("Properties\\{83da6326-97a6-4088-9453-a1923f573b29}\\0064")->get_value("")->get_data();
							my ($t0,$t1) = unpack("VV",$t);
							::rptMsg(sprintf "%-25s|%-30s","First Install Date",::getDateFromEpoch(::getTime($t0,$t1)));
						};
						
						eval {
							$t = $k->get_subkey("Properties\\{83da6326-97a6-4088-9453-a1923f573b29}\\0065")->get_value("")->get_data();
							my ($t0,$t1) = unpack("VV",$t);
							#::rptMsg("    InstallDate           : ".::getDateFromEpoch(::getTime($t0,$t1))."Z");
						};
						
						eval {
							$t = $k->get_subkey("Properties\\{83da6326-97a6-4088-9453-a1923f573b29}\\0066")->get_value("")->get_data();
							my ($t0,$t1) = unpack("VV",$t);
						::rptMsg(sprintf "%-25s|%-30s","Last Arrival Date",::getDateFromEpoch(::getTime($t0,$t1)));
						};
						
						eval {
							$t = $k->get_subkey("Properties\\{83da6326-97a6-4088-9453-a1923f573b29}\\0067")->get_value("")->get_data();
							my ($t0,$t1) = unpack("VV",$t);
							#::rptMsg(sprintf "%-30s %-30s","Last Removal Date Time |".::getDateFromEpoch(::getTime($t0,$t1)));
						};
						
					}					
				}
				#::rptMsg("");
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