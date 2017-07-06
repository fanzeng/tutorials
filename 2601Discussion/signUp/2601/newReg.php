<?PHP
$SID = "";
$LastName = "";
$FirstName = "";
$DiscussionSess = "";
$Phone = "";
$errorMessage = "";
$Quota = 5;
$Remain = array();

//==========================================
//	ESCAPE DANGEROUS SQL CHARACTERS
//==========================================
function quote_smart($value, $handle) {

    if (get_magic_quotes_gpc()) {
        $value = stripslashes($value);
    }

    if (!is_numeric($value)) {
        $value = "'" . mysqli_real_escape_string($handle, $value) . "'";
    }
    return $value;
}

//==========================================
//	GET NUMBER OF PEOPLE REGISTERED
//==========================================
function getRegNum($db_handle, $DiscussionSess) {
    $SQL = "SELECT * FROM DiscussionReg WHERE DiscussionSess = $DiscussionSess";
    $result = mysqli_query($db_handle, $SQL);
    if ($result) {
        $num_rows = mysqli_num_rows($result);
        return $num_rows;
    } else {
        $err_msg = mysqli_errno($db_handle) . ": " . mysqli_error($db_handle) . "\n";
        echo $err_msg;
        logging('getRegNum', $err_msg, '$err_msg', $whichlog = 'ERROR');
        return -1;
    }
}

//==========================================
//	CHECK IF A SESSION IS FULL
//==========================================
function is_session_full($db_handle, $DiscussionSess, $Quota) {
    if ($DiscussionSess != "") {
        if (getRegNum($db_handle, $DiscussionSess) < $Quota) {
            return FALSE;
        } else {
            return TRUE;
        }
    } else {
        return FALSE;
    }
}

//==========================================
//	CHECK IF IT IS THE SAME PERSON
//==========================================
function is_same_person($db_handle, $result, $FirstName, $LastName, $Phone) {
    mysqli_data_seek($result, 0);
    $db_field = mysqli_fetch_assoc($result);
    $FirstName_record = quote_smart($db_field['FirstName'], $db_handle);
    $LastName_record = quote_smart($db_field['LastName'], $db_handle);
    $Phone_record = quote_smart($db_field['Phone'], $db_handle);
    if ($FirstName == $FirstName_record && $LastName == $LastName_record && $Phone == $Phone_record) {
        return TRUE;
    } else {
        return FALSE;
    }
}

//==========================================
//	CHECK IF IT IS THE SAME CHOICE
//==========================================
function is_same_choice($db_handle, $result, $DiscussionSess) {
    mysqli_data_seek($result, 0);
    $db_field = mysqli_fetch_assoc($result);
    $DiscussionSess_record = quote_smart($db_field['DiscussionSess'], $db_handle);
    if ($DiscussionSess == $DiscussionSess_record) {
        return TRUE;
    } else {
        return FALSE;
    }
}

//==========================================
//	CHECK IF INFO INPUT BY USER IS IN COURSE RECORD
//==========================================
function is_info_valid($db_handle, $SID, $LastName) {
    $SQL = "SELECT * FROM SID_LastName_List WHERE SID = $SID";
    logging($SID, $SQL, '$SQL', $whichlog = 'SQL');
    $result = mysqli_query($db_handle, $SQL);
    if ($result) {
        $num_rows = mysqli_num_rows($result);
        if ($num_rows == 0) {
            return FALSE;
        }
        mysqli_data_seek($result, 0);
        $db_field = mysqli_fetch_assoc($result);

        $LastName = str_replace(' ', '', $LastName);
        if ($LastName == quote_smart($db_field['LastName'], $db_handle)) {
            return TRUE;
        }
    } else {
        $err_msg = "Connection error. Please retry.";
        echo $err_msg;
        logging('$result FALSE in is_info_valid. ', $err_msg, '$err_msg', $whichlog = 'ERROR');
    }
    return FALSE;
}

//==========================================
//	LOGGING THE EVENTS
//==========================================
function logging($SID, $data, $msg, $which_log) {
    $date = date_create("now", timezone_open('Asia/Hong_Kong'));
    $path = ".//log//";
    $file_name = date_format($date, 'y-m-d') . '_' . $which_log . '.log';
    $log_file_name = $path . $file_name;
    if (!file_exists($log_file_name)) {
        fclose(fopen($log_file_name, "w"));
        chmod($log_file_name, 0700);
    }

    $file_handle = fopen($log_file_name, "a");
    $file_contents = date_format($date, 'r') . ': ' . $SID . ':' . $msg . "\n" . print_r($data, TRUE) . "\n";

    fwrite($file_handle, $file_contents);
    fclose($file_handle);
}

