
<?php
  $call_no = $_POST[ 'call_no' ];
      if ( is_null( $call_no ) ) {
        echo '<h1>Fail!</h1>';
      } else {
        $jb_conn = mysqli_connect( "192.168.0.7", "root", "1234", "FOBO");
        $jb_sql = "UPDATE call_time SET state = 'complete' WHERE ct_num = $call_no;";
        mysqli_query( $jb_conn, $jb_sql );
        echo '<script>alert("success!");</script>';
        echo '<script>location.href="index.php";</script>';
      }
    ?>