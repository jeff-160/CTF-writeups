syntax = {
    "chat is this real": "if",            
    "yo chat": "elif",                    
    "only in ohio": "else",               
    "mewing": "for",                      
    "let him cook": "while",              
    
    "hawk": "try",                        
    "tuah": "except",                     
    "spit on that thang": "finally",      

    "bop": "def",                         
    "skibidi": "class",                   
    "GOAT": "global",                     
    "motion": "nonlocal",                 
    "pluh": "pass",                       
    "pause": "yield",                     
    "pause no diddy": "yield from",       
    "unc": "self",                        

    "glaze": "import",                    
    "lock in": "from",                    

    "yap": "print",                       
    "mog": "open",                        
    "demure": "close",                    
    
    "Aura": "True",                       
    "Cooked": "False",                    
    "NPC": "None",                        
    
    "rizz": "+",                          
    "fanum tax": "-",                     
    "sigma": ">",                         
    "beta": "<",                          
    "sigma twin": ">=",                   
    "beta twin": "<=",                    
    "twin": "==",                         
    
    "just put the fries in the bag bro": "break",   
    "edge": "continue",                              

    "sus": "assert",                     
    "crashout": "raise",                 
    
    "pookie": "with",                    
    "ahh": "as",                         

    "delulu": "del",                     
    "huzz": "range",  

    'its giving': 'return'                   
}

with open("AuraTester2000.gyat", "r", encoding='utf-8') as f:
    code = f.read().strip()

for a, b in syntax.items():
    code = code.replace(a, b)

with open("deobf.py", "w", encoding='utf-8') as f:
    f.write(code)