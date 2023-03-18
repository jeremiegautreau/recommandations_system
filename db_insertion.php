<?php
    // test connection with database
    $servername = "localhost";
    $username = "root";
    $password = "jro35all!";

    try {
    $conn = new PDO("mysql:host=$servername;dbname=recosyst", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "Connected successfully";
    } catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
    }

    // test insertion of variable in database

    $nom ='Buffard';
    $prenom = 'Ludo';

    $sql = "INSERT INTO user (nom, prenom) VALUES (?,?)";
    $conn->prepare($sql)->execute([$nom, $prenom]);  

?>