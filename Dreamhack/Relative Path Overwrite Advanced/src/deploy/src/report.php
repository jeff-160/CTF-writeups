<?php
if(isset($_POST['path'])){
    exec(escapeshellcmd("python3 /bot.py " . escapeshellarg(base64_encode($_POST['path']))) . " 2>/dev/null &", $output);
    echo($output[0]);
}
?>

<form method="POST" class="form-inline">
    <div class="form-group">
        <label class="sr-only" for="path">/</label>
        <div class="input-group">
            <div class="input-group-addon">http://127.0.0.1/</div>
            <input type="text" class="form-control" id="path" name="path" placeholder="/">
        </div>
    </div>
    <button type="submit" class="btn btn-primary">Report</button>
</form>