<?php
    
    function db_insertion($data){
        // test connection with database
        $servername = "localhost";
        $username = "root";
        $password = "jro35all!";

        try {
            $conn = new PDO("mysql:host=$servername;dbname=recosyst", $username, $password);
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
        } 
        catch(PDOException $e) {
            echo "Connection failed: " . $e->getMessage();
        }

        // insertion of variables in database

        $insert = array_values($data);

        //$conn->beginTransaction();

        $sql = "INSERT INTO user (nom, 
                                prenom,
                                m778,
                                m608,
                                m1527,
                                m3000,
                                m2324,
                                m2329,
                                m2028,
                                m2858,
                                m3147,
                                m2762,
                                m2571,
                                m2959,
                                m3578,
                                m3949,
                                m4011,
                                m7022,
                                m5618,
                                m4878,
                                m4963,
                                m27368,
                                m6502,
                                m27773,
                                m7153,
                                m6874,
                                m6711,
                                m6539,
                                m7254,
                                m7361,
                                m32587,
                                m33493,
                                m48780,
                                m44191,
                                m51255,
                                m54001,
                                m55247,
                                m58559,
                                m63082,
                                m64614,
                                m60069,
                                m79132,
                                m60684,
                                m72998,
                                m70286,
                                m52319,
                                m76251,
                                m92259,
                                m89745,
                                m96079,
                                m99114,
                                m109487
                                ) VALUES (
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?
                                    )"; 
        $conn->prepare($sql)->execute($insert);

        //$conn->commit();

        $conn = null;    
    }  

?>