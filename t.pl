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
use scigen;
use IO::File;

my $tex_file = "test.tex";

my $name_dat = {};
my $name_RE = undef;
my $tex_dat = {};
my $tex_RE = undef;

my $sysname = 'BurekOS';

my $tex_fh = new IO::File ("<scirules.in");
my $start_rule = "SCIPAPER_LATEX";
my @a = ($sysname);
$tex_dat->{"SYSNAME"} = \@a;

my $s = "";
my @b = ($s);
$tex_dat->{"SCIAUTHORS"} = \@b;

scigen::read_rules ($tex_fh, $tex_dat, \$tex_RE, 0);
my $tex = scigen::generate ($tex_dat, $start_rule, $tex_RE, 0, 1);
open( TEX, ">$tex_file" ) or die( "Couldn't open $tex_file for writing" );
print TEX $tex;
close( TEX );
