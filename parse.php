<?php

//INITIALIZATION
$STDIN = STDIN;
$STDOUT = STDOUT;
$order = 0;
ini_set('display_errors','stderr');
//END-INITIALIZATION

if($argc == 0)
    exit(10);

//Prints user help
if($argc == 2) {
    if ($argv[1] == "--help") {
        fprintf(STDOUT, "Error codes:\n");
        fprintf(STDOUT, "10 - missing or wrong parameters\n");
        fprintf(STDOUT, "11 - error input file\n");
        fprintf(STDOUT, "12 - error output file\n");
        fprintf(STDOUT, "21 - wrong or missing header in source code\n");
        fprintf(STDOUT, "22 - unknown or wrong operational code in source code -> lexical error\n");
        fprintf(STDOUT, "23 - another lexical or syntax error in source code -> syntax error\n");
        fprintf(STDOUT, "99 - Intern error\n");
        exit(0);
    } else
        exit(10);
}

// Checks header .IPPcode21
if($argc == 1) {

    while($line = fgets($STDIN))
    {
        $line = preg_replace("/#.*/", "", $line, 1, $found);
        if (preg_match("/^.IPPcode21/",$line)) {
            fprintf($STDOUT, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
            fprintf($STDOUT, "<program language=\"IPPcode21\">\n");
            break;
        }
        elseif ($line == "" || $line == "\n") {
            continue;
        }
        else
            exit(21);
    }



    while (($line = fgets($STDIN)) != NULL) {
        $order++;

        //Line Parser and Comment Trimmer
        $line = preg_replace("/#.*/", "", $line, 1, $found);
        $array = preg_split("/[[:blank:]]+/", trim($line), 5, PREG_SPLIT_NO_EMPTY);
        $count = count($array);

        //Instruction Parser
        if ($array == NULL)
            $order--;
        else {
            if ($count == 5)
                exit(23);

            $opcode = $array[0];
            $opcode = strtoupper($opcode);
            switch ($opcode) {
                // var symb
                case "MOVE":
                case "INT2CHAR":
                case "NOT":
                case "STRLEN":
                case "TYPE":
                    func_var_symb($order, $opcode, $array);
                    break;

                // var
                case "DEFVAR":
                case "POPS":
                    func_var($order, $opcode, $array);
                    break;

                // none
                case "CREATEFRAME":
                case "PUSHFRAME":
                case "POPFRAME":
                case "RETURN":
                case "BREAK":
                    func_none($order, $opcode, $array);
                    break;

                // label
                case "CALL":
                case "LABEL":
                case "JUMP":
                    func_label($order, $opcode, $array);
                    break;

                //label symb symb
                case "JUMPIFEQ":
                case "JUMPIFNEQ":
                    func_label_symb_symb($order, $opcode, $array);
                    break;

                // var symb symb
                case "ADD":
                case "SUB":
                case "MUL":
                case "IDIV":
                case "LT":
                case "GT":
                case "EQ":
                case "AND":
                case "OR":
                case "STRI2INT":
                case "CONCAT":
                case "GETCHAR":
                case "SETCHAR":
                    func_var_symb_symb($order, $opcode, $array);
                    break;

                //symb
                case "PUSHS":
                case "WRITE":
                case "DPRINT":
                case "EXIT":
                    func_symb($order, $opcode, $array);
                    break;

                //var type
                case "READ":
                    func_var_type($order, $opcode, $array);
                    break;

                // exit - no instruction found
                default:
                    exit(22);
            }
        }
    }
    fprintf(STDOUT, "</program>"); // end of program
}

//FUNCTIONS
// Checks for these instruction cases:
//"CREATEFRAME" "PUSHFRAME" "POPFRAME" "RETURN" "BREAK"
// Input: counter $order, Instruction $opcode, array of args $array
// Output: printer XML code or error
function func_none($order, $opcode, $array)
{
    if (count($array) == 1) {
            fprintf(STDOUT, "\t<instruction order=\"%d\" opcode=\"%s\">\n", $order, $opcode);
            fprintf(STDOUT, "\t</instruction>\n");
    } else
        exit(23);
}

// Checks for these instruction cases:
// "DEFVAR" "POPS"
// Input:  counter $order, Instruction $opcode, array of args $array
// Output: printer XML code or error
function func_var($order,$opcode,$array)
{
    if (count($array) == 2) {

        // Checks correct var
        if (preg_match("/^TF@/", $array[1]) || preg_match("/^GF@/", $array[1]) || preg_match("/^LF@/", $array[1])) {
            $array[1] = check_string($array[1]);
            fprintf(STDOUT, "\t<instruction order=\"%d\" opcode=\"%s\">\n", $order, $opcode);
            fprintf(STDOUT, "\t\t<arg1 type=\"var\">%s</arg1>\n", $array[1]);
            fprintf(STDOUT, "\t</instruction>\n");
        } else
            exit(23);
    } else
        exit(23);
}

// Checks for these instruction cases:
// "CALL" "LABEL" "JUMP"
// Input:  counter $order, Instruction $opcode, array of args $array
// Output: printer XML code or error
function func_label($order, $opcode, $array)
{
    if (count($array) == 2) {
        // Checks correct label
        if (preg_match("/^TF@/", $array[1]) || preg_match("/^GF@/", $array[1]) || preg_match("/^LF@/", $array[1]) || preg_match("/^string@/", $array[1]) || preg_match("/^int@/", $array[1]) || preg_match("/^bool@/", $array[1]) || preg_match("/^nil@/", $array[1]))
            exit(23);
        $array[1] = check_string($array[1]);
        fprintf(STDOUT, "\t<instruction order=\"%d\" opcode=\"%s\">\n", $order, $opcode);
        fprintf(STDOUT, "\t\t<arg1 type=\"label\">%s</arg1>\n", $array[1]);
        fprintf(STDOUT, "\t</instruction>\n");
    } else
        exit(23);
}

// Checks for these instruction cases:
// "PUSHS" "WRITE" "DPRINT" "EXIT"
// Input:  counter $order, Instruction $opcode, array of args $array
// Output: printer XML code or error
function func_symb($order, $opcode, $array)
{
    if (count($array) == 2) {
        $leftRight = ["var", $array[1]];

        // Checks correct symb
        if (preg_match("/^TF@/", $array[1]) || preg_match("/^GF@/", $array[1]) || preg_match("/^LF@/", $array[1]) || preg_match("/^string@/", $array[1]) || preg_match("/^int@/", $array[1]) || preg_match("/^bool@/", $array[1]) || preg_match("/^nil@/", $array[1])) {
            if (preg_match("/^string@/", $array[1]) || preg_match("/^int@/", $array[1]) || preg_match("/^bool@/", $array[1]) || preg_match("/^nil@/", $array[1])) {
                $leftRight = preg_split("/[@]+/", $array[1], 2);
                if (preg_match("/^string@/", $array[1]))
                    $leftRight[1] = check_string($leftRight[1]);
                elseif (preg_match("/^int@/", $array[1]))
                    $leftRight[1] = check_int($leftRight[1]);
                elseif (preg_match("/^bool@/", $array[1]))
                    $leftRight[1] = check_bool($leftRight[1]);
            }

            fprintf(STDOUT, "\t<instruction order=\"%d\" opcode=\"%s\">\n", $order, $opcode);
            fprintf(STDOUT, "\t\t<arg1 type=\"%s\">%s</arg1>\n", $leftRight[0], $leftRight[1]);
            fprintf(STDOUT, "\t</instruction>\n");
        } else
            exit(23);
    } else
        exit(23);
}

// Checks for these instruction cases:
// "MOVE" "INT2CHAR" "NOT" "STRLEN" "TYPE"
// Input:  counter $order, Instruction $opcode, array of args $array
// Output: printer XML code or error
function func_var_symb($order, $opcode, $array)
{
    if (count($array) == 3) {
        $leftRight = ["var", $array[2]];

        // Checks correct var
        if (preg_match("/^TF@/", $array[1]) || preg_match("/^GF@/", $array[1]) || preg_match("/^LF@/", $array[1])) {
            $array[1] = check_string($array[1]);

            // Checks correct symb
            if (preg_match("/^TF@/", $array[2]) || preg_match("/^GF@/", $array[2]) || preg_match("/^LF@/", $array[2]) || preg_match("/^string@/", $array[2]) || preg_match("/^int@/", $array[2]) || preg_match("/^bool@/", $array[2]) || preg_match("/^nil@/", $array[2])) {
                if (preg_match("/^string@/", $array[2]) || preg_match("/^int@/", $array[2]) || preg_match("/^bool@/", $array[2]) || preg_match("/^nil@/", $array[2])) {
                    $leftRight = preg_split("/[@]+/", $array[2], 2);
                    if (preg_match("/^string@/", $array[2]))
                        $leftRight[1] = check_string($leftRight[1]);
                    elseif (preg_match("/^int@/", $array[2]))
                        $leftRight[1] = check_int($leftRight[1]);
                    elseif (preg_match("/^bool@/", $array[2]))
                        $leftRight[1] = check_bool($leftRight[1]);
                }

                fprintf(STDOUT, "\t<instruction order=\"%d\" opcode=\"%s\">\n", $order, $opcode);
                fprintf(STDOUT, "\t\t<arg1 type=\"var\">%s</arg1>\n", $array[1]);
                fprintf(STDOUT, "\t\t<arg2 type=\"%s\">%s</arg2>\n", $leftRight[0], $leftRight[1]);
                fprintf(STDOUT, "\t</instruction>\n");
            } else
                exit(23);
        } else
            exit(23);
    } else
        exit(23);
}

// Checks for these instruction cases:
// "READ"
// Input:  counter $order, Instruction $opcode, array of args $array
// Output: printer XML code or error
function func_var_type($order, $opcode, $array)
{
    if (count($array) == 3) {
        // Checks correct var
        if (preg_match("/^TF@/", $array[1]) || preg_match("/^GF@/", $array[1]) || preg_match("/^LF@/", $array[1])) {
            $array[1] = check_string($array[1]);

            // Checks correct type
            if ($array[2] != "string" && $array[2] != "int" && $array[2] != "bool")
                exit(23);
            fprintf(STDOUT, "\t<instruction order=\"%d\" opcode=\"%s\">\n", $order, $opcode);
            fprintf(STDOUT, "\t\t<arg1 type=\"var\">%s</arg1>\n", $array[1]);
            fprintf(STDOUT, "\t\t<arg2 type=\"type\">%s</arg2>\n", $array[2]);
            fprintf(STDOUT, "\t</instruction>\n");
        } else
            exit(23);
    } else
        exit(23);
}

// Checks for these instruction cases:
// "JUMPIFEQ" "JUMPIFNEQ"
// Input:  counter $order, Instruction $opcode, array of args $array
// Output: printer XML code or error
function func_label_symb_symb($order, $opcode, $array)
{
    if (count($array) == 4) {
        // Checks correct label
        if (preg_match("/^TF@/", $array[1]) || preg_match("/^GF@/", $array[1]) || preg_match("/^LF@/", $array[1]) || preg_match("/^string@/", $array[1]) || preg_match("/^int@/", $array[1]) || preg_match("/^bool@/", $array[1]) || preg_match("/^nil@/", $array[1]))
            exit(23);
        $leftRight1 = ["var", $array[2]];
        $leftRight2 = ["var", $array[3]];
        $array[1] = check_string($array[1]);

        // Checks correct symb
        if (preg_match("/^TF@/", $array[2]) || preg_match("/^GF@/", $array[2]) || preg_match("/^LF@/", $array[2]) || preg_match("/^string@/", $array[2]) || preg_match("/^int@/", $array[2]) || preg_match("/^bool@/", $array[2]) || preg_match("/^nil@/", $array[2])) {
            if (preg_match("/^string@/", $array[2]) || preg_match("/^int@/", $array[2]) || preg_match("/^bool@/", $array[2]) || preg_match("/^nil@/", $array[2])) {
                $leftRight1 = preg_split("/[@]+/", $array[2], 2);
                if (preg_match("/^string@/", $array[2]))
                    $leftRight1[1] = check_string($leftRight1[1]);
                elseif (preg_match("/^int@/", $array[2]))
                    $leftRight1[1] = check_int($leftRight1[1]);
                elseif (preg_match("/^bool@/", $array[2]))
                    $leftRight1[1] = check_bool($leftRight1[1]);
            }

            // Checks correct symb
            if (preg_match("/^TF@/", $array[3]) || preg_match("/^GF@/", $array[3]) || preg_match("/^LF@/", $array[3]) || preg_match("/^string@/", $array[3]) || preg_match("/^int@/", $array[3]) || preg_match("/^bool@/", $array[3]) || preg_match("/^nil@/", $array[3])) {
                if (preg_match("/^string@/", $array[3]) || preg_match("/^int@/", $array[3]) || preg_match("/^bool@/", $array[3]) || preg_match("/^nil@/", $array[3])) {
                    $leftRight2 = preg_split("/[@]+/", $array[3], 2);
                    if (preg_match("/^string@/", $array[3]))
                        $leftRight2[1] = check_string($leftRight2[1]);
                    elseif (preg_match("/^int@/", $array[3]))
                        $leftRight2[1] = check_int($leftRight2[1]);
                    elseif (preg_match("/^bool@/", $array[3]))
                        $leftRight2[1] = check_bool($leftRight2[1]);
                }

                fprintf(STDOUT, "\t<instruction order=\"%d\" opcode=\"%s\">\n", $order, $opcode);
                fprintf(STDOUT, "\t\t<arg1 type=\"label\">%s</arg1>\n", $array[1]);
                fprintf(STDOUT, "\t\t<arg2 type=\"%s\">%s</arg2>\n", $leftRight1[0], $leftRight1[1]);
                fprintf(STDOUT, "\t\t<arg3 type=\"%s\">%s</arg3>\n", $leftRight2[0], $leftRight2[1]);
                fprintf(STDOUT, "\t</instruction>\n");
            } else
                exit(23);
        } else
            exit(23);
    } else
        exit(23);
}

// Checks for these instruction cases:
// "ADD" "SUB" "MUL" "IDIV" "LT"
// "GT" "EQ" "AND" "OR"
// "STRI2INT" "CONCAT" "GETCHAR" "SETCHAR"
// Input:  counter $order, Instruction $opcode, array of args $array
// Output: printer XML code or error
function func_var_symb_symb($order, $opcode, $array)
{
    if (count($array) == 4) {
        // Checks correct var
        if (preg_match("/^TF@/", $array[1]) || preg_match("/^GF@/", $array[1]) || preg_match("/^LF@/", $array[1])) {
            $leftRight1 = ["var", $array[2]];
            $leftRight2 = ["var", $array[3]];
            $array[1] = check_string($array[1]);

            // Checks correct symb
            if (preg_match("/^TF@/", $array[2]) || preg_match("/^GF@/", $array[2]) || preg_match("/^LF@/", $array[2]) || preg_match("/^string@/", $array[2]) || preg_match("/^int@/", $array[2]) || preg_match("/^bool@/", $array[2]) || preg_match("/^nil@/", $array[2])) {
                if (preg_match("/^string@/", $array[2]) || preg_match("/^int@/", $array[2]) || preg_match("/^bool@/", $array[2]) || preg_match("/^nil@/", $array[2])) {
                    $leftRight1 = preg_split("/[@]+/", $array[2], 2);
                    if (preg_match("/^string@/", $array[2]))
                        $leftRight1[1] = check_string($leftRight1[1]);
                    elseif (preg_match("/^int@/", $array[2]))
                        $leftRight1[1] = check_int($leftRight1[1]);
                    elseif (preg_match("/^bool@/", $array[2]))
                        $leftRight1[1] = check_bool($leftRight1[1]);
                }

                // Checks correct symb
                if (preg_match("/^TF@/", $array[3]) || preg_match("/^GF@/", $array[3]) || preg_match("/^LF@/", $array[3]) || preg_match("/^string@/", $array[3]) || preg_match("/^int@/", $array[3]) || preg_match("/^bool@/", $array[3]) || preg_match("/^nil@/", $array[3])) {
                    if (preg_match("/^string@/", $array[3]) || preg_match("/^int@/", $array[3]) || preg_match("/^bool@/", $array[3]) || preg_match("/^nil@/", $array[3])) {
                        $leftRight2 = preg_split("/[@]+/", $array[3], 2);
                        if (preg_match("/^string@/", $array[3]))
                            $leftRight2[1] = check_string($leftRight2[1]);
                        elseif (preg_match("/^int@/", $array[3]))
                            $leftRight2[1] = check_int($leftRight2[1]);
                        elseif (preg_match("/^bool@/", $array[3]))
                            $leftRight2[1] = check_bool($leftRight2[1]);
                    }
                    fprintf(STDOUT, "\t<instruction order=\"%d\" opcode=\"%s\">\n", $order, $opcode);
                    fprintf(STDOUT, "\t\t<arg1 type=\"var\">%s</arg1>\n", $array[1]);
                    fprintf(STDOUT, "\t\t<arg2 type=\"%s\">%s</arg2>\n", $leftRight1[0], $leftRight1[1]);
                    fprintf(STDOUT, "\t\t<arg3 type=\"%s\">%s</arg3>\n", $leftRight2[0], $leftRight2[1]);
                    fprintf(STDOUT, "\t</instruction>\n");
                } else
                    exit(23);
            } else
                exit(23);
        } else
            exit(23);
    } else
        exit(23);
}

// Checks if integer is numeric
// Input:  $integer is type string
// Output: same input string or error
function check_int($integer)
{
    if (is_numeric($integer))
        return $integer;
    else
        exit(23);
}

// Checks the value of boolean
// Input:  $boolean is type string
// Output: same input string or error
function check_bool($boolean)
{
    if ($boolean == "true" || $boolean == "false")
        return $boolean;
    else
        exit(23);
}

// Replaces forbidden symbols in string
// Input:  $string is type string
// Output: same input string or modified string
function check_string($string)
{
    $string = str_replace("&", "&amp", $string);
    $string = str_replace("<", "&lt", $string);
    $string = str_replace(">", "&gt", $string);
    $string = str_replace("'", "&apos", $string);
    $string = str_replace('"', "&quot", $string);
    return $string;
}
//END-FUNCTIONS

?>

