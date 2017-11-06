#!/usr/bin/perl -T
# by Matija Nalis <mnalis-perl@voyager.hr> GPLv3+ started 20171106
# generira jednostavne rečenice za čitanje (za prvašiće - polaznike prvog razreda osnovne škole)

use strict;
use feature 'say';
use autodie qw(:all);
use utf8;

my $DEBUG = 9;
my $DB_WORDS = 'rjecnik.txt';
my $DB_CONSTRUCTS = 'recenice.txt';
my $ONLY_UPPERCASE = 1;
my $LETTERS = 'manieouljr';	# by default accept all letters

$ENV{PATH} = '/bin:/usr/bin';
my %WORDS = ();
my @KONSTRUKCIJE = ();

# reads the database
sub read_db()
{
	open my $db_words, '<:encoding(UTF-8)', $DB_WORDS;
	while (<$db_words>) {
		next if /^\s*(#.*)?$/;	# skip empty lines and comments
		chomp;
		my ($type, $word) = split ' ', $_, 2;
		$DEBUG > 7 && say "parsing $type => $word";
		if ($word !~ /^[$LETTERS ]+$/i) {
			$DEBUG > 8 && say "skipping $word, as it does not contain only $LETTERS";
			next;		# skip words containing non yet learned letters
		}
		push @{$WORDS{$type}}, $word;
		$DEBUG > 8 && say "adding $word";
	}

	open my $db_constructs, '<:encoding(UTF-8)', $DB_CONSTRUCTS;
	while (<$db_constructs>) {
		next if /^\s*(#.*)?$/;	# skip empty lines and comments
		chomp;
		push @KONSTRUKCIJE, $_;
		$DEBUG > 8 && say "adding construct $_";
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


# Fixing starting letter to upcase, and add '.' or '!' at random.
sub fix_case($)
{
	my ($s) = @_;
	if ($ONLY_UPPERCASE) {
		$s = uc ($s);
	} else {
		$s = ucfirst ($s);
	}
	my @end = qw(. !);
	$s .= get_random1 (\@end);
	return $s;
}

###
### here goes the main
###

binmode STDOUT, ':utf8';
read_db();	# initialize the DB

if ($DEBUG > 5) {
	use Data::Dumper;
	say Dumper(\%WORDS);
	say Dumper(\@KONSTRUKCIJE);
}

say fix_case(fill_words(get_random1(\@KONSTRUKCIJE)));
