<!DOCTYPE HTML PUBLIC "-//SoftQuad Software//DTD HoTMetaL PRO 6.0::19990601::extensions to HTML 4.0//EN" "hmpro6.dtd">
<HTML> 
  <HEAD> 

  <META NAME="KEYWORDS" CONTENT="infinite , instant , unlimited , word search , wordsearch , generator , puzzle , script ,  printable"> 
<META NAME="DESCRIPTION" CONTENT="Word Search Puzzle Generator Script to create Word Search for prining or saving for use in your web browser">


	 <TITLE>Infinite Crossword Puzzle Generator by Emogic.com</TITLE> 
  </HEAD> 
  <BODY BACKGROUND="wordsearch.gif"> 
	 <CENTER> 
		<TABLE CELLPADDING="0" CELLSPACING="0" BGCOLOR="#FFFFFF"> 
		  <TR> 
			 <TD></TD> 
		  </TR> 
		</TABLE> 
		<TABLE CELLPADDING="0" CELLSPACING="1" BGCOLOR="#000000"> 
		  <TR> 
			 <TD> 
				<TABLE CELLPADDING="5" CELLSPACING="0" BGCOLOR="#FFFFFF"> 
				  <TR> 
					 <TD> 
						<Center><H3>Word Search made by Emogic's Infinite Crossword Puzzle Generator</H3></center>
						<CENTER> 
<p>
<a href="http://www.somewhereincanada.com/cgi/wordsearch/">Create a new Word Search Puzzle</a>
</p>
<?echo linkgames("/wordsearch/common" , getgames('.')) , "<p></p>";?>

<?php
$myarray = array();

$dir="./"; // Directory where files are stored

if ($dir_list = opendir($dir))
	{
	while(($filename = readdir($dir_list)) !== false)
		{
		//if ($filename != "." && $filename != "..") 
		if (strpos($filename , "html"))
			{
			$myarray[] = $filename;
			}
		}
	closedir($dir_list);
	}

sort($myarray);

foreach ($myarray as $key => $val) 
	{
    ?>
    <a href="<?php echo $val; ?>"><?php echo $val;?></a> ,
    <?
	}

?>				

<?
function getgames($GameSavePath) 
	{	
	//input: server path to saved games , the uid of the game owner
	//output: a sorted array of the game numbers
	$gamesarray = array();
	if (is_dir("$GameSavePath") == FALSE) {return $gamesarray;}
	if ($handle = opendir("$GameSavePath")) 
		{
    	while (false !== ($file = readdir($handle))) 
			{
        	if ($file != "." && $file != ".." &&is_dir($file)) 
				{
				array_push($gamesarray , "$file");
    		    } 
			}
		}
	sort($gamesarray); //sort numerically	
	return $gamesarray;
	}

function linkgames($GameURL , $games)
	{	
	 //input: base url to games , the uid of the game owner , array of the owners games , the name or /uid of the person who wants to join this game
	 //output: a formated link to the game
	 
	 if ($games == array()) {return "No games created.<br>";} foreach ($games as $game) { $outstr = "$outstr<a href='$GameURL/$game'><u>$game</u></a> &nbsp;&nbsp;"; 
	 //$outstr = "$outstr <br>"; 
	 } return($outstr); } ?>		 

						  
						 

						  </CENTER> 
						<P></P> </TD> 
				  </TR> 
				</TABLE></TD> 
		  </TR> 
		</TABLE> 
		<TABLE CELLPADDING="0" CELLSPACING="0" BGCOLOR="#FFFFFF"> 
		  <TR> 
			 <TD> </TD> 
		  </TR> 
		</TABLE></CENTER> </BODY>
</HTML>





