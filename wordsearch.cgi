#!/usr/bin/perl

print "Content-type: text/html\n\n";

eval {
      use strict;
      use lib '.';
      #load up common variables and routines. // &cgierr
      require "vars.cgi";
      #JSON module
      require 'PP.pm';
      use JSON::PP;
      };
warn $@ if $@;

if ($@)
   {
    print "Content-type: text/plain\n\n";
    print "Error including libraries: $@\n";
    print "Make sure they exist, permissions are set properly, and paths are set correctly.";
    exit;
    }

eval { &main; };                            # Trap any fatal errors so the program hopefully
if ($@) { &cgierr("fatal error: $@"); }     # never produces that nasty 500 server error page.
exit;   # There are only two exit calls in the script, here and in in &cgierr.

sub main
{
@letters = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');

%in = &parse_form; #get input arguments
&process_arguments();
&set_defaults();
&clear_grid();
&create_word_list();

if (@word_list < $numberofwords) {$numberofwords = @word_list};

$time_to_quit = time() + 20; #only give 20 seconds to build
# Add words to puzzle
for ($word_counter = 0; $word_counter < $numberofwords; $word_counter++)
      {
      $ret_val = 0;
      while ($ret_val == 0) #keep trying words till we jam one in
              {
              $ret_val = &attempt_word_insert(&get_random_word);
              if (time() > $time_to_quit)
                  {last;}
              }
      if (time() > $time_to_quit)
                  {last;}
      }
&generate_answer_array();

$puzzle_string = &print_puzzle();
#$puzzle_string = &print_answers();
$answer_string = &print_answers();
#if ($in{answers} != 1) {$answer_string = ''}
$word_list_string = &print_word_list();

open (DATA, "<./templates/index.html") or die("Template file /templates/index.html does not exist");
@template_file = <DATA>;
close (DATA);
$template_file = join('' , @template_file);
$template_file =~ s/<%puzzle%>/$puzzle_string/;
$template_file =~ s/<%words%>/$word_list_string/;
$template_file =~ s/<%answers%>/$answer_string/;

#print $template_file;
#print "\n";

$template_file =~ s/\%archivepath\%/$archivepath/g;
$template_file =~ s/\%archiveurl\%/$archiveurl/g;
$template_file =~ s/\%scripturl\%/$scripturl/g;

#archive the puzzle!
my $game = time;
my $filename = "$game\.html";

#my $uid = $in{uid}; #facebook user ID number
#if ($uid eq '') {$uid='common'} #for non facebook games
#$template_file =~ s/\%uid\%/$uid/g;
#my $name = $in{name}; #facebook user name
#$name =~ s/\%20/ /g; #get rid of %20 for spaces
#$template_file =~ s/\%name\%/$name/g;
#$template_file =~ s/\%name\%/$name/g;

$template_file =~ s/\%filename\%/$filename/g;
$template_file =~ s/\%game\%/$game/g;
#print $template_file;

#write archive game file and directory
if (not -d ("$archivepath")) {mkdir("$archivepath")  or die("Could not create archive path $archivepath");}
#if (not -d ("$archivepath/$uid")) {mkdir("$archivepath/$uid")  or die("Could not create archive path $archivepath/$uid");}
#if (not -d ("$archivepath/$uid/$game")) {mkdir("$archivepath/$uid/$game")  or die("Could not create archive path $archivepath/$uid/$game");}
#open (DATA, ">$archivepath/$uid/$game/index.html") or die("Could not create archive file $archivepath/$uid/$game/index.html");
open (DATA, ">$archivepath/$filename") or die("Could not create archive file $archivepath/$filename");
print DATA $template_file;
close (DATA);
#create empty chat.txt file - cuts down on 404 errors
#open (DATA, ">$archivepath/$uid/$game/chat.txt") or die("Could not create chat file $archivepath/$game/chat.txt");
#close (DATA);
#create empty out.txt file - cuts down on 404 errors
#open (DATA, ">$archivepath/$uid/$game/out.txt") or die("Could not create chat file $archivepath/$uid/$game/out.txt");
#close (DATA);

#print a jump to game page output
#print qq|<META HTTP-EQUIV="Refresh" CONTENT="0; URL=$archiveurl/$uid/$game/?uid=$uid&name=$name">|; #name is for chat
print qq|<META HTTP-EQUIV="Refresh" CONTENT="0; URL=$archiveurl/$game\.html">|;

print "\n\n";
exit;
=pod
if ($in{email})
    {
    $mailresult=&sendmail($from , $from , $in{'email'}, $SMTP_SERVER, "$subject", $template_file);
    if ($mailresult ne "1") {die("MAIL NOT SENT. SMTP ERROR: $mailcodes{'$mailresult'}<br>Sendmail: $SEND_MAIL or SMTP Server: $SMTP_SERVER @mailloc\n<br><$sendmail>")}
    }
=cut
}

