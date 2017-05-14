<?PHP
$uname = "";
$pword = "";
$errorMessage = "";

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

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $uname = $_POST['username'];
    $pword = $_POST['password'];

    $uname = htmlspecialchars($uname);
    $pword = htmlspecialchars($pword);

    //==========================================
    //	CONNECT TO THE LOCAL DATABASE
    //==========================================
    $user_name = "root";
    $pass_word = "";
    $database = "login";
    $server = "127.0.0.1";
    $db_handle = mysqli_connect($server, $user_name, $password, $database);
    if (mysqli_connect_errno()) {
        printf("Connect failed: %s\n", mysqli_connect_error());
        exit();
    }

    $uname = quote_smart($uname, $db_handle);
    $pword = quote_smart($pword, $db_handle);

    $SQL = "SELECT * FROM login WHERE L1 = $uname AND L2 = md5($pword)";
    $result = mysqli_query($db_handle, $SQL);
    $num_rows = mysqli_num_rows($result);

    //====================================================
    //	CHECK TO SEE IF THE $result VARIABLE IS TRUE
    //====================================================

    if ($result) {
        if ($num_rows > 0) {
            session_start();
            $_SESSION['login'] = "1";
            header("Location: page1.php");
        } else {
            session_start();
            $_SESSION['login'] = "";
            header("Location: signup.php");
        }
    } else {
        $errorMessage = "Error logging on";
    }

    mysqli_close($db_handle);
}
?>


<html>
    <head>
        <title>Basic Login Script</title>
    </head>
    <body>

        <FORM NAME ="form1" METHOD ="POST" ACTION ="login.php">

            Username: <INPUT TYPE = 'TEXT' Name ='username'  value="<?PHP print $uname; ?>" maxlength="20">
            Password: <INPUT TYPE = 'TEXT' Name ='password'  value="<?PHP print $pword; ?>" maxlength="16">

            <P align = center>
                <INPUT TYPE = "Submit" Name = "Submit1"  VALUE = "Login">
            </P>

        </FORM>

        <P>
<?PHP print $errorMessage; ?>




    </body>
</html>