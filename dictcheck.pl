#!/usr/bin/perl -T
# by Matija Nalis <mnalis-perl@voyager.hr> AGPLv3+ started 20171107
#  provjera ispravnosti hrvatski.in dictionarya

use strict;
use warnings;
use autodie qw(:all);

use Data::Dumper;
use feature 'say';

my %KEYS=();
my %SEEN=();

####
#### MAIN
####

while (<>) {
	next if not /^\w/;
	chomp;
	my ($k,$v) = split " ", $_, 2;
	$KEYS{$k}.="$v:";
	$SEEN{$k}=0;
}



#say Dumper(\%KEYS);

# zamjena KEYeva sa njihovim VALUES
# mora biti od najduzih prema najkracima kako ne bi substituirali sadrzaj od npr. RECENICA  umjesto od RECENICA_UPITNA
foreach my $k (sort { length $b <=> length $a } keys %KEYS) {
	my $v=$KEYS{$k};
	#say "zamjena k=$k\tv=$v";
	foreach my $k2 (keys %KEYS) {
		if ($KEYS{$k2} =~ s{\Q$k\E}{$v}g) {	# in all values, replace KEY with its VALUE
			$SEEN{$k}++;
		}
	}
}

#say Dumper(\%KEYS);
#say Dumper(\%SEEN);


my $count_errors = 0;

# provjera nekoristenih KEYeva
foreach my $k (keys %SEEN) {
	if ($SEEN{$k} == 0 and $k ne 'RECENICA') {	# svi osim pocetnog moraju imati barem jednog childa
		$count_errors++;
		say "WARNING: nekorišteni key: $k";
	}
}

# provjera nedostajucih KEYeva
foreach my $k (keys %KEYS) {
	my $v=$KEYS{$k};
	if ($v =~ /([A-Z0-9_]{2,})/) {
		$count_errors++;
		say "ERROR: korištenje nepostojećeg keya u $k: $1";
	}
}

exit $count_errors;
