#-----------------------------------------------------------
# windowsversion.pl
#


package windowsversion;
use strict;

my %config = (hive          => "Software",
              osmask        => 22,
              hasShortDescr => 1,
              hasDescr      => 0,
              hasRefs       => 0,
              version       => 20200525);

sub getConfig{return %config}

sub getShortDescr {
	return "Get Windows version & build info";	
}
sub getDescr{}
sub getRefs {}
sub getHive {return $config{hive};}
sub getVersion {return $config{version};}

my $VERSION = getVersion();

sub pluginmain {
	my $class = shift;
	my $hive = shift;
	#::logMsg("Launching winver v.".$VERSION);
	#::rptMsg("winver v.".$VERSION); 
  #::rptMsg("(".getHive().") ".getShortDescr()."\n"); 
  
  
  my %vals = (1 => "ProductName",
              #2 => "ReleaseID",
              #3 => "CSDVersion",
              #4 => "BuildLab",
              2 => "BuildLabEx",
              3 => "CompositionEditionID",
              #7 => "RegisteredOrganization",
              4 => "RegisteredOwner");
   my %vals1 = (1 => "Product Name",
              #2 => "ReleaseID",
              #3 => "CSDVersion",
              #4 => "BuildLab",
              2 => "Release Version",
              3 => "Composition Edition ID",
              #7 => "RegisteredOrganization",
              4 => "Registered Owner");
	my $reg = Parse::Win32Registry->new($hive);
	my $root_key = $reg->get_root_key;
	my $key_path = "Microsoft\\Windows NT\\CurrentVersion";
	my $key;
	if ($key = $root_key->get_subkey($key_path)) {
		
		foreach my $v (sort {$a <=> $b} keys %vals) {
			
			eval {
				my $i = $key->get_value($vals{$v})->get_data();
				::rptMsg(sprintf "%-25s|%-20s",$vals1{$v},$i);
			};
		}
		
		eval {
			my $install = $key->get_value("InstallDate")->get_data();
			::rptMsg(sprintf "%-25s|%-20s","OS Install Date",::getDateFromEpoch($install));
		};
	
		eval {
			my $it = $key->get_value("InstallTime")->get_data();
			my ($t0,$t1) = unpack("VV",$it);
			my $t = ::getTime($t0,$t1);
			#::rptMsg(sprintf "%-25s %-20s","Install Time|",::getDateFromEpoch($t));
		};
		
	}
	else {
		#::rptMsg($key_path." not found.");
	}
}
1;