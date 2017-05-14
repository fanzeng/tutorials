<?PHP
include 'sqlSurvey.php';
// session_start();
if ((isset($_SESSION['hasVoted']))) {
    if ($_SESSION['hasVoted'] = '1') {
        print "You've already voted";
    }
} else {
    if (isset($_GET['Submit1']) && isset($_GET['q'])) {

        $selected_radio = $_GET['q'];

        $user_name = "root";
        $password = "";
        $database = "surveyTest";
        $server = "127.0.0.1";

        $db_handle = mysqli_connect($server, $user_name, $password, $database);
        if (mysqli_connect_errno()) {
            printf("Connect failed: %s\n", mysqli_connect_error());
            exit();
        }


        $_SESSION['hasVoted'] = '1';
        $SQL = "UPDATE answers SET $selected_radio = $selected_radio + 1 WHERE answers.QID = '$qNum' ";

        $result = mysqli_query($db_handle, $SQL);
        if (!$result) {
            print "Update failed. Error is";
            echo mysqli_errno($db_handle)  . ": " .  mysqli_error($db_handle);
        } else {
            print "Thanks for voting!";
        }
        mysqli_close($db_handle);
    } else {
        print "You didn't selected a voting option!";
    }
}
?>

<html>
    <head>
        <title>Process Survey</title>
    </head>



    <body>

    </body>
</html>

