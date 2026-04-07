<?php
if (str_contains($lang, "index")) {
  $data = file_get_contents($lang);
  if ($data === false) {
    echo "An unexpected error has occured";
  }
  echo $data;
  exit;
}

include($lang);

?>