<!DOCTYPE HTML PUBLIC "-//SoftQuad Software//DTD HoTMetaL PRO 6.0::19990601::extensions to HTML 4.0//EN" "hmpro6.dtd">
<HTML> 
  <HEAD> 

  <META NAME="KEYWORDS" CONTENT="infinite , instant , unlimited , word search , wordsearch , generator , puzzle , script ,  printable"> 
<META NAME="DESCRIPTION" CONTENT="Word Search Puzzle Generator Script to create Word Search for prining or saving for use in your web browser">


	 <TITLE>Word Search Puzzle Generator by Emogic.com</TITLE> 
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
						<Center><H3>Word Search made by Emogic's Word Search Puzzle Generator</H3></center>
						<CENTER> 
<p>
<a href="/cgi/wordsearch/">Create a new Word Search Puzzle</a>
</p>

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





