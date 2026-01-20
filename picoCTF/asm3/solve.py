def asm3(arg1, arg2, arg3):    
    ah = (arg1 >> 8) & 0xff       
    al_sub = (arg2 >> 24) & 0xff  
    ah_add = (arg2 >> 8) & 0xff   
    word = (arg3 >> 16) & 0xffff  

    ax = ah                          
    ax = ax << 8                     
                                      
    eax = ax << 16                   
    al = eax & 0xff
    ah = (eax >> 8) & 0xff
    
    al = (al - al_sub) & 0xff
    ah = (ah + ah_add) & 0xff
    ax = (ah << 8) | al
    
    ax ^= word
    return ax

print("Flag:", hex(asm3(0xb75a8f13,0xe1860bd7,0xc8e62f81)))