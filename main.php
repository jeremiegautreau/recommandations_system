<?php
    include 'retrieve_data.php';
    include 'db_insertion.php';

    $data= retrieve_data();

    db_insertion($data);
    
    include "formulaire.html";

    // readfile("result_reco.html");

    // $reco = shell_exec("reco_system_main.py");


?>