//==========================================
//	COMFIRM USER WANTS TO MODIFY
//==========================================
function confirm_modify($result, $DiscussionSess_New) {
    mysqli_data_seek($result, 0);
    $db_field = mysqli_fetch_assoc($result);
    $message = "Click OK to change to session " . $DiscussionSess_New . ". Click Cancel to Cancel";
    logging($db_field['SID'], $message, '$message', $whichlog = 'MSG');
    $url = '"newReg.php"';
    $param = '"' . "?SID=" . $db_field['SID'] . '&FirstName=' . $db_field['FirstName'] . '&LastName=' . $db_field['LastName'] . '&DiscussionSess=' . $DiscussionSess_New . '&Phone=' . $db_field['Phone'] . '"';
    print("<script type='text/javascript'>"
            . "if (confirm('$message')){"
            . "window.location.href = $url + $param; "
            . "}else{"
            . "window.location.href = $url;"
            . "}"
            . "</script>");
}

//==========================================
//	INSERT NEW OR MODIFY EXISTING DATA
//==========================================
function insert_data($db_handle, $SQL, $SID) {

    $result = mysqli_query($db_handle, $SQL);

    if ($result) {
        $message = "Good. Success. Thank you!";
        logging($SID, $message, '$message', $whichlog = 'MSG');
        print("<script type='text/javascript'>"
                . "alert('$message');"
                . "window.location.replace('newReg.php');"
                . "</script>");
    } else {
        $err_msg = mysqli_errno($db_handle) . ": " . mysqli_error($db_handle) . "\n";
        echo $err_msg;
        logging('insert_data', $err_msg, '$err_msg', $whichlog = 'ERROR');
    }
}

//==========================================
//	THE PROGRAM STARTS HERE
//==========================================
//
//==========================================
//	CONNECT TO THE DATABASE
//==========================================
$user_name = "2271317_discussion";
$password = trim(file_get_contents("babyFile"));
$database = "2271317_discussion";
$server = "fdb12.biz.nf";
$db_handle = mysqli_connect($server, $user_name, $password, $database);
if (mysqli_connect_errno()) {
    $err_msg = "Connect failed:" . mysqli_connect_error() . "\n";
    echo $err_msg;
    logging('CONNECT TO THE DATABASE', $err_msg, '$err_msg', $whichlog = 'ERROR');
    exit();
}
//==========================================
//	CALCULATE REMAINING SEATS
//==========================================
for ($i = 1; $i <= 25; $i++) {
    $Remain[$i] = $Quota - getRegNum($db_handle, $i);
}


//==========================================
//	IF THE FORM IS SUBMITTED BY USER CLICKING BUTTON
//==========================================
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $_POST = array_map('htmlspecialchars', $_POST);
    foreach ($_POST as &$POST_var) {
        $POST_var = quote_smart($POST_var, $db_handle);
    }
    unset($POST_var);
    $SID = $_POST['SID'];
    $FirstName = $_POST['FirstName'];
    $LastName = $_POST['LastName'];
    $DiscussionSess = $_POST['DiscussionSess'];
    $Phone = $_POST['Phone'];

//    $referrer = $_SERVER['HTTP_REFERER'];
//    $browser = $_SERVER['HTTP_USER_AGENT'];
//    $ipAddress = $_SERVER['REMOTE_ADDR'];
//
//    print "Referrer = " . $referrer . "<BR>";
//    print "Browser = " . $browser . "<BR>";
//    print "IP Adress = " . $ipAddress;

    logging($SID, $_POST, '$_POST', $whichlog = 'HTTP');
    logging($SID, $_SERVER, '$_SERVER', $whichlog = 'HTTP');
    $SQL = "SELECT * FROM DiscussionReg WHERE SID = $SID";
    logging($SID, $SQL, '$SQL', $whichlog = 'SQL');
    $result = mysqli_query($db_handle, $SQL);


