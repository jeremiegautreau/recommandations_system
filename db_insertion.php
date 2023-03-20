<?php
    
    function db_insertion($data){
        // test connection with database
        $servername = "localhost";
        $username = "root";
        $password = "jro35all!";

        try {
            $conn = new PDO("mysql:host=$servername;dbname=recosyst", $username, $password);
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            echo "Connected successfully";
        } 
        catch(PDOException $e) {
            echo "Connection failed: " . $e->getMessage();
        }

        // insertion of variables in database


        $sql = "INSERT INTO user (nom, prenom) VALUES (?,?)";
        $conn->prepare($sql)->execute([implode(", ", $data)]);

        $conn = null;    
    }  

?>