sub process_arguments()
{
#process input arguments

if ($in{width} !~ /^\d+$/) { $in{width} = 20;}
if  ($in{width} < 5)  { $in{width} = 5;}
if ( $in{width} > 50) { $in{width} = 50;}
$puzzle_x = $in{width}; $puzzle_y = $puzzle_x;

$numberofwords = $in{numberofwords};
if ( $in{numberofwords} !~ /^\d+$/) {$numberofwords = 10;}
if ( $in{numberofwords} < 5) { $numberofwords = 5;}
if ( $in{numberofwords} > 500 ) { $numberofwords = 500;}

if ($in{difficulty}) {$difficulty = $in{difficulty}; } else { $difficulty = 4;}
if ($in{wordlist}) {$word_string = $in{wordlist} } else
     {
     if ($in{wordfilename}) {$input_filename = $in{wordfilename};}
     else {$input_filename = "words/kjv.txt"};
     open (DATA, "<$input_filename") or die("Word file $input_filename does not exist");
     read(DATA , $word_string , 99999999); # Load words list
     close (DATA);
     }
};

sub set_defaults()
{
# Test inputs to see if they are valid and set defaults
if (($numberofwords =~ /[^0-9]/) ||($puzzle_x =~ /[^0-9]/) || ($puzzle_y =~ /[^0-9]/) || ($difficulty =~ /[^0-9]/)){die("ERROR: Non-numeric value specified for numeric-only option.\n");}
if ($puzzle_x < 10) { $puzzle_x = 10; $puzzle_y = 10;}
if (($difficulty < 1) || ($difficulty > 4)) { $difficulty = 4; } #default 4
if ($difficulty == 4) { $flag_reverse_words = 1; } else { $flag_reverse_words = 0; } # Set flag_reverse_words based on difficulty
};

sub generate_answer_array()
{
# Fill in blanks in the puzzle with random letters & generate an answer array
for ($v_counter = 0; $v_counter < $puzzle_y; $v_counter++)
      {
      for ($h_counter = 0; $h_counter < $puzzle_x; $h_counter++)
            {
            $solved_puzzle[$h_counter][$v_counter] = $puzzle[$h_counter][$v_counter];
            if ($puzzle[$h_counter][$v_counter] eq ""){$puzzle[$h_counter][$v_counter] = $letters[int(rand(26))];}
            }
      }
};

sub print_word_list()
{
my $count = 1;
my $trigger = 0;
my $local_string;
my $triggermax = scalar(@word_details) / 4; #4 columns

$local_string = "<table cellpadding='10';><tr>";
foreach $item (@word_details) {
#ID it with word_xxxxxx
if ($trigger == 0) {$local_string .= "<td>"}
eval $preitemtoeval;
$local_string .= "<div ID='word_$item'>$count. $preitem$item$postitem</div><br>";
$count = $count + 1;
$trigger = $trigger + 1;
if ($trigger >= $triggermax) {$local_string .= "</td>";$trigger = 0;}
}
$local_string .= "</tr></table>";

return $local_string;
};

