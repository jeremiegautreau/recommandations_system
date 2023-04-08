<?php
    include 'retrieve_data.php'; // Get function to retrieve data from forms
    include 'db_insertion.php'; // Get function to insert data in database

    $data= retrieve_data(); // retrive data from html form

    db_insertion($data); // insert data in the database

    include 'result_reco.html'; // read html with the result of the recommandation

?>