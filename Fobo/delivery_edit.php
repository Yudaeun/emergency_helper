<?php
  $del_num = $_POST[ 'del_num' ];
  $jb_conn = mysqli_connect( "192.168.0.7", "root", "1234", "FOBO");
  $jb_sql_edit = "SELECT * FROM delivery WHERE del_num = $del_num;";
  $jb_result = mysqli_query( $jb_conn, $jb_sql_edit );
  $jb_row = mysqli_fetch_array( $jb_result );
?>

<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <title>Edit Delivery</title>
    <style>
      body {
        font-family: Consolas, monospace;
        font-family: 12px;
      }
    </style>
  </head>
  <body>
    <h1>Edit Delivery</h1>
    <form action="del_update.php" method="POST">
      <input type="hidden" name="del_num" value="<?php echo $jb_row[ 'del_num' ]; ?>">
      <p>일련번호 <?php echo $jb_row[ 'del_num' ]; ?></p>
      <p>가구번호 <input type="text" name="house_num" value="<?php echo $jb_row[ 'house_num' ]; ?>" required></p>
      <p>배달 물품 <input type="text" name="del_goods" value="<?php echo $jb_row[ 'del_goods' ]; ?>" required></p>
      <p>상태 <select name="state" required>
        <option value="waiting" <?php if ( $jb_row[ 'state' ] == 'waiting' ) { echo 'selected'; } ?>>waiting</option>
        <option value="complete" <?php if ( $jb_row[ 'state' ] == 'complete' ) { echo 'selected'; } ?>>complete</option>
      </select></p>
      <p>운송장번호 <input type="text" name="tracking_num" value="<?php echo $jb_row[ 'tracking_num' ]; ?>" required></p>
      <p>택배사 <input type="text" name="courier" value="<?php echo $jb_row[ 'courier' ]; ?>" required></p>
      <button>Edit</button>
    </form>
  </body>
</html>