//====================================================
//	CHECK TO SEE IF THE $result VARIABLE IS TRUE
//====================================================

    if ($result) {
        $num_rows = mysqli_num_rows($result);

//====================================================
//	IF THE "SUBMIT" BUTTON IS CLICKED
//====================================================

        if (isset($_POST['SubmitBtn'])) {
            if ($num_rows > 0) {
                if (is_same_person($db_handle, $result, $FirstName, $LastName, $Phone)) {
                    if (is_same_choice($db_handle, $result, $DiscussionSess)) {
                        $message = "Yes, you\'re already enrolled in session " . $DiscussionSess . ".";
                        logging($SID, $message, '$message', $whichlog = 'MSG');
                        print("<script type='text/javascript'>"
                                . "alert('$message');"
                                . "window.location.replace('newReg.php');"
                                . "</script>");
                    } else {
                        confirm_modify($result, $DiscussionSess);
                    }
                } else {
                    $message = "Error. Your SID has already registered.";
                    logging($SID, $message, '$message', $whichlog = 'MSG');
                    print("<script type='text/javascript'>"
                            . "alert('$message');"
                            . "window.location.replace('newReg.php');"
                            . "</script>");
                }
            } else if (is_session_full($db_handle, $DiscussionSess, $Quota)) {
                $message = "Sorry, session full. Please pick another.";
                logging($SID, $message, '$message', $whichlog = 'MSG');
                print("<script type='text/javascript'>"
                        . "alert('$message');"
                        . "window.location.replace('newReg.php');"
                        . "</script>");
            } else if (!is_info_valid($db_handle, $SID, $LastName)) {
                $message = "Sorry, the information you\'ve input is not correct.";
                logging($SID, $message, '$message', $whichlog = 'MSG');
                print("<script type='text/javascript'>"
                        . "alert('$message');"
                        . "window.location.replace('newReg.php');"
                        . "</script>");
            } else if ($DiscussionSess == "") {
                $message = "You haven\'t selected any session.";
                logging($SID, $message, '$message', $whichlog = 'MSG');
                print("<script type='text/javascript'>"
                        . "alert('$message');"
                        . "window.location.replace('newReg.php');"
                        . "</script>");
            } else {
                $SQL = "INSERT INTO `DiscussionReg` "
                        . "(`SID`, `FirstName`, `LastName`, `DiscussionSess`, `Phone`)"
                        . " VALUES ($SID, $FirstName, $LastName,"
                        . " $DiscussionSess, $Phone)";
                insert_data($db_handle, $SQL, $SID);
                logging($SID, $SQL, '$SQL', $whichlog = 'SQL');
            }
        }

//====================================================
//	IF THE "CHECK" BUTTON IS CLICKED
//====================================================        
        else {
            if ($num_rows > 0) {
                if (is_same_person($db_handle, $result, $FirstName, $LastName, $Phone)) {
                    mysqli_data_seek($result, 0);
                    $db_field = mysqli_fetch_assoc($result);
                    $DiscussionSess_record = quote_smart($db_field['DiscussionSess'], $db_handle);
                    $message = "According to record, you\'ve registered session " . $DiscussionSess_record;
                    logging($SID, $message, '$message', $whichlog = 'MSG');
                    print("<script type='text/javascript'>"
                            . "alert('$message');"
                            . "window.location.replace('newReg.php');"
                            . "</script>");
                } else {
                    $message = "Your information is not entered correctly." . $DiscussionSess_record;
                    logging($SID, $message, '$message', $whichlog = 'MSG');
                    print("<script type='text/javascript'>"
                            . "alert('$message');"
                            . "window.location.replace('newReg.php');"
                            . "</script>");
                }
            } else {
                $message = "No record found. Maybe you haven\'t registered.";
                logging($SID, $message, '$message', $whichlog = 'MSG');
                print("<script type='text/javascript'>"
                        . "alert('$message');"
                        . "window.location.replace('newReg.php');"
                        . "</script>");
            }
        }
    }

//==========================================
//	IF $result IS FALSE
//==========================================    
    else {

        $err_msg = "Connection error. Please retry.";
        echo $err_msg;
        logging('$result FALSE in POST (submitted by javascript) case. ', $err_msg, '$err_msg', $whichlog = 'ERROR');
    }
}


