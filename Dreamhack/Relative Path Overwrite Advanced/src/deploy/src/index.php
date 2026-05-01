<html>
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
<title>Relative-Path-Overwrite-Advanced</title>
</head>
<body>
    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">Relative-Path-Overwrite-Advanced</a>
        </div>
        <div id="navbar">
          <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="/?page=vuln&param=dreamhack">Vuln page</a></li>
            <li><a href="/?page=report">Report</a></li>
          </ul>

        </div><!--/.nav-collapse -->
      </div>
    </nav><br/><br/><br/>
    <div class="container">
    <?php
          $page = $_GET['page'] ? $_GET['page'].'.php' : 'main.php';
          if (!strpos($page, "..") && !strpos($page, ":") && !strpos($page, "/"))
              include $page;
      ?>
    </div>
</body>
</html>
