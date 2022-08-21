#-----------------------------------------------------------
# installedapplications.pl
# Gets contents of Uninstall key from Software hive; sorts 
# display names based on key LastWrite time

package installedapplications;
use strict;

my %config = (hive          => "Software, NTUSER\.DAT",
              osmask        => 22,
              hasShortDescr => 1,
              hasDescr      => 0,
              hasRefs       => 0,
              version       => 20200525);

sub getConfig{return %config}

sub getShortDescr {
	return "Gets contents of Uninstall keys from Software, NTUSER\.DAT hives";	
}
sub getDescr{}
sub getRefs {}
sub getHive {return $config{hive};}
sub getVersion {return $config{version};}

my $VERSION = getVersion();

sub pluginmain {
	my $class = shift;
	my $hive = shift;
	#::logMsg("Launching uninstall v.".$VERSION);
	#::rptMsg("uninstall v.".$VERSION); # banner
    #::rptMsg("(".getHive().") ".getShortDescr()."\n"); # banner
	my @keys = ('Microsoft\\Windows\\CurrentVersion\\Uninstall',
	            'Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall',
	            'Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall',                  # NTUSER.DAT
	            'Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall');    # NTUSER.DAT
	
	my $reg = Parse::Win32Registry->new($hive);
	my $root_key = $reg->get_root_key;
	#::rptMsg("Uninstall");
	foreach my $key_path (@keys) {
		my $key;
		if ($key = $root_key->get_subkey($key_path)) {
			
			#::rptMsg($key_path);
			#::rptMsg("");
		
			my %uninst;
			my @subkeys = $key->get_list_of_subkeys();
	 		if (scalar(@subkeys) > 0) {
	 			foreach my $s (@subkeys) {
	 				my $lastwrite = $s->get_timestamp();
	 				my $display;
	 				eval {
	 					$display = $s->get_value("DisplayName")->get_data();
	 				};
	 				$display = $s->get_name() if ($display eq "");
	 			
	 				my $ver;
	 				eval {
	 					$ver = $s->get_value("DisplayVersion")->get_data();
	 				};
	 				$display .= " v\.".$ver unless ($@);
	 			
	 				push(@{$uninst{$lastwrite}},$display);
	 			}
	 			foreach my $t (reverse sort {$a <=> $b} keys %uninst) {
					#::rptMsg(::getDateFromEpoch($t)."Z");
					foreach my $item (@{$uninst{$t}}) {
						#::rptMsg("  ".$item);
						::rptMsg(::getDateFromEpoch($t)."|".$item);
					}
					#::rptMsg("");
				}
	 		}
	 		else {
	 			#::rptMsg($key_path." has no subkeys.");
	 		}
		}
		else {
#			::rptMsg($key_path." not found.");
		}
	}
}
1;