
undefined8 FUN_004024e4(void)

{
  char cVar1;
  long lVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  byte bVar5;
  undefined8 local_348 [39];
  undefined8 uStack_210;
  undefined8 local_208 [12];
  undefined1 local_1a4 [100];
  undefined1 local_140 [100];
  undefined1 local_dc [4];
  undefined1 local_d8 [4];
  undefined1 local_d4 [4];
  undefined1 local_d0 [8];
  undefined1 local_c8 [112];
  undefined1 local_58 [48];
  undefined1 local_28 [32];
  
  bVar5 = 0;
  uStack_210 = 0x4024f4;
  FUN_0040238a();
  uStack_210 = 0x4024fe;
  FUN_00415ea0("Welcome into the latest version of");
  uStack_210 = 0x402508;
  FUN_00415ea0("      Albo delle Eccellenze       ");
  uStack_210 = 0x402512;
  FUN_00415ea0("   (PascalCTF Beginners 2026)     ");
  uStack_210 = 0x40251c;
  FUN_00415ea0(&DAT_0050bd7b);
  uStack_210 = 0x402535;
  thunk_FUN_00423c60(local_208,0,0x13c);
  uStack_210 = 0x402544;
  FUN_00405c80("Enter your name: ");
  uStack_210 = 0x40255f;
  FUN_004159c0(local_208,100,PTR_DAT_005396d8);
  uStack_210 = 0x40256e;
  FUN_00405c80("Enter your surname: ");
  uStack_210 = 0x402590;
  FUN_004159c0(local_1a4,100,PTR_DAT_005396d8);
  uStack_210 = 0x40259f;
  FUN_00405c80("Enter your date of birth (DD/MM/YYYY): ");
  uStack_210 = 0x4025ba;
  FUN_004159c0(local_c8,100,PTR_DAT_005396d8);
  uStack_210 = 0x402600;
  FUN_00405b50(local_c8,"%2d/%2d/%4d",local_dc,local_d8,local_d4);
  uStack_210 = 0x40260f;
  FUN_00405c80("Enter your sex (M/F): ");
  uStack_210 = 0x40262a;
  FUN_004159c0(local_c8,100,PTR_DAT_005396d8);
  uStack_210 = 0x402651;
  FUN_00405b50(local_c8,&DAT_0050bdf3,local_d0);
  uStack_210 = 0x402660;
  FUN_00405c80("Enter your place of birth: ");
  uStack_210 = 0x402685;
  FUN_004159c0(local_140,100,PTR_DAT_005396d8);
  uStack_210 = 0x40269f;
  lVar2 = thunk_FUN_00423f50(local_140,&DAT_0050be12);
  local_140[lVar2] = 0;
  puVar3 = local_208;
  puVar4 = local_348;
  for (lVar2 = 0x27; lVar2 != 0; lVar2 = lVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + (ulong)bVar5 * -2 + 1;
    puVar4 = puVar4 + (ulong)bVar5 * -2 + 1;
  }
  *(undefined4 *)puVar4 = *(undefined4 *)puVar3;
  FUN_00401f96(local_28);
  uStack_210 = 0x4026f2;
  cVar1 = FUN_004023eb(local_28);
  if (cVar1 == '\x01') {
    uStack_210 = 0x40273d;
    FUN_00405c80("Code did not match. Your code is: %s\n",local_28);
  }
  else {
    uStack_210 = 0x402705;
    FUN_00402311(local_58);
    uStack_210 = 0x40270f;
    FUN_00415ea0("Code matched!");
    uStack_210 = 0x402725;
    FUN_00405c80("Here is the flag: %s\n",local_58);
  }
  return 0;
}


void FUN_00401f96(long param_1)

