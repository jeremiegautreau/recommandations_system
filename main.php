<?php
    include 'retrieve_data.php';
    include 'db_insertion.php';

    $data= retrieve_data();

    db_insertion($data);

    include 'result_reco.html';

?>