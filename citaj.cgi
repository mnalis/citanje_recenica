#!/usr/bin/perl -T
# by Matija Nalis <mnalis-perl@voyager.hr> GPLv3+ started 20171106
# generira jednostavne recenice za citanje za prvasice

use strict;
use feature 'say';
use autodie qw(:all);

my $DB = 'rjecnik.txt';
my $DEBUG = 9;

$ENV{PATH} = '/bin:/usr/bin';
my %WORDS = ();

my @KONSTRUKCIJE = (
	"s1 g1 o1",
	"s1 g1 o2",
	"s1 g1 p1 o1",
	"s1 g1 p2 o2",
	"s2 g2 o1",
	"s2 g2 o2",
	"s2 g2 p1 o1",
	"s2 g2 p2 o2",
);

# reads the database
sub read_db()
{
	open my $db, '<', $DB;
	while (<$db>) {
		next if /^\s*(#.*)?$/;	# skip empty lines and comments
		chomp;
		my ($type, $word) = split ' ', $_, 2;
		$DEBUG > 7 && say "parsing $type => $word";
		push @{$WORDS{$type}}, $word;
	}
}

# returns a random element of the array
sub get_random1($)
{
	my ($aref) = @_;
	my $len = scalar @$aref;
	my $rnd = int(rand($len));
	my $ret = $$aref[$rnd];
	$DEBUG > 4 && say "len=$len, rnd=$rnd, ret=$ret";
	return $ret;
}

# given $KONSTRUKCIJE{xxx} template, generate a full sentence by replacing words.
sub fill_words($)
{
	my ($template) = @_;
	my $recenica = '';
	while ($template =~ s/^(\S+)(\s*)//) {
		my $token = $1;
		my $spaces = $2;
		$DEBUG > 5 && say "token=$token, template=$template";
		my $lref = $WORDS{$token};
		die "nepoznati token $token" if not defined $lref;
		my $word = get_random1($lref);
		$DEBUG > 4 && say "chosen word for token $token: $word";
		$recenica .= "$word$spaces";
	}

	return $recenica;
}

###
### here goes the main
###

read_db();	# initialize the DB

if ($DEBUG > 5) {
	use Data::Dumper;
	say Dumper(\%WORDS);
	say Dumper(\@KONSTRUKCIJE);
}

say fill_words(get_random1(\@KONSTRUKCIJE));