{
  undefined1 uVar1;
  int iVar2;
  undefined8 in_stack_00000130;
  undefined4 uStack0000000000000138;
  int iStack000000000000013c;
  char in_stack_00000140;
  undefined1 local_1f8 [112];
  undefined1 local_188 [112];
  undefined1 local_118 [112];
  undefined1 local_a8 [112];
  int local_38;
  int local_34;
  uint local_30;
  int local_2c;
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  
  FUN_00401d43(&stack0x00000008,local_a8,local_118);
  FUN_00401d43(&stack0x0000006c,local_188,local_1f8);
  local_34 = thunk_FUN_00423f70(local_188);
  local_38 = thunk_FUN_00423f70(local_1f8);
  local_1c = 0;
  for (local_20 = 0; iVar2 = local_1c, local_20 < 3; local_20 = local_20 + 1) {
    if (local_20 < local_34) {
      local_1c = local_1c + 1;
      *(undefined1 *)(iVar2 + param_1) = local_188[local_20];
    }
  }
  for (local_24 = 0; (iVar2 = local_1c, local_1c < 3 && (local_24 < local_38));
      local_24 = local_24 + 1) {
    local_1c = local_1c + 1;
    *(undefined1 *)(iVar2 + param_1) = local_1f8[local_24];
  }
  while (local_1c < 3) {
    *(undefined1 *)(param_1 + local_1c) = 0x58;
    local_1c = local_1c + 1;
  }
  local_34 = thunk_FUN_00423f70(local_a8);
  local_38 = thunk_FUN_00423f70(local_118);
  if (local_34 < 4) {
    for (local_28 = 0; iVar2 = local_1c, local_28 < 3; local_28 = local_28 + 1) {
      if (local_28 < local_34) {
        local_1c = local_1c + 1;
        *(undefined1 *)(iVar2 + param_1) = local_a8[local_28];
      }
    }
    for (local_2c = 0; (iVar2 = local_1c, local_1c < 6 && (local_2c < local_38));
        local_2c = local_2c + 1) {
      local_1c = local_1c + 1;
      *(undefined1 *)(iVar2 + param_1) = local_118[local_2c];
    }
    while (local_1c < 6) {
      *(undefined1 *)(param_1 + local_1c) = 0x58;
      local_1c = local_1c + 1;
    }
  }
  else {
    *(undefined1 *)(local_1c + param_1) = local_a8[0];
    iVar2 = local_1c + 2;
    *(undefined1 *)((local_1c + 1) + param_1) = local_a8[2];
    local_1c = local_1c + 3;
    *(undefined1 *)(iVar2 + param_1) = local_a8[3];
  }
  FUN_00405d50(param_1 + 6,&DAT_0050bcc0,iStack000000000000013c % 100);
  uVar1 = FUN_00401e7e(uStack0000000000000138);
  *(undefined1 *)(param_1 + 8) = uVar1;
  if (in_stack_00000140 == 'F') {
    iVar2 = 0x28;
  }
  else {
    iVar2 = 0;
  }
  FUN_00405d50(param_1 + 9,&DAT_0050bcc0,iVar2 + in_stack_00000130._4_4_);
  local_30 = 0;
  do {
    if (0x1edf < local_30) {
LAB_004022e0:
      uVar1 = FUN_00401ca5(param_1);
      *(undefined1 *)(param_1 + 0xf) = uVar1;
      *(undefined1 *)(param_1 + 0x10) = 0;
      return;
    }
    iVar2 = thunk_FUN_00423e60("Abano Terme" + (long)(int)local_30 * 0x37,&stack0x000000d0);
    if (iVar2 == 0) {
      thunk_FUN_00423ef0(param_1 + 0xb,&UNK_004a12b2 + (long)(int)local_30 * 0x37);
      goto LAB_004022e0;
    }
    local_30 = local_30 + 1;
  } while( true );
}


undefined8 FUN_004023eb(long param_1)

{
  undefined1 uVar1;
  int iVar2;
  long lVar3;
  undefined8 uVar4;
  int local_14;
  int local_10;
  int local_c;
  
  lVar3 = thunk_FUN_00423f70(param_1);
  if (lVar3 == 0x10) {
    for (local_c = 0; local_c < 0x40; local_c = local_c + 1) {
      for (local_10 = 0; local_10 < 0x10; local_10 = local_10 + 1) {
        *(byte *)(param_1 + local_10) = *(byte *)(param_1 + local_10) ^ 0x5e;
      }
      for (local_14 = 0; local_14 < 0x10; local_14 = local_14 + 1) {
        uVar1 = *(undefined1 *)(param_1 + (long)local_14 + 1);
        *(undefined1 *)(param_1 + (long)local_14 + 1) = *(undefined1 *)(param_1 + local_14);
        *(undefined1 *)(local_14 + param_1) = uVar1;
      }
    }
    iVar2 = thunk_FUN_00423e60(param_1,"A11D612LPSCBLS37");
    if (iVar2 == 0) {
      uVar4 = 1;
    }
    else {
      uVar4 = 0;
    }
  }
  else {
    uVar4 = 0;
  }
  return uVar4;
}


void FUN_00402311(long param_1)

{
  long lVar1;
  long lVar2;
  
  lVar1 = FUN_00415cf0(&DAT_0050bcc7,&DAT_0050bcc5);
  if (lVar1 == 0) {
    FUN_0040044b("Could not open flag file");
    FUN_004059a0(1);
  }
  FUN_004159c0(param_1,0x32,lVar1);
  lVar2 = thunk_FUN_00423f50(param_1,&DAT_0050bce5);
  *(undefined1 *)(lVar2 + param_1) = 0;
  FUN_00415490(lVar1);
  return;
}

