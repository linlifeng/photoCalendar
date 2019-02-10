<html>
    <?php
    $dates = $_POST['date'];
    $url = $_POST['url'];
    $y = explode('-', $dates)[0];
    $m = explode('-', $dates)[1];
    $d = explode('-', $dates)[2];
    $current = $_POST['current'];
    //$fname = "$m" . str_replace('0','',$d) . "$y" . ".jpg";
    $sd = ltrim($d, '0');
    $fname = "$m" . "$sd" . "$y" . ".jpg";


if($_FILES['image']['type'] != "image/jpeg") {
    echo "Only jpg/jpeg images are allowed!";
    exit;
}


/*the code below is supposedly safer but does not work for mobile uploads
$verifyimg = getimagesize($_FILES['image']['tmp_name']);

if($verifyimg['mime'] != 'image/jpeg') {
    echo $verifyimg['mime'];
    echo "Only jpg images are allowed!";
    exit;
}
*/

$uploaddir = 'photos/';

//$uploadfile = $uploaddir . basename($_FILES['image']['name']);
$uploadfile = $uploaddir . $fname;
if (move_uploaded_file($_FILES['image']['tmp_name'], $uploadfile)) {
    echo "Image succesfully uploaded.";
    shell_exec("convert -thumbnail 200 ".$uploadfile." ".$uploaddir."thumb-".$fname);
    if($current=='on'){
        shell_exec("cp ".$uploadfile." ".$uploaddir."image.jpg");
        shell_exec("convert -blur 0x8 ".$uploaddir."image.jpg ".$uploaddir."image-blur.jpg");
        shell_exec("convert ".$uploaddir."image-blur.jpg -fill white -colorize 50%  ".$uploaddir."image-blur-whiten.jpg");
        shell_exec("mv ".$uploaddir."image-blur-whiten.jpg ".$uploaddir."image-blur.jpg");
        echo "<br/>background reset.";
    }
} else {
    echo $uploadfile."<br/>";
    echo "Image uploading failed.";
}
?>


</html>
