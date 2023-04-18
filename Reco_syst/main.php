<?php
    include 'retrieve_data.php'; // get function to retrieve data from forms
    include 'db_insertion.php'; // get function to insert data in database

    $data= retrieve_data(); // retrive data from html form

    db_insertion($data); // insert data in the database

    $name = $_POST["name"]; // get name from form
    $firstname = $_POST["firstname"]; // get firstname from form

    include 'testSiteRestitution.html'; // read html with the result of the recommandation

?>