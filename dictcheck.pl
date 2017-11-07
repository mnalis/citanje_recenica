#!/usr/bin/perl -T
# by Matija Nalis <mnalis-perl@voyager.hr> AGPLv3+ started 20171107
#  provjera ispravnosti hrvatski.in dictionarya

use strict;
use warnings;
use autodie qw(:all);

use Data::Dumper;
use feature 'say';

my %KEYS=();

sub provjeri
{
	my ($key) = @_;
	say "Parsing: $key";
	if (!defined $KEYS{$key}) { say "ERROR: Ne postoji key $key" }
	my @elements = split /:/, $KEYS{$key};
	foreach my $element (@elements) {
		say "  el=$element";
		if ($element =~ /^[A-Z][A-Z0-9_]*$/) {	# ALL_UPERCASE => this is another key
			provjeri($element);
		}
	}
}

####
#### MAIN
####

while (<>) {
	next if not /^\w/;
	chomp;
	my ($k,$v) = split " ", $_, 2;
	$KEYS{$k}.="$v:"
}



say Dumper(\%KEYS);
#provjeri ('RECENICA');


# mora biti od najduzih prema najkracima kako ne bi substituirali sadrzaj od npr. RECENICA  umjesto od RECENICA_UPITNA
foreach my $k (sort { length $b <=> length $a } keys %KEYS) {
	my $v=$KEYS{$k};
	say "zamjena k=$k\tv=$v";
	foreach my $k2 (keys %KEYS) {
		$KEYS{$k2} =~ s{\Q$k\E}{$v}g;	# in all values, replace KEY with its VALUE
	}
}

say Dumper(\%KEYS);
