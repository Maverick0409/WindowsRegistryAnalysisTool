
#-----------------------------------------------------------
# Plugin for Registry Ripper, NTUSER.DAT edition - gets the 
# TypedURLs values 

package urlstyped;
use strict;

my %config = (hive          => "NTUSER\.DAT",
              hasShortDescr => 1,
              hasDescr      => 0,
              hasRefs       => 1,
              osmask        => 22,
              version       => 20200526);

sub getConfig{return %config}
sub getShortDescr {
	return "Returns contents of user's TypedURLs key.";	
}
sub getDescr{}
sub getRefs {
	my %refs = ("IESample Registry Settings" => 
	            "http://msdn2.microsoft.com/en-us/library/aa908115.aspx",
	            "How to clear History entries in IE" =>
	            "http://support.microsoft.com/kb/157729");
	return %refs;	
}
sub getHive {return $config{hive};}
sub getVersion {return $config{version};}

my $VERSION = getVersion();

sub pluginmain {
	my $class = shift;
	my $ntuser = shift;
	#::logMsg("Launching typedurls v.".$VERSION);
	#::rptMsg("typedurls v.".$VERSION); # banner
    #::rptMsg("(".getHive().") ".getShortDescr()."\n"); # banner
	my $reg = Parse::Win32Registry->new($ntuser);
	my $root_key = $reg->get_root_key;
	
	my $key_path = 'Software\\Microsoft\\Internet Explorer\\TypedURLs';
	my $key;
	if ($key = $root_key->get_subkey($key_path)) {
		#::rptMsg("TypedURLs");
		#::rptMsg($key_path);
		::rptMsg(sprintf "%-20s|%-40s","Last Write Time",::getDateFromEpoch($key->get_timestamp()));
		my @vals = $key->get_list_of_values();
		if (scalar(@vals) > 0) {
			my %urls;
# Retrieve values and load into a hash for sorting			
			foreach my $v (@vals) {
				my $val = $v->get_name();
				my $data = $v->get_data();
				my $tag = (split(/url/,$val))[1];
				$urls{$tag} = $val.":".$data;
			}
# Print sorted content to report file			
			foreach my $u (sort {$a <=> $b} keys %urls) {
				my ($val,$data) = split(/:/,$urls{$u},2);
				::rptMsg(sprintf "%-20s|%-40s",$val,$data);
			}
		}
		else {
			#::rptMsg($key_path." has no values.");
		}
	}
	else {
		#::rptMsg($key_path." not found.");
	}
}

1;