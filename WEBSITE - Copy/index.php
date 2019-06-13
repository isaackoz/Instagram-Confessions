<?php
ini_set( "display_errors", 0); 

if(isset($_POST['submit'])){
	$privkey = "PRIVATE-KEY-GOES-HERE";
	$resKey = $_POST['g-recaptcha-response'];
	$userIP = $_SERVER['REMOTE_ADDR'];
	$url = "https://www.google.com/recaptcha/api/siteverify?secret=$privkey&response=$resKey&remoteip=$userIP";
	$response = json_decode(file_get_contents($url));
	
	$confession = $_POST['confession'];
	$username = $_POST['first_name'];
	$string_exp = "/^[A-Za-z .'-]+$/";
	
	if($response->success){
		
		function died($error) {
			echo '<script type="text/javascript">alert("Error '.$error.' please correct these errors.");window.history.back();</script>';
			die();
		}
		
		
		if(!isset($username) || !isset($confession)){
			died('username or confession is invalid');
		}
		if(!preg_match($string_exp,$username)) {
			died('Username you entered does not appear to be valid. ');
		}

		
		$brosnan = $userIP.'ยง'.$username.' says: '.$confession;
		$addr = 'SERVER-IP-ADDRESS-GOES-HERE';
		$port = 47225;
		
		$sock = socket_create(AF_INET, SOCK_STREAM, 0);
		socket_connect($sock, $addr, $port) or die('Bot down');
		socket_write($sock, $brosnan);
		socket_close($sock);
		
		echo '<script type="text/javascript">alert("Confession submitted to the queue!");</script>';
		}
		
	else
		echo '<script type="text/javascript">alert("Captcha failed!!");</script>';
}

?>

<!doctype html>
<html>
  <head>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://www.google.com/recaptcha/api.js" async defer></script>
	

  </head>
<body>

	<form id="contactForm" style="font-size:14px;font-family:'Roboto',Arial,Helvetica,sans-serif;color:#34495E;max-width:100%;min-width:30%" name="htmlform" method="post" action="index.php">
		<label id="warningLabel"><b><font size = "30">What is your confession? <br/></font></b></label>	
		<label <font size = "10">Due to instagram's limitations, confessions are posted every 65 seconds. Once you submit your confession, your confession will be placed in the queue. Please wait patiently.
		<div class="element-input"><label class="title"><span class="required">*</span></label><div class="item-cont"><input id ="inputBox" type="text" name="first_name" required="required" maxlength="30" placeholder="Username"/><span class="icon-place"></span></div></div>
		<div class="element-input"><label class="title"><span class="required">*</span></label><div class="item-cont"><textarea id ="textBox" style="resize:none" type="text" name="confession" required="required" maxlength="600" cols = "40" rows = "10" placeholder="Confession"></textarea><span class="icon-place"></span></div></div>
		<div class="g-recaptcha" data-sitekey="CAPTCHA-PUBLIC-KEY-GOES-HERE"></div>
		<div class="submit" ><input name="submit" style="width: 300px" type="submit" value="Confess!"/></div>
		<label>The content submitted is not monitored and is fully automatic. By clicking 'Confess!' you agree to not share any information that is illegal or harmful to others.
		<!-- lol thats a lie ^^-->
	</form>

</body>
</html>

