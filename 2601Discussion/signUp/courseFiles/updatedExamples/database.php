<?php

$user_name = "root";
$password = "";
$database = "addressbook";
$server = "127.0.0.1";
$db_handle = mysqli_connect($server, $user_name, $password, $database);
if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}

$sql = "select * from tbl_address_book";
$result = mysqli_query($db_handle, $sql);
if (!$result) {
    printf("Could not successfully run query ($sql) from DB: " . mysql_error());
    exit();
}
while ($db_field = mysqli_fetch_assoc($result)) {
    print $db_field['ID'] . "<br>";
    print $db_field['First_Name'] . "<br>";
    print $db_field['Surname'] . "<br>";
    print $db_field['Address'] . "<br>";
}
mysqli_close($db_handle);
?>