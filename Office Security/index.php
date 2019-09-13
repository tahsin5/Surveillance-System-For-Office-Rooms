<html>
    <head>
<title>Office Security</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <link rel="stylesheet" href="style.css"> 
    </head>
    <body>
        
        <div class="container">
            
            <?php

$db = new SQLite3('example.db');

$create_table = $db->exec('CREATE TABLE IF NOT EXISTS intruders
                (id integer primary key, date text, time text, img text)');


$rows = $db->query("SELECT count(*) FROM intruders");
$row = $rows->fetchArray();
$numRows = $row['count(*)'];
            
if($numRows == 0){
    echo "<div class='page-header'><h2>No entries to show</h2></div>";
}else{
    
$ret = $db->query('SELECT * FROM intruders ORDER BY id DESC');

 echo "<table class='table'><tr><th>ID</th><th>DATE</th><th>TIME</th><th></th><th></th></tr>";
 while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
      $id = $row['id'];
      echo "<tr>";
      echo "<td>".$id. "</td>";
      echo "<td>".$row['date'] . "</td>";
      echo "<td>".$row['time'] . "</td>";
      $img = $row['img'];
      echo "<td><form method='post' action=''><button type='submit' class='btn btn-primary' name='view' value='$img'>View Image</button></form></td>";
      echo "<td><form method='post' action=''><button type='submit' class='btn btn-danger' name='delete' value='$id'>Delete Entry</button></form></td>";
      //echo "<td>".$row['img'] . "</td>";
      
      echo "</tr>";
      //echo "<br>";
   }
   echo "</table>";
   //echo "Operation done successfully\n";
   

if(isset($_POST['view'])){
    $file = $_POST['view'];
    $file = explode("y\\", $file);
    $img = $file[1];
    
header("Location: $img");

}
if(isset($_POST['delete'])){
    $id = $_POST['delete'];
    $ret = $db->exec("DELETE FROM intruders WHERE id= $id");
    
    echo "<script>window.open('index.php','_self')</script>";

}


}
$db->close();
?>
</div>
    </body>
</html>