//==========================================
//	IF THE FORM IS SUBMITTED BY JS
//==========================================
else if ($_SERVER['REQUEST_METHOD'] == 'GET' && isset($_GET['SID'])) {
    $_GET = array_map('htmlspecialchars', $_GET);
    foreach ($_GET as &$GET_var) {
        $GET_var = quote_smart($GET_var, $db_handle);
    }
    unset($GET_var);
    $SID = $_GET['SID'];
    $FirstName = $_GET['FirstName'];
    $LastName = $_GET['LastName'];
    $DiscussionSess = $_GET['DiscussionSess'];
    $Phone = $_GET['Phone'];
    logging($SID, $_GET, '$_GET', $whichlog = 'HTTP');
    logging($SID, $_SERVER, '$_SERVER', $whichlog = 'HTTP');
    $SQL = "SELECT * FROM DiscussionReg WHERE SID = $SID";
    logging($SID, $SQL, '$SQL', $whichlog = 'SQL');

    $result = mysqli_query($db_handle, $SQL);
    if ($result) {
        $num_rows = mysqli_num_rows($result);
        if ($num_rows > 0) {
            if (is_same_person($db_handle, $result, $FirstName, $LastName, $Phone)) {
                if (is_same_choice($db_handle, $result, $DiscussionSess)) {
                    $message = "Yes, you\'re already enrolled in session " . $DiscussionSess . ".";
                    logging($SID, $message, '$message', $whichlog = 'MSG');
                    print("<script type='text/javascript'>"
                            . "alert('$message');"
                            . "window.location.replace('newReg.php');"
                            . "</script>");
                } else if (is_session_full($db_handle, $DiscussionSess, $Quota)) {
                    $message = "Sorry, session full. Please pick another.";
                    logging($SID, $message, '$message', $whichlog = 'MSG');
                    print("<script type='text/javascript'>"
                            . "alert('$message');"
                            . "window.location.replace('newReg.php');"
                            . "</script>");
                } else {
                    $SQL = "UPDATE `DiscussionReg` "
                            . "SET `DiscussionSess` = $DiscussionSess"
                            . " WHERE `DiscussionReg`.`SID` = $SID";

                    insert_data($db_handle, $SQL, $SID);
                    logging($SID, $SQL, '$SQL', $whichlog = 'SQL');
                }
            } else {
                $message = "No wait, your SID is registered.";
                logging($SID, $message, '$message', $whichlog = 'MSG');
                print("<script type='text/javascript'>"
                        . "alert('$message');"
                        . "window.location.replace('newReg.php');"
                        . "</script>");
            }
        }
    }


//==========================================
//	IF $result IS FALSE
//==========================================
    else {

        $err_msg = "Connection error. Please retry.";
        echo $err_msg;
        logging('$result FALSE in GET (submitted by javascript) case. ', $err_msg, '$err_msg', $whichlog = 'ERROR');
    }
}
mysqli_close($db_handle);
?>


