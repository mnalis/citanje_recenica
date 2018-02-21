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
my $LETTERS   = 'abcćčdđefghijklmnoprsštuvzž';
my $UPLETTERS = 'ABCĆČDĐEFGHIJKLMNOPRSŠTUVZŽ';

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

$| = 1;

binmode STDOUT, ':utf8';
binmode STDERR, ':utf8';

$q  = new CGI;
print $q->header (
	-charset    => 'utf-8',
	);

$LETTERS = validate_oknull('letters', "[$LETTERS]{0,27}") || $LETTERS;
my $MUST = validate_oknull('must', "([$LETTERS$UPLETTERS]|[Ll][Jj]|[Nn][Jj]|[Dd][Žž])") || '';
$ONLY_UPPERCASE = validate_oknull('upcase', '[01]') || 0;
$DEBUG = validate_oknull('debug', '[0-9]*') || 0;
$DEBUG > 1 && say "Allowed letters=$LETTERS (" . length($LETTERS) . "), must use=$MUST, upcase=$ONLY_UPPERCASE";

my $ok_slova = qr/^[$LETTERS \.!\?]+$/i;

read_db();	# initialize the DB

# filter by allowed letters
for my $macro (keys %$hrv_dat) {
	my $v = $$hrv_dat{$macro};
	foreach my $orig_word (@$v) {
		my $word = $orig_word . " "; 	# make a copy, so we don't clobber the original value!
		$DEBUG > 10 && say "hrv_dat{$macro}";
		$DEBUG > 11 && say "\tpre =  $word";
		my $plain_words = '';
		while ($word =~ s/$hrv_RE//s ) {
			my $preamble = $1;
			my $rule = $2;
			$DEBUG > 13 && say "\t\tpreamble=$preamble\n\t\trule=$rule";
			$plain_words .= $preamble;
		}
		$plain_words .= $word;	# for simple words withut macro, while() above does not execute at all;
		$DEBUG > 12 && say "\tpost = $word";
		$DEBUG > 10 && say "\tplain_words = $plain_words";

		if ($plain_words =~ /$ok_slova/ and $plain_words =~ /$MUST/) {
			$DEBUG > 11 && say "\tok, keeping word";
		} else {
			$DEBUG > 10 && say "\t removing word '$orig_word' as it does not match ok_slova=$ok_slova and MUST=$MUST";
			$orig_word = undef;
		}
	}
	@$v = grep defined, @$v;	# remove all undef values
}


if ($DEBUG > 7) {
	use Data::Dumper;
	$Data::Dumper::Terse = 1;
	say "\nok_slova = " . Dumper($ok_slova);
	say "MUST = " . Dumper($MUST);
	say "hrv_RE = " . Dumper($hrv_RE);
	say "hrv_dat = " . Dumper($hrv_dat);
}

my $start_rule = "RECENICA";
my $recenica = 'XXX_%UNDEF0%';
my $count = 10000;
my $found = 0;

# FIXME: this is rather stupid and slow way to eliminate sentances with invalid letters, but is quickest to implement... should really modify scigen.pm one day (but watch out for non-expanded macros if there is nothing matching them!)
# FIXME: also should support more than one $MUST letter
while ($count-- > 0 and $found < 2) {
	$found = 0;
	$recenica = scigen::generate ($hrv_dat, $start_rule, $hrv_RE, 0, 1);
	chomp $recenica;
	$DEBUG > 3 && say "Pokusavam recenicu '$recenica' u setu slova '$ok_slova' (obavezna slova: $MUST)";
	if ($recenica =~ /$ok_slova/) { $found++; }
	if ($recenica =~ /$MUST/) { $found++; }
}

if ($count > 0) {
	say fix_case($recenica);
	$DEBUG > 0 && say "(count went down to $count)";
} else {
	say "(Nažalost, ne mogu pronaći rečenicu koji koristi samo slova: $LETTERS" . ($MUST ? " (obavezna slova: $MUST)" : "") . ")";
}

