<?php
error_reporting(0);

$flag = file_get_contents('/flag');
putenv("FLAG=".$flag);

const PLACEHOLDER_REGEX_PART = '[[:alpha:]][^>} <`{"\']*';
const PLACEHOLDER_REGEX = '~\{(' . PLACEHOLDER_REGEX_PART . ')\}~';

$error=null;
$result=null;

// from https://git.moodle.org/gw?p=moodle.git;a=blob;f=question/type/calculated/questiontype.php;h=7bd48f61120199b8b7987acd6b6b319201ce891b;hb=db07c09afc52f67a7fa3dc41ba1707ed7f99b58a
function check_formula($formula) {
    foreach (['//', '/*', '#', '<?', '?>'] as $commentstart) {
        if (strpos($formula, $commentstart) !== false) {
            return 'no hack';
        }
    }
    
    $formula = preg_replace(PLACEHOLDER_REGEX, '1.0', $formula);
    $formula = strtolower(str_replace(' ', '', $formula));
    
    $safeoperatorchar = '-+/*%>:^\~<?=&|!';
    $operatorornumber = "[{$safeoperatorchar}.0-9eE]";
    
    while (preg_match("~(^|[{$safeoperatorchar},(])([a-z0-9_]*)" .
             "\\(({$operatorornumber}+(,{$operatorornumber}+((,{$operatorornumber}+)+)?)?)?\\)~",
             $formula, $regs)) {
        switch ($regs[2]) {
            case '':
                if ((isset($regs[4]) && $regs[4]) || strlen($regs[3]) == 0) {
                    return $regs[0].' Illegal formula syntax';
                }
                break;
    
            case 'pi':
                if (array_key_exists(3, $regs)) {
                    return $regs[2].' does not require any args';
                }
                break;

            case 'abs': case 'ceil':
            case 'decbin': case 'decoct': case 'deg2rad':
            case 'exp': case 'floor':
            case 'octdec': case 'rad2deg':
    
            case 'round':
                if (!empty($regs[5]) || empty($regs[3])) {
                    return $regs[2].' requires one or two args';
                }
                break;
    
            default:
                return $regs[2].' is not supported';
        }

    
        if ($regs[1]) {
            $formula = str_replace($regs[0], $regs[1] . '1.0', $formula);
       
    
        } else {
            $formula = preg_replace('~^' . preg_quote($regs[2], '~') . '\([^)]*\)~', '1.0', $formula);
        }
    }

                 
    if (preg_match("~[^{$safeoperatorchar}.0-9eE]+~", $formula, $regs)) {
        return $regs[0].' Illegal formula syntax';
    } else {
        return false;
    }
}

function calculate($formula){
    global $error;
    $error = check_formula($formula);
    if($error){

    } else {
        // Variable variables are not allowed.
        $formula = str_replace('{', '(', $formula);
        $formula = str_replace('}', ')', $formula);
        
        return eval('return ' . $formula . ';');

    }

}

if (isset($_GET['f']) && $_GET['f'] !== ''){
    $formula = $_GET['f'];
    $result = calculate($formula);
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Calculator Page</title>
    <style>
        .calculator {
            width: 300px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            text-align: center;
            margin: 0 auto;
            margin-top: 50px;
        }
        .display {
            width: 100%;
            height: 40px;
            text-align: right;
            margin-bottom: 10px;
            font-size: 18px;
            padding: 5px;
            box-sizing: border-box;
        }
        .button {
            width: 50px;
            height: 45px;
            margin: 5px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <form method="GET" action="cal.php">
            <input type="text" id="display" name="f" class="display" value="<?php echo isset($_GET['f']) ? htmlspecialchars($_GET['f']) : "0"; ?>" readonly>
            <br>
            <button type="button" class="button" onclick="appendNumber('1')">1</button>
            <button type="button" class="button" onclick="appendNumber('2')">2</button>
            <button type="button" class="button" onclick="appendNumber('3')">3</button>
            <button type="button" class="button" onclick="appendOperator('+')">+</button>
            <br>
            <button type="button" class="button" onclick="appendNumber('4')">4</button>
            <button type="button" class="button" onclick="appendNumber('5')">5</button>
            <button type="button" class="button" onclick="appendNumber('6')">6</button>
            <button type="button" class="button" onclick="appendOperator('-')">-</button>
            <br>
            <button type="button" class="button" onclick="appendNumber('7')">7</button>
            <button type="button" class="button" onclick="appendNumber('8')">8</button>
            <button type="button" class="button" onclick="appendNumber('9')">9</button>
            <button type="button" class="button" onclick="appendOperator('*')">*</button>
            <br>
            <button type="button" class="button" onclick="appendNumber('0')">0</button>
            <button type="button" class="button" onclick="appendOperator('/')">/</button>

            <button type="button" class="button" onclick="clearDisplay()">AC</button>
            <button type="submit" class="button">=</button>
            <br>
            <button type="button" class="button" onclick="appendEtc('(')">(</button>
            <button type="button" class="button" onclick="appendEtc(')')">)</butto>
            <button type="button" class="button" onclick="appendEtc('.')">.</button>
            <button type="button" class="button" onclick="appendEtc(',')">,</button>
            <br>
            <button type="button" class="button" onclick="appendFunction('decbin')">DTB</button>
            <button type="button" class="button" onclick="appendFunction('decoct')">DTO</button>
            <button type="button" class="button" onclick="appendFunction('deg2rad')">DTR</button>
            <button type="button" class="button" onclick="appendFunction('exp')">EXP</button>
            <br>
            <button type="button" class="button" onclick="appendFunction('floor')">FLO</button>
            <button type="button" class="button" onclick="appendFunction('octdec')">OTD</button>
            <button type="button" class="button" onclick="appendFunction('rad2deg')">RTD</button>
            <button type="button" class="button" onclick="appendFunction('round')">ROU</button>
            <br>
            <button type="button" class="button" onclick="appendFunction('pi')">PI</button>
            <button type="button" class="button" onclick="appendFunction('abs')">ABS</button>
            <button type="button" class="button" onclick="backSpace()">C</button>
            <button type="button" class="button" onclick="">N/A</button>
        </form>
        <div>
            <?php if (gettype($error) === 'string'): ?>
                <p style="color: red;"><?php echo $error; ?></p>
            <?php else: ?>
                <p>Result: <?php echo $result; ?></p>
            <?php endif; ?>
        </div>
    </div>

</body>
<script>
    
        function appendNumber(number) {
            if (document.getElementById('display').value === '0'){
                document.getElementById('display').value = number;
            } else {
                document.getElementById('display').value += number;
            }
        }

        function appendOperator(operator) {
            document.getElementById('display').value += operator;
        }

        function appendEtc(etc) {
            document.getElementById('display').value += etc;
        }

        function appendFunction(functionName){
            if (document.getElementById('display').value === '0'){
                document.getElementById('display').value = functionName + '(';  
            } else {
                document.getElementById('display').value += functionName + '(';
            }
        }

        function backSpace(){
            if (document.getElementById('display').value !== ''){
                document.getElementById('display').value = document.getElementById('display').value.slice(0,-1);
            }
        }

        function clearDisplay() {
            document.getElementById('display').value = '0';
        }


</script>
</html>
