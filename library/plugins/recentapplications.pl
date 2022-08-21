
#-----------------------------------------------------------
# recentapplications.pl
# Plugin for Registry Ripper, NTUSER.DAT edition - gets the 
# UserAssist values 


package recentapplications;
use strict;

my %config = (hive          => "NTUSER\.DAT",
              hasShortDescr => 1,
              hasDescr      => 0,
              hasRefs       => 0,
              osmask        => 22,
              version       => 20170204);

sub getConfig{return %config}
sub getShortDescr {
	return "Displays contents of UserAssist subkeys";	
}
sub getDescr{}
sub getRefs {"Description of Control Panel Files in XP" => "http://support.microsoft.com/kb/313808"}
sub getHive {return $config{hive};}
sub getVersion {return $config{version};}

my $VERSION = getVersion();

sub pluginmain {
	my $class = shift;
	my $ntuser = shift;
	#::logMsg("Launching userassist v.".$VERSION);
	my $reg = Parse::Win32Registry->new($ntuser);
	my $root_key = $reg->get_root_key;
	
	my $key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist";              
	my $key;
	
	if ($key = $root_key->get_subkey($key_path)) {
		#::rptMsg("UserAssist");
		#::rptMsg($key_path);
		#::rptMsg("LastWrite Time ".::getDateFromEpoch($key->get_timestamp())."Z");
		my $timestamp1 = ::getDateFromEpoch($key->get_timestamp());
		#::rptMsg("");
		my @subkeys = $key->get_list_of_subkeys();
		if (scalar(@subkeys) > 0) {
			foreach my $s (@subkeys) {
				my $appname = $s->get_name();
				#::rptMsg(substr($appname,0,1) ne "{" & substr($appname,length($appname)-2,length($appname)-1) ne "}");
				#if(substr($appname,0,1) ne "{" & substr($appname,length($appname)-2,length($appname)-1) ne "}"){
				#::rptMsg(sprintf "%-20s|%-80s".$timestamp1,$s->get_name());
				processKey($s);
				#}
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

sub processKey {
	my $ua = shift;
	
	my $key = $ua->get_subkey("Count");

	my %ua = ();
	my @no_time = ();
	my $hrzr = "HRZR";
	
	my @vals = $key->get_list_of_values();
	if (scalar(@vals) > 0) {
		foreach my $v (@vals) {
			my $value_name = $v->get_name();
			my $data = $v->get_data();

# Windows XP/2003/Vista/2008
			if (length($data) == 16) {
				my ($session,$count,$val1,$val2) = unpack("V*",$data);
			 	if ($val2 != 0) {
					my $time_value = ::getTime($val1,$val2);
					if ($value_name =~ m/^$hrzr/) { 
						$value_name =~ tr/N-ZA-Mn-za-m/A-Za-z/;
					}
					$count -= 5 if ($count > 5);
					push(@{$ua{$time_value}},$value_name." (".$count.")");
				}
				else {
					push(@no_time,$value_name);
				}
			}
# Windows 7				
			elsif (length($data) == 72) { 
				$value_name =~ tr/N-ZA-Mn-za-m/A-Za-z/;
#				if (unpack("V",substr($data,0,4)) == 0) {	
#					my $count = unpack("V",substr($data,4,4));
#					my @t = unpack("VV",substr($data,60,8));
#					next if ($t[0] == 0 && $t[1] == 0);
#					my $time_val = ::getTime($t[0],$t[1]);	
#					print "    .-> ".$time_val."\n";
#					push(@{$ua{$time_val}},$value_name." (".$count.")");
#				}
				my $count = unpack("V",substr($data,4,4));
				my @t = unpack("VV",substr($data,60,8));
				if ($t[0] == 0 && $t[1] == 0) {
					push(@no_time,$value_name);
				}
				else {
#				
#				print "Value name: ".$value_name."\n";
#				
					my $time_val = ::getTime($t[0],$t[1]);
					push(@{$ua{$time_val}},$value_name." (".$count.")");
				}
			}
			else {
# Nothing else to do
			}
		}
		foreach my $t (reverse sort {$a <=> $b} keys %ua) {
			#::rptMsg(::getDateFromEpoch($t));
			foreach my $i (@{$ua{$t}}) {
				if(substr($i,0,0) ne "{" & substr($i,length($i)-1,length($i)-1) ne "}"){
				::rptMsg(sprintf "%-20s|%-80s",::getDateFromEpoch($t),$i);}
			}
		}
		#::rptMsg("");
		#::rptMsg("Value names with no time stamps:");
		#foreach my $n (@no_time) {
		#	::rptMsg("  ".$n);
		#}
		
	}
}
1;