sub print_answers()
{
my $local_string;

#$local_string .= "<div class='puzzle'>";
$local_string .= "<table class='puzzle'>";
for ($y = 0; $y < $puzzle_y; $y++)
      {
      #$local_string .= "<div class='row'>";
      $local_string .= "<tr class='row'>";
      for ($x = 0; $x < $puzzle_x; $x++)
        {
        #$local_string .= "<div class='box' id='AnswerCell\_$x\_$y'><div class='letter'>$puzzle[$x][$y]</div></div>";
        #$local_string .= "<div class='box' id='AnswerCell\_$x\_$y'>$puzzle[$x][$y]</div>";
        $local_string .= "<td class='box' id='AnswerCell\_$x\_$y'>$puzzle[$x][$y]</td>";
       # $local_string .= "<span class='box' id='AnswerCell\_$x\_$y'>$puzzle[$x][$y]</span>";
        }
       #$local_string .= "</div>";
       $local_string .= "</tr>";
       #$local_string .= "<br>";
      $local_string .= "\n";
      }
#$local_string .= "</div>";
$local_string .= "</table>";

return $local_string;
};

sub print_puzzle()
{
my $local_string;

$words_export_ref = \%words_export;
$utf8_encoded_json_text = encode_json $words_export_ref ;

$local_string .= "<script>var words = $utf8_encoded_json_text ; </script>";
#$local_string .= "<div class='puzzle'>";
$local_string .= "<table class='puzzle'>";
for ($y = 0; $y < $puzzle_y; $y++)
      {
      #$local_string .= "<div class='row'>";
      $ocal_string .= "<tr class='row'>";
      for ($x = 0; $x < $puzzle_x; $x++)
        {
        #$local_string .= "<div class='box' id='Cell\_$x\_$y' ONCLICK='HighlightBox(this.id);'><div class='letter'>$puzzle[$x][$y]</div></div>";
        #$local_string .= "<div class='box' id='Cell\_$x\_$y' ONCLICK='HighlightBox(this.id);'>$puzzle[$x][$y]</div>";
        #$local_string .= "<div class='box' id='Cell\_$x\_$y' ONCLICK='HighlightBox(this.id);'>$puzzle[$x][$y]</div>";
        $local_string .= "<td class='box' id='Cell\_$x\_$y' ONCLICK='HighlightBox(this.id);'>$puzzle[$x][$y]</td>";
        }
       $local_string .= "</tr>";
#       $local_string .= "<br>";
      $local_string .= "\n";
      }
$local_string .= "</table>";

return $local_string;
};

sub get_random_word()
{
do #don't use word twice!!!
    {$randomword = $word_list[rand(@word_list)];}
until ($PickedWords{$randomword} ne 1);
#set $PickedWords{} in &insert_word()
return $randomword;
};

sub create_word_list()
{
#scriptman filter any text block into @word_list
$word_string =~ s/[\s,\W,\d]+/ /g; #remove 2 or more spaces, non letters and numbers
@word_list = split(' ' , $word_string);
@word_list = grep {length() > 3}  @word_list; #remove words 3 letters or less
#@word_list = grep {length() < $puzzle_x - 3}  @word_list; #remove words greater than the width - 3
@word_list = grep {length() < $puzzle_x}  @word_list; #remove words greater than the width - 1
if ($in{nonames}){@word_list = grep {m/^[a-z]/} @word_list;} #remove words starting with capitals
#remove duplicate words
%wordhash = map{$_,1} @word_list; # or a hash slice: @wordhash{ @word_list } = (); # or a foreach: $wordhash{$_} = 1 foreach ( @word_list );
@word_list = keys %wordhash;
};

sub clear_grid()
{
# Initialize puzzle grid
for ($v_counter = 0; $v_counter < $puzzle_y; $v_counter++)
{for ($h_counter = 0; $h_counter < $puzzle_x; $h_counter++)
 {$puzzle[$h_counter][$v_counter] = "";}}
};

