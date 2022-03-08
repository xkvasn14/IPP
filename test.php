<?php
#https://www.quackit.com/html/html_table_generator.cfm <- really nice html tables!
# Jaroslav Kvasnička
# IPP - proj 2
# test.php


$parseOnlyCheck = False;
$parseScriptCheck = False;
$intOnlyCheck = False;
$intScriptCheck = False;
$recursiveCheck = False;
$success = 0;
$failure = 0;
$counter = 0;
$directoryDefault = realpath("");
$directory = realpath("");
$directoryInt = realpath(""."interpret.py");
$directoryParse = realpath(""."parse.php");
$directoryJexamxml = "/pub/courses/ipp/jexamxml/jexamxml.jar";
$directoryJexamcfg = "/pub/courses/ipp/jexamxml/options";


# ------------------ Argument Parser ----------------------
foreach($argv as $arg)
{
    $arg = preg_replace('/^--/',"",$arg);
    $arg = preg_replace('/=.+/',"=",$arg);


    if("help" == $arg && $argc == 2)
    {
        echo "--help               pro zobrazení nápovědy\n";
        echo "--directory=path     test hledá v zadaném adresáři, jinak prochází aktuální adresář\n";
        echo "--recursive          test bude procházet i podadresáře\n";
        echo "--parse-script=file  soubor se skriptem parse.php, pokud není hledá v aktuálním adresáři\n";
        echo "--int-script=file    soubor se skriptem interpret.py, pokud není hledá v aktuálním adresáři\n";
        echo "--parse-only         bude testován pouze soubor parse.php\n";
        echo "--int-only           bude testován pouze soubor interpret.py\n";
        echo "--jexamxml=file      soubor s JAR balíčkem s nástrojem A7Soft JExamXML\n";
        echo "--jexamcfg=file      soubor s konfigurací nástroje A7Soft JExamXML\n";
        exit(0);
    }
    elseif("directory=" == $arg){
        $directory = preg_replace('/^--directory=/',"",$argv[$counter]);
        $directoryDefault = $directory;
        if(!is_dir($directory))
            exit(11);
    }
    elseif("recursive" == $arg){
        $recursiveCheck = True;
    }
    elseif("parse-script=" == $arg && $intOnlyCheck == False){
        $parseScriptCheck = True;
        $directoryParse = preg_replace('/^--parse-script=/',"",$argv[$counter]);
        if(!is_dir($directoryParse))
            exit(11);
    }
    elseif("int-script=" == $arg && $parseOnlyCheck == False){
        $intScriptCheck = True;
        $directoryInt = preg_replace('/^--int-script=/',"",$argv[$counter]);
        if(!is_dir($directoryInt))
            exit(11);
    }
    elseif("parse-only" == $arg && $intOnlyCheck == False && $intScriptCheck = False){
        $parseOnlyCheck = True;
    }
    elseif("int-only" == $arg && $parseOnlyCheck == False && $parseScriptCheck == False){
        $intOnlyCheck = True;
    }
    elseif("jexamxml=" == $arg){
        $directoryJexamxml = preg_replace('/^--jexamxml=/',"",$argv[$counter]);
        if(!is_dir($directoryJexamxml))
            exit(11);
    }
    elseif("jexamcfg=" == $arg){
        $directoryJexamcfg = preg_replace('/^--jexamcfg=/',"",$argv[$counter]);
        if(!is_dir($directoryJexamcfg))
            exit(11);
    }
    elseif($arg == "test.php")
    {}
    else{
        exit(10);
    }
    $counter = $counter + 1;
}
# ------------------ Argument Parser ----------------------
# ------------------ First HTML      ----------------------
echo "<!doctype html><html>
	<head>
<style>
table.GeneratedTable {
  width: 100%;
  background-color: #ffffff;
  border-collapse: collapse;
  border-width: 2px;
  border-color: #ffcc00;
  border-style: dashed;
  color: #000000;
}

table.GeneratedTable td, table.GeneratedTable th {
  border-width: 2px;
  border-color: #ffcc00;
  border-style: dashed;
  padding: 3px;
}

table.GeneratedTable thead {
  background-color: #ffcc00;
}
</style>

<table class=GeneratedTable>
  <thead>
    <tr>
      <th>Name & path</th>
      <th>Exit code / Expected</th>
      <th>Pass / Fail</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td></td>
      <td></td>
    </tr>";



# ------------------ First HTML      ----------------------



