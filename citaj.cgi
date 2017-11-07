#!/usr/bin/perl -T
# by Matija Nalis <mnalis-perl@voyager.hr> AGPLv3+ started 20171106
# generira jednostavne rečenice za čitanje (za prvašiće - polaznike prvog razreda osnovne škole)

use strict;
use lib '.';
use feature 'say';
use autodie qw(:all);
use utf8;

use CGI qw(-utf8);

use scigen;

my $DEBUG = 0;
my $DB_WORDS = 'hrvatski.in';
my $ONLY_UPPERCASE = 0;
my $LETTERS = 'abcćčdđefghijklmnoprsštuvzž';

$ENV{PATH} = '/bin:/usr/bin';


# reads the database
my $hrv_dat = {};
my $hrv_RE = undef;
sub read_db()
{
	open my $hrv_fh, '<:encoding(UTF-8)', $DB_WORDS;
	scigen::read_rules ($hrv_fh, $hrv_dat, \$hrv_RE, 0);
}


# Fixing starting letter to upcase, and add '.' or '!' at random.
sub fix_case($)
{
	my ($s) = @_;
	return $ONLY_UPPERCASE ? uc ($s) : ucfirst ($s);
}

# validates CGI param
my $q;
sub validate_oknull($$)
{
	my ($param, $regex) = @_;
	my $value = $q->param($param);
	if (not defined $value) { return undef; }
	if ($value =~ /^($regex)$/) { return $1; }
	die "invalid value for $param: $value does not match $regex";
}

###
### here goes the main
###

binmode STDOUT, ':utf8';
binmode STDERR, ':utf8';

$q  = new CGI;
print $q->header (
	-charset    => 'utf-8',
	);

$LETTERS = validate_oknull('letters', "[$LETTERS]{0,27}") || $LETTERS;
$ONLY_UPPERCASE = validate_oknull('upcase', '[01]') || 0;
$DEBUG = validate_oknull('debug', '[0-9]') || 0;
$DEBUG > 1 && say "Allowed letters=$LETTERS (" . length($LETTERS) . "), upcase=$ONLY_UPPERCASE";

read_db();	# initialize the DB

if ($DEBUG > 7) {
	use Data::Dumper;
	say Dumper(\$hrv_dat);
	say Dumper(\$hrv_RE);
}

my $start_rule = "RECENICA";
my $recenica = 'XXX_%UNDEF0%';
my $count = 10000;
my $ok_slova = qr/^[$LETTERS \.!\?]+$/i;

# FIXME: this is rather stupid and slow way to eliminate sentances with invalid letters, but is quickest to implement... should really modify scigen.pm one day (but watch out for non-expanded macros if there is nothing matching them!)
while ($count-- > 0 and $recenica !~ /$ok_slova/) {
	$recenica = scigen::generate ($hrv_dat, $start_rule, $hrv_RE, 0, 1);
	chomp $recenica;
	$DEBUG > 3 && say "Pokusavam recenicu '$recenica' u setu slova '$ok_slova'";
}

if ($count > 0) {
	say fix_case($recenica);
	$DEBUG > 0 && say "(count went down to $count)";
} else {
	say "(Nažalost, ne mogu pronaći rečenicu koji koristi samo slova: $LETTERS)";
}

