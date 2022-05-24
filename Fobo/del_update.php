

<?php
      $del_num = $_POST[ 'del_num' ];
      $house_num = $_POST[ 'house_num' ];
      $del_goods = $_POST[ 'del_goods' ];
      $state = $_POST[ 'state' ];
      $tracking_num = $_POST[ 'tracking_num' ];
      $courier = $_POST[ 'courier' ];
      if ( is_null( $del_num ) ) {
        echo '<script>alert("Fail!");</script>';
      } else {
        $jb_conn = mysqli_connect( "192.168.0.7", "root", "1234", "FOBO");
        $jb_sql = "UPDATE delivery SET del_num = '$del_num', house_num = '$house_num', del_goods = '$del_goods', state = '$state', tracking_num = '$tracking_num',courier='$courier' WHERE del_num = $del_num;";
        mysqli_query( $jb_conn, $jb_sql );
        echo '<script>alert("success!");</script>';
        echo '<script>location.href="delivery.php";</script>';      }
    ?>