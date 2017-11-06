#!/usr/bin/perl -w

#    This file is part of SCIgen.
#
#    SCIgen is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    SCIgen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with SCIgen; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

use lib '.';

use strict;
use autodie qw(:all);

use scigen;

my $hrv_dat = {};
my $hrv_RE = undef;

open my $hrv_fh, '<', 'hrvatski.in';
#open my $hrv_fh, 'egrep  "X|[Mm]a|vol|^[A-Z0-9_ ]+$" hrvatski.in|';
my $start_rule = "RECENICA";

scigen::read_rules ($hrv_fh, $hrv_dat, \$hrv_RE, 0);

my $recenica = scigen::generate ($hrv_dat, $start_rule, $hrv_RE, 0, 1);
print $recenica;

$recenica = scigen::generate ($hrv_dat, $start_rule, $hrv_RE, 0, 1);
print $recenica;

$recenica = scigen::generate ($hrv_dat, $start_rule, $hrv_RE, 0, 1);
print $recenica;
