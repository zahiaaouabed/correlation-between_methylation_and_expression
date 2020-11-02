#!/usr/bin/perl                                                                                                                                             
use YAML::Tiny;
use Statistics::R ;
use Statistics::Basic qw(:all);
use Parallel::Runner;
  
my $R = Statistics::R->new() ;
  
my @files = glob("CG*");
use Excel::Writer::XLSX;

my %counts;
my %cumulated_values;

my $context = $ARGV[2];

open(my $fh, $ARGV[0])
    or die "Could not open file!";
my $runner = Parallel::Runner->new(20);
while (my $row = <$fh>) { 
    chomp($row);
    @t = split("\t", $row);
    $chr = $t[0];
    $tss = $t[1];
    $tts = $t[2];
    my @files = glob("CG_bed_files");
    ProcessFiles(\@files, $chr, $tss, $tts);
}
$runner->finish;

sub ProcessFiles {
    my $achr = "chr".$_[1];
    my $afrom = $_[2];
    my $ato = $_[3];
    my $list_ref = shift; 
    my $k = 0;
    my $n;
    open(my $fh, $ARGV[1]) # subjectsall.csv
	or die "Could not open file!";
    while (my $row = <$fh>) {
	chomp($row);
	my $filename = "CG_bed_files/s".$row.".met.".$context;
	my $filename_out = "s".$row.".met";
	$runner->run( sub { 

	    my $_from = $afrom-5000;
	    my $_to = $ato+5000;
	    my $begin = $_from+" ";
	    my $end = $_to+" ";
	    my $s = 0;
	    while (substr($begin,0,$s) == substr($end, 0,$s)) {
		$s++;
	    }
	    $common = substr($begin, 0, $s-1);
	    my $search = $achr."\t".$common;

            print "serach=".$search."\n";
            print "common=".$common."\n";

	    print $achr."/".$context."/".$filename_out."_".$achr."_".$_from."_".$_to.".".$context.".METH.gene5k.profile\n";
	    if (! -e $achr."/".$context."/".$filename_out."_".$achr."_".$_from."_".$_to.".".$context.".METH.gene5k.profile") {
		$size = $_to-$_from;
		print $size."\n";
		my $var = `cat ${filename} | awk \'\{ if (\$1 == "$achr" && \$2 > $_from && \$2 < $_to )  print \$0 \}\' > ${achr}/${context}/${filename_out}_${achr}_${_from}_${_to}.${context}.METH.gene5k.profile`;
		print "no\n";
	    } else {
		print "exists\n";
	    }
		      } );

    }
}