sub insert_word()
{
my $x_start = $_[0];
my $y_start = $_[1];
my $original_word = $_[2];
my $direction = $_[3];
my $word_reversed = $_[4];
my $x_cursor = $x_start;
my $y_cursor = $y_start;
my $word = uc($original_word);
my $letter_counter;
my $word_length = length($word);
my $word_inserted = 1; #assumsion

if ($direction == 1) {$x_dir = 1; $y_dir = 0;};
if ($direction == 2) {$x_dir = 0; $y_dir = 1;};
if ($direction == 3) {$x_dir = 1; $y_dir = 1;};
if ($direction == 4) {$x_dir = -1; $y_dir = 1;};
if ($word_reversed) {$word = reverse $word};

#see if text will fit
for ($letter_counter = 0; $letter_counter < $word_length; $letter_counter++)
     {
     $character = $puzzle[$x_cursor][$y_cursor];
     if ($character ne "")
          {
          if ($character ne substr($word,$letter_counter,1) )
               {
               $word_inserted = 0;
               last;
               };
          }
     $x_cursor = $x_cursor + $x_dir;
     $y_cursor = $y_cursor + $y_dir;
     }

@letterpositionlist = (); #list of letter positions for this word
#$word_export{$};
@endpoints = (); #first and last letter positions

if ($word_inserted) #it fits so insert word
     {
     $x_cursor = $x_start;
     $y_cursor = $y_start;
     for ($letter_counter = 0; $letter_counter < $word_length; $letter_counter++)
           {
           $puzzle[$x_cursor][$y_cursor] = substr($word,$letter_counter,1);
           push (@letterpositionlist , [$x_cursor,$y_cursor]); #build list of letter positions for this word
           $x_cursor = $x_cursor + $x_dir;
           $y_cursor = $y_cursor + $y_dir;
           }
      push (@word_details, "$original_word");
      $PickedWords{$original_word} = 1; #mark word used for use in &get_random_word() maybe better to just remove from list?

     @endpoints = ($letterpositionlist[0] , $letterpositionlist[scalar @letterpositionlist - 1]);
     $startstopposition = "$endpoints[0][0]_$endpoints[0][1]_$endpoints[1][0]_$endpoints[1][1]";
     $words_export{$startstopposition}{'word'} = $original_word;
     $words_export{$startstopposition}{'letterpositions'} = [@letterpositionlist];
     $words_export{$startstopposition}{'direction'} = $direction;
     }

return $word_inserted; # 0 - no 1 - yes
};

sub attempt_word_insert
{
my        $word = $_[0];
my        $direction;
my        $insert_x;
my        $insert_y;
my        $region_text;
my        $x_counter;
my        $y_counter;
my        $word_inserted = 0;
my        $letter_counter;
my        $original_word = $word; # Set original_word; we may reverse the word inserted
my        $word_reversed = 0; #default
my        $attempts = 100; #Try inserting word 100 times

# Set direction based on difficulty
if ($difficulty == 1){$direction = int(rand(2))+1;}
if ($difficulty == 2){$direction = int(rand(3))+1;}
if (($difficulty == 3) || ($difficulty == 4)){$direction = int(rand(4))+1;}

#if allowing reverse words, 1 in 3 chance it will be reversed
if ( (int(rand(3))) && ($flag_reverse_words == 1) ){$word_reversed = 1; }

# Attempt to insert the word into the puzzle
while (($word_inserted == 0) and ($attempts > 0))
        {
        if ($direction == 1) # Across
             {
             # Get random starting coordinates
             $insert_x = int(rand($puzzle_x - length($word)));
             $insert_y = int(rand($puzzle_y));
             $word_inserted = &insert_word($insert_x , $insert_y, $word , $direction , $word_reversed);
             }
        if ($direction == 2) # Down
             {
             # Get random starting coordinates
             $insert_x = int(rand($puzzle_x));
             $insert_y = int(rand($puzzle_y - length($word)));
             $word_inserted = &insert_word($insert_x , $insert_y, $word , $direction , $word_reversed);
             }
        if ($direction == 3) # Diagonal (down-right)
             {
             # Get random starting coordinates
             $insert_x = int(rand($puzzle_x - (length($word))));
             $insert_y = int(rand($puzzle_y - (length($word))));
             if ($insert_x < 0) { $insert_x = 0; }
             if ($insert_y < 0) { $insert_y = 0; }
             $word_inserted = &insert_word($insert_x , $insert_y, $word , $direction , $word_reversed);
             }
        if ($direction == 4) # Diagonal (down-left)
             {
             # Get random starting coordinates
             $insert_x = length($word) + int(rand($puzzle_x - length($word)));
             #$insert_x = int(rand($puzzle_x)) + length($word);
             $insert_y = int(rand($puzzle_y - (length($word))));
             if ($insert_x < 0) { $insert_x = 0; }
             if ($insert_y < 0) { $insert_y = 0; }
             $word_inserted = &insert_word($insert_x , $insert_y, $word , $direction , $word_reversed);
             }
        $attempts = $attempts - 1;
        }
return $word_inserted;
}
