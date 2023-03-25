<?php
    $command = escapeshellcmd("C:/Users/jerem/AppData/Local/Programs/Python/Python310/python.exe C:/lamp/htdocs/Reco_syst/reco_system_main.py");
    $reco = shell_exec($command);
    echo $reco; 
    ?>