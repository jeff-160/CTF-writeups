<?php

	function waf($data, $special = false, $len=96){
		
		$filtered = False;

		# length check
		if(strlen($data) > $len){
			$filtered = True;
		}
		#blacklist waf
		if(preg_match("/role|username|password|email|comment/is", $data)
                ){
			$filtered = True;
		}
		#blacklist waf
		if(preg_match("/limit|between|regexp|sounds|true|false|binary|not|file|rlike|div|group|by|having|union|mod|%|0b|0x|x'/is",$data)){
			$filtered = True;
		}

		#regdate injection filtering
		if(preg_match('/[0-9]{14}/is')){
			$filtered = True;
		}

		# whitelist waf
		if($special){
			if(!preg_match("/^[a-zA-Z0-9\x60\x27\x40\x20\x2e]+$/is", $data)){
				$filtered = True;
			}
		}else{
			if(!preg_match("/^[a-zA-Z0-9]+$/is",$data)){
				$filtered = True;
			}
		}

		if($filtered){
			alert("no hack!");
			die();
		}

                return $data;
        }

	function alert($msg){
		echo "<script>alert('$msg');</script>";
	}

        function location_alert($msg, $path){
                echo "<script>alert('$msg');location.href='$path';</script>";
        }
        
?>
