#-----------------------------------------------------------
# recentdocuments.pl
# Plugin for Registry Ripper 
# Parses RecentDocs keys/values in NTUSER.DAT 
#

package recentdocuments;
use strict;
use Encode;

my %config = (hive          => "NTUSER\.DAT",
              hasShortDescr => 1,
              hasDescr      => 0,
              hasRefs       => 0,
              osmask        => 22,
              version       => 20200427);

sub getShortDescr {
	return "Gets contents of user's RecentDocs key";	
}
sub getDescr{}
sub getRefs {}
sub getHive {return $config{hive};}
sub getVersion {return $config{version};}

my $VERSION = getVersion();

sub pluginmain {
	my $class = shift;
	my $ntuser = shift;
	#::logMsg("Launching recentdocs v.".$VERSION);
	#::rptMsg("recentdocs v.".$VERSION); # banner
  #::rptMsg("(".getHive().") ".getShortDescr()."\n"); # banner
	my $reg = Parse::Win32Registry->new($ntuser);
	my $root_key = $reg->get_root_key;

	my $key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs";
	my $key;
	if ($key = $root_key->get_subkey($key_path)) {
		#::rptMsg("RecentDocs");
		#::rptMsg("**All values printed in MRUList\\MRUListEx order.");
		#::rptMsg($key_path);
		#::rptMsg("LastWrite Time: ".::getDateFromEpoch($key->get_timestamp())."Z");
# Get RecentDocs values		
		my %rdvals = getRDValues($key);
		if (%rdvals) {
			my $tag;
			if (exists $rdvals{"MRUListEx"}) {
				$tag = "MRUListEx";
			}
			elsif (exists $rdvals{"MRUList"}) {
				$tag = "MRUList";
			}
			else {
				
			}
			
			my @list = split(/,/,$rdvals{$tag});
			foreach my $i (@list) {
				#::rptMsg("  ".$i." = ".$rdvals{$i});
			}
			#::rptMsg("");
		}
		else {
			#::rptMsg($key_path." has no values.");
			#::logMsg("Error: ".$key_path." has no values.");
		}
# Get RecentDocs subkeys' values		
	my @subkeys = $key->get_list_of_subkeys();
		if (scalar(@subkeys) > 0) {
			foreach my $s (@subkeys) {
				if($s->get_name() ne ".jpg" & $s->get_name() ne ".cc" & $s->get_name() ne ".com"){
				::rptMsg(sprintf "%-20s|%-40s","Type/Extension",$s->get_name());
				::rptMsg(sprintf "%-20s|%-40s","Last Write Time",::getDateFromEpoch($s->get_timestamp()));
				
				my %rdvals = getRDValues($s);
				if (%rdvals) {
					my $tag;
					if (exists $rdvals{"MRUListEx"}) {
						$tag = "MRUListEx";
					}
					elsif (exists $rdvals{"MRUList"}) {
						$tag = "MRUList";
					}
					else {
				
					}
			
					my @list = split(/,/,$rdvals{$tag});
					#::rptMsg($tag." = ".$rdvals{$tag});
					foreach my $i (@list) {
						::rptMsg(sprintf "%-20s|%-40s","File name",$rdvals{$i}) if($s->get_name() ne "Folder");
						::rptMsg(sprintf "%-20s|%-40s","Folder name",$rdvals{$i}) if($s->get_name() eq "Folder");
					}
					
					#::rptMsg("");
				}
				else {
					#::rptMsg($key_path." has no values.");
				}
				}}
		}
		else {
			#::rptMsg($key_path." has no subkeys.");
		}
	}
	else {
		#::rptMsg($key_path." not found.");
	}
}


sub getRDValues {
	my $key = shift;
	
	my $mru = "MRUList";
	my %rdvals;
	
	my @vals = $key->get_list_of_values();
	if (scalar @vals > 0) {
		foreach my $v (@vals) {
			my $name = $v->get_name();
			my $data = $v->get_data();
			if ($name =~ m/^$mru/) {
				my @mru;
				if ($name eq "MRUList") {
					@mru = split(//,$data);
				}
				elsif ($name eq "MRUListEx") {
					@mru = unpack("V*",$data);
				}
# Horrible, ugly cludge; the last, terminating value in MRUListEx
# is 0xFFFFFFFF, so we remove it.
				pop(@mru);
				$rdvals{$name} = join(',',@mru);
			}
			else {
# New code
				$data = decode("ucs-2le", $data);
				my $file = (split(/\00/,$data))[0];
#				my $file = (split(/\00\00/,$data))[0];
#				$file =~ s/\00//g;
				$rdvals{$name} = $file;
			}
		}
		return %rdvals;
	}
	else {
		return undef;
	}
}

1;