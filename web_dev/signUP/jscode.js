function validateSubmit(){
    var textbox_SID = document.getElementById("SID");
    var textbox_LastName = document.getElementById("LastName");
    var textbox_phone = document.getElementById("Phone");
    if (textbox_SID.value.length != 10){
        alert("SID should be 10 digits long.");
        return false;
    }
    if (textbox_LastName.value == ""){
        alert("Please input your last name.");
        return false;
    }
    if (textbox_phone.value == ""){
        alert("Please put something in \"Phone Number\" field.");
        return false;
    }
    
}