# ------------------ TESTING         ----------------------
if($parseOnlyCheck == True && $intOnlyCheck == False)
{
    # parser only
    if($recursiveCheck == True)
    {
        $adress = new RecursiveDirectoryIterator($directory);
        $arrofarr = new RecursiveIteratorIterator($adress);
        $names = new RegexIterator($arrofarr, '/^.+\.src$/i', RecursiveRegexIterator::GET_MATCH);

        foreach ($names as $key) {
            $item = strrev($key[0]);
            $item = strrev(explode(".", $item, 2)[1]);
            $directory = $item;
            if (!is_file($directory . ".out"))
                touch($directory . ".out");
            if (!is_file($directory . ".in"))
                touch($directory . ".in");
            if (!is_file($directory . ".rc")) {
                touch($directory . ".rc");
                $file = fopen($directory . '.rc', "w");
                fwrite($file, "0");
                fclose($file);
            }

            exec("php7.4 " . $directoryParse . " <".  $directory . ".src >file", $output, $ret_value);
            $returnValue = fgets(fopen($directory . ".rc", 'r'));

            if($ret_value == 0)
            {
                exec("java -jar ".$directoryJexamxml." file ". $directory.".out",$output,$ret_value);
                if($ret_value == 0)
                {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                }
                else
                {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            }
            else
            {
                if($returnValue == $ret_value)
                {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                }
                else
                {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            }
        }
        unlink("file");
    }
    else
    {
        $arr = glob("*.src");
        foreach ($arr as $item) {
            $item = preg_replace('/\.src/',"",$item);
            $directory = $directoryDefault.'/'.$item;

            if (!is_file($directory . ".out"))
                touch($directory . ".out");
            if (!is_file($directory . ".in"))
                touch($directory . ".in");
            if (!is_file($directory . ".rc")) {
                touch($directory . ".rc");
                $file = fopen($directory . '.rc', "w");
                fwrite($file, "0");
                fclose($file);
            }

            exec("php7.4 " . $directoryParse . " <" . $directory . ".src >file", $output, $ret_value);
            $returnValue = fgets(fopen($directory . ".rc", 'r'));

            if ($ret_value == 0) {
                exec("java -jar " . $directoryJexamxml . " file " . $directory . ".out", $output, $ret_value);
                if ($ret_value == 0) {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                } else {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            } else {
                if ($returnValue == $ret_value) {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                } else {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            }
        }
    }
    unlink("file");
}
elseif($intOnlyCheck == True && $parseOnlyCheck == False)
{
    # interpret only
    if($recursiveCheck == True)
    {
        $adress = new RecursiveDirectoryIterator($directory);
        $arrofarr = new RecursiveIteratorIterator($adress);
        $names = new RegexIterator($arrofarr, '/^.+\.src$/i', RecursiveRegexIterator::GET_MATCH);

        foreach ($names as $key) {
            $item = strrev($key[0]);
            $item =strrev(explode(".", $item,2)[1]);
            $directory = $item;
            if (!is_file($directory . ".out"))
                touch($directory . ".out");
            if (!is_file($directory . ".in"))
                touch($directory . ".in");
            if (!is_file($directory . ".rc")) {
                touch($directory . ".rc");
                $file = fopen($directory . '.rc', "w");
                fwrite($file, "0");
                fclose($file);
            }

            exec("python3 " . $directoryInt . " --source=" . $directory . ".src --input=" . $directory . ".in >file", $output, $ret_value);
            $returnValue = fgets(fopen($directory . ".rc", 'r'));


            if ($returnValue == $ret_value && $ret_value != 0) {
                # SUCCESS
                echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
            } elseif ($returnValue != $ret_value && $ret_value != 0) {
                # FAILURE
                echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
            } elseif ($returnValue == $ret_value && $ret_value == 0) {
                exec("diff file " . $directory . ".out", $output, $return_value);
                if ($return_value == 0) {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$return_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                } else {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$return_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            } else {
                # FAILURE
                echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
            }
        }
        unlink("file");
    }
    else
    {
        $arr = glob("*.src");
        foreach($arr as $item) {
            $item = preg_replace('/\.src/',"",$item);
            $directory = $directoryDefault.'/'.$item;

            if (!is_file($directory . ".out"))
                touch($directory . ".out");
            if (!is_file($directory . ".in"))
                touch($directory . ".in");
            if (!is_file($directory . ".rc")) {
                touch($directory . ".rc");
                $file = fopen($directory . '.rc', "w");
                fwrite($file, "0");
                fclose($file);
            }

            exec("python3 " . $directoryInt . " --source=" . $directory . ".src --input=" . $directory . ".in >file", $output, $ret_value);
            $returnValue = fgets(fopen($directory . ".rc", 'r'));

            if ($returnValue == $ret_value && $ret_value != 0) {
                # SUCCESS
                echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
            } elseif ($returnValue != $ret_value && $ret_value != 0) {
                # FAILURE
                echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
            } elseif ($returnValue == $ret_value && $ret_value == 0) {
                exec("diff file " . $directory . ".out", $output, $return_value);
                if ($return_value == 0) {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$return_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                } else {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$return_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            } else {
                # FAILURE
                echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
            }
        }
    }
    unlink("file");
}
elseif($intOnlyCheck == False && $parseOnlyCheck == False)
{
    # parser & interpret
    if($recursiveCheck == true)
    {
        $adress = new RecursiveDirectoryIterator($directory);
        $arrofarr = new RecursiveIteratorIterator($adress);
        $names = new RegexIterator($arrofarr, '/^.+\.src$/i', RecursiveRegexIterator::GET_MATCH);

        foreach ($names as $key) {
            $item = strrev($key[0]);
            $item = strrev(explode(".", $item, 2)[1]);
            $directory = $item;

            if (!is_file($directory . ".out"))
                touch($directory . ".out");
            if (!is_file($directory . ".in"))
                touch($directory . ".in");
            if (!is_file($directory . ".rc")) {
                touch($directory . ".rc");
                $file = fopen($directory . '.rc', "w");
                fwrite($file, "0");
                fclose($file);
            }

            exec("php7.4 " . $directoryParse . " <" . $directory . ".src >filex", $output, $ret_value);
            $returnValue = fgets(fopen($directory . ".rc", 'r'));

            if($ret_value == 0)
            {
                exec("python3.8 ".$directoryInt." --source=".$directory."filex --input=".$directory.".in >file",$output,$ret_value);
                $returnValue = fgets(fopen($directory.".rc",'r'));

                if ($returnValue == $ret_value && $ret_value != 0) {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                } elseif ($returnValue != $ret_value && $ret_value != 0) {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                } elseif ($returnValue == $ret_value && $ret_value == 0) {
                    exec("diff file " . $directory . ".out", $output, $return_value);
                    if ($return_value == 0) {
                        # SUCCESS
                        echo "<tr>
                      <td>$directory</td>
                      <td>$return_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                    } else {
                        # FAILURE
                        echo "<tr>
                      <td>$directory</td>
                      <td>$return_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                    }
                } else {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            }
            else
            {
                if($returnValue == $ret_value)
                {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                }
                else
                {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            }
        }
        unlink("filex");
        unlink("file");
    }
    else
    {
        $arr = glob("*.src");
        foreach ($arr as $item) {
            $item = preg_replace('/\.src/',"",$item);
            $directory = $directoryDefault.'/'.$item;

            if (!is_file($directory . ".out"))
                touch($directory . ".out");
            if (!is_file($directory . ".in"))
                touch($directory . ".in");
            if (!is_file($directory . ".rc")) {
                touch($directory . ".rc");
                $file = fopen($directory . '.rc', "w");
                fwrite($file, "0");
                fclose($file);
            }

            exec("php7.4 " . $directoryParse . " <" . $directory . ".src >filex", $output, $ret_value);
            $returnValue = fgets(fopen($directory . ".rc", 'r'));

            if($ret_value == 0)
            {
                exec("python3.8 ".$directoryInt." --source=".$directory."filex --input=".$directory.".in >file",$output,$ret_value);
                $returnValue = fgets(fopen($directory.".rc",'r'));

                if ($returnValue == $ret_value && $ret_value != 0) {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                } elseif ($returnValue != $ret_value && $ret_value != 0) {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                } elseif ($returnValue == $ret_value && $ret_value == 0) {
                    exec("diff file " . $directory . ".out", $output, $return_value);
                    if ($return_value == 0) {
                        # SUCCESS
                        echo "<tr>
                      <td>$directory</td>
                      <td>$return_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                    } else {
                        # FAILURE
                        echo "<tr>
                      <td>$directory</td>
                      <td>$return_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                    }
                } else {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            }
            else
            {
                if($returnValue == $ret_value)
                {
                    # SUCCESS
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: green;\">PASS</td>
                      </tr>";
                }
                else
                {
                    # FAILURE
                    echo "<tr>
                      <td>$directory</td>
                      <td>$ret_value/$returnValue</td>
                      <td style=\"background-color: red;\">FAIL</td>
                      </tr>";
                }
            }
        }
    }
    unlink("filex");
    unlink("file");
}
else
{
    exit(10);
}


echo "</tbody></table></html>";
?>