<html>
    <head>
        <title>Discussion Sign Up</title>
        <link rel = "stylesheet" type = "text/css" href = "StyleSheet.css">
    </head>
    <body>
        <form NAME = "form1" METHOD = "POST" ACTION = "newReg.php" id = "theForm" onsubmit = "return validateSubmit();">
            
            <div class = "row">
                <label for = "SID">SID: </label> <input TYPE = 'TEXT' Name = 'SID' id = "SID" value = "<?PHP print $SID; ?>" maxlength = "10">&nbsp;Input your 10-digit SID, e.g. <span class = "eg">1155000000</span>
            </div>
            <div class = "row">
                <label for = "FirstName">First Name: </label><input TYPE = 'TEXT' Name = 'FirstName' id = "FirstName"  value = "<?PHP print $FirstName; ?>" maxlength = "16">&nbsp;Input your first name, e.g. <span class = "eg">Tai Man</span>
            </div>
            <div class = "row">
                <label for = "LastName">Last Name: </label><input TYPE = 'TEXT' Name = 'LastName' id = "LastName" value = "<?PHP print $LastName; ?>" maxlength = "16">&nbsp;Input your last name in BLOCK LETTERS, e.g. <span class = "eg">CHAN</span>
            </div>
            <div class = "row">
                <label for = "DiscussionSessTbl">Discussion Session: </label>
            
            <table id = "DiscussionSessTbl">
                <thead style = "display:table-header-group">
                    <tr>
                        <th id='th1'>Topic No.</th>
                        <th id='th2'>Topic</th>
                        <!--<th id='th3'>Tutor in charge</th>-->
                        <th id='th4'>2:30 - 2:50</th>
                        <th id='th5'>2:50 - 3:10</th>
                        <th id='th6'>3:10 - 3:30</th>
                        <th id='th7'>3:30 - 3:50</th>
                        <th id='th8'>3:50 - 4:10</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td headers="th1">1</td>
                        <td headers="th2">Technology's Impact on Society</td>
                        <!--<td headers="th3">Kunyu Zhang</td>-->
                        <td headers="th4"><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '1' <?php echo $Remain[1]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[1] ?>)</span>&nbsp;01.Cantonese</td>
                        <td headers="th5"><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '2' <?php echo $Remain[2]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[2] ?>)</span>&nbsp;02.Cantonese</td>
                        <td headers="th6"><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '3' <?php echo $Remain[3]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[3] ?>)</span>&nbsp;03.English</td>
                        <td headers="th7"><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '4' <?php echo $Remain[4]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[4] ?>)</span>&nbsp;04.English</td>
                        <td headers="th8"><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '5' <?php echo $Remain[5]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[5] ?>)</span>&nbsp;05.Mandarin</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>Careers in Engineering</td>
                        <!--<td>Fan Zeng</td>-->
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '6' <?php echo $Remain[6]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[6] ?>)</span>&nbsp;06.Cantonese</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '7' <?php echo $Remain[7]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[7] ?>)</span>&nbsp;07.Cantonese</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '8' <?php echo $Remain[8]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[8] ?>)</span>&nbsp;08.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '9' <?php echo $Remain[9]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[9] ?>)</span>&nbsp;09.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '10' <?php echo $Remain[10]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[10] ?>)</span>&nbsp;10.Mandarin</td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>Hijacked Plane Dilemma</td>
                        <!--<td>Ye Bian</td>-->
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '11' <?php echo $Remain[11]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[11] ?>)</span>&nbsp;11.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '12' <?php echo $Remain[12]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[12] ?>)</span>&nbsp;12.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '13' <?php echo $Remain[13]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[13] ?>)</span>&nbsp;13.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '14' <?php echo $Remain[14]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[14] ?>)</span>&nbsp;14.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '15' <?php echo $Remain[15]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[15] ?>)</span>&nbsp;15.Mandarin</td>
                    </tr>
                    <tr>
                        <td>4</td>
                        <td>Engineering Design</td>
                        <!--<td>Xiayi Xu</td>-->
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '16' <?php echo $Remain[16]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[16] ?>)</span>&nbsp;16.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '17' <?php echo $Remain[17]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[17] ?>)</span>&nbsp;17.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '18' <?php echo $Remain[18]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[18] ?>)</span>&nbsp;18.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '19' <?php echo $Remain[19]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[19] ?>)</span>&nbsp;19.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '20' <?php echo $Remain[20]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[20] ?>)</span>&nbsp;20.Mandarin</td>
                    </tr>
                    <tr>
                        <td>5</td>
                        <td>Nuclear Energy</td>
                        <!--<td>Qianyi Xu</td>-->
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '21' <?php echo $Remain[21]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[21] ?>)</span>&nbsp;21.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '22' <?php echo $Remain[22]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[22] ?>)</span>&nbsp;22.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '23' <?php echo $Remain[23]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[23] ?>)</span>&nbsp;23.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '24' <?php echo $Remain[24]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[24] ?>)</span>&nbsp;24.English</td>
                        <td><INPUT TYPE = 'Radio' Name = 'DiscussionSess' value = '25' <?php echo $Remain[25]>0?"enabled":"disabled";?>><span class = "remain">(<?php echo $Remain[25] ?>)</span>&nbsp;25.Mandarin</td>
                    </tr>
                </tbody>
            </table> 
            </div>
            
            <div class = "row">
                <label for = "Phone">Phone Number: </label><input TYPE = 'TEXT' Name = 'Phone' id = "Phone" value = "<?PHP print $Phone; ?>" maxlength="16">&nbsp;Input your phone number as identity token. Please remember what you've put. You'll need to provide this if you want to modify registration later.<br>
            </div>
            <div class = "row">
                <label for = "SubmitBtn">Select a Choice: </label>
            <P align = left>
                <INPUT TYPE = "Submit" Name = "SubmitBtn" class = "button" id = "SubmitBtn " VALUE = "New/Modify Registration">
                <INPUT TYPE = "Submit" Name = "CheckBtn" class = "button" VALUE = "Check My Registration">
            </P>
            </div>
        </FORM>

            <?PHP print $errorMessage; ?>
            <script src = "jscode.js"></script>
    </body>
</html>