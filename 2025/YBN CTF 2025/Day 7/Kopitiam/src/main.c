/* WARNING: Unknown calling convention */

int main(void)

{
  ulong uVar1;
  byte bVar2;
  long lVar3;
  __int32_t *p_Var4;
  char cVar5;
  int iVar6;
  time_t tVar7;
  char *pcVar8;
  long lVar9;
  byte *pbVar10;
  __int32_t **pp_Var11;
  size_t sVar12;
  ulong uVar13;
  ulong uVar14;
  void *pvVar15;
  size_t sVar16;
  EVP_CIPHER_CTX *ctx;
  EVP_CIPHER *cipher;
  int iVar17;
  byte *pbVar18;
  byte *pbVar19;
  size_t sVar20;
  size_t bufsz;
  morse_entry *pmVar21;
  size_t bufsz_00;
  char *pcVar22;
  size_t bufsz_01;
  uint uVar23;
  byte *pbVar24;
  size_t sVar25;
  long lVar26;
  ulong uVar27;
  long in_FS_OFFSET;
  bool bVar28;
  byte bVar29;
  int local_370;
  int len;
  SHA256_CTX c_1;
  uchar key [32];
  char a [128];
  char b [128];
  char c [128];
  uchar out [256];
  
  bVar29 = 0;
  lVar3 = *(long *)(in_FS_OFFSET + 0x28);
  tVar7 = time((time_t *)0x0);
  srand((uint)tVar7);
  pcVar8 = getenv("A_CAUSE_GREATER_THAN_OUR_SELF");
  if (pcVar8 != (char *)0x0) {
    lVar9 = 0;
    do {
      *(ulong *)(out + lVar9) =
           *(ulong *)("x\x02\x04ox{c}xydt\x03m\x04gxno\x7fpmn\n" + lVar9) ^ 0x3737373737373737;
      lVar9 = lVar9 + 8;
    } while (lVar9 != 0x18);
    out[0x18] = '\0';
    __printf_chk(2,"[Easter Egg] base32 token: %s\n");
  }
  puts("===== Kopitiam Morning Rush: Uncle Lim starts taking drinks order from customer =====");
  puts("Customer queue long long... faster faster!\n");
  a[0] = '\0';
  a[1] = '\0';
  a[2] = '\0';
  a[3] = '\0';
  a[4] = '\0';
  a[5] = '\0';
  a[6] = '\0';
  a[7] = '\0';
  a[8] = '\0';
  a[9] = '\0';
  a[10] = '\0';
  a[0xb] = '\0';
  a[0xc] = '\0';
  a[0xd] = '\0';
  a[0xe] = '\0';
  a[0xf] = '\0';
  a[0x10] = '\0';
  a[0x11] = '\0';
  a[0x12] = '\0';
  a[0x13] = '\0';
  a[0x14] = '\0';
  a[0x15] = '\0';
  a[0x16] = '\0';
  a[0x17] = '\0';
  a[0x18] = '\0';
  a[0x19] = '\0';
  a[0x1a] = '\0';
  a[0x1b] = '\0';
  a[0x1c] = '\0';
  a[0x1d] = '\0';
  a[0x1e] = '\0';
  a[0x1f] = '\0';
  a[0x20] = '\0';
  a[0x21] = '\0';
  a[0x22] = '\0';
  a[0x23] = '\0';
  a[0x24] = '\0';
  a[0x25] = '\0';
  a[0x26] = '\0';
  a[0x27] = '\0';
  a[0x28] = '\0';
  a[0x29] = '\0';
  a[0x2a] = '\0';
  a[0x2b] = '\0';
  a[0x2c] = '\0';
  a[0x2d] = '\0';
  a[0x2e] = '\0';
  a[0x2f] = '\0';
  a[0x30] = '\0';
  a[0x31] = '\0';
  a[0x32] = '\0';
  a[0x33] = '\0';
  a[0x34] = '\0';
  a[0x35] = '\0';
  a[0x36] = '\0';
  a[0x37] = '\0';
  a[0x38] = '\0';
  a[0x39] = '\0';
  a[0x3a] = '\0';
  a[0x3b] = '\0';
  a[0x3c] = '\0';
  a[0x3d] = '\0';
  a[0x3e] = '\0';
  a[0x3f] = '\0';
  a[0x40] = '\0';
  a[0x41] = '\0';
  a[0x42] = '\0';
  a[0x43] = '\0';
  a[0x44] = '\0';
  a[0x45] = '\0';
  a[0x46] = '\0';
  a[0x47] = '\0';
  a[0x48] = '\0';
  a[0x49] = '\0';
  a[0x4a] = '\0';
  a[0x4b] = '\0';
  a[0x4c] = '\0';
  a[0x4d] = '\0';
  a[0x4e] = '\0';
  a[0x4f] = '\0';
  a[0x50] = '\0';
  a[0x51] = '\0';
  a[0x52] = '\0';
  a[0x53] = '\0';
  a[0x54] = '\0';
  a[0x55] = '\0';
  a[0x56] = '\0';
  a[0x57] = '\0';
  a[0x58] = '\0';
  a[0x59] = '\0';
  a[0x5a] = '\0';
  a[0x5b] = '\0';
  a[0x5c] = '\0';
  a[0x5d] = '\0';
  a[0x5e] = '\0';
  a[0x5f] = '\0';
  a[0x60] = '\0';
  a[0x61] = '\0';
  a[0x62] = '\0';
  a[99] = '\0';
  a[100] = '\0';
  a[0x65] = '\0';
  a[0x66] = '\0';
  a[0x67] = '\0';
  a[0x68] = '\0';
  a[0x69] = '\0';
  a[0x6a] = '\0';
  a[0x6b] = '\0';
  a[0x6c] = '\0';
  a[0x6d] = '\0';
  a[0x6e] = '\0';
  a[0x6f] = '\0';
  a[0x70] = '\0';
  a[0x71] = '\0';
  a[0x72] = '\0';
  a[0x73] = '\0';
  a[0x74] = '\0';
  a[0x75] = '\0';
  a[0x76] = '\0';
  a[0x77] = '\0';
  a[0x78] = '\0';
  a[0x79] = '\0';
  a[0x7a] = '\0';
  a[0x7b] = '\0';
  a[0x7c] = '\0';
  a[0x7d] = '\0';
  a[0x7e] = '\0';
  a[0x7f] = '\0';
  b[0] = '\0';
  b[1] = '\0';
  b[2] = '\0';
  b[3] = '\0';
  b[4] = '\0';
  b[5] = '\0';
  b[6] = '\0';
  b[7] = '\0';
  b[8] = '\0';
  b[9] = '\0';
  b[10] = '\0';
  b[0xb] = '\0';
  b[0xc] = '\0';
  b[0xd] = '\0';
  b[0xe] = '\0';
  b[0xf] = '\0';
  b[0x10] = '\0';
  b[0x11] = '\0';
  b[0x12] = '\0';
  b[0x13] = '\0';
  b[0x14] = '\0';
  b[0x15] = '\0';
  b[0x16] = '\0';
  b[0x17] = '\0';
  b[0x18] = '\0';
  b[0x19] = '\0';
  b[0x1a] = '\0';
  b[0x1b] = '\0';
  b[0x1c] = '\0';
  b[0x1d] = '\0';
  b[0x1e] = '\0';
  b[0x1f] = '\0';
  b[0x20] = '\0';
  b[0x21] = '\0';
  b[0x22] = '\0';
  b[0x23] = '\0';
  b[0x24] = '\0';
  b[0x25] = '\0';
  b[0x26] = '\0';
  b[0x27] = '\0';
  b[0x28] = '\0';
  b[0x29] = '\0';
  b[0x2a] = '\0';
  b[0x2b] = '\0';
  b[0x2c] = '\0';
  b[0x2d] = '\0';
  b[0x2e] = '\0';
  b[0x2f] = '\0';
  b[0x30] = '\0';
  b[0x31] = '\0';
  b[0x32] = '\0';
  b[0x33] = '\0';
  b[0x34] = '\0';
  b[0x35] = '\0';
  b[0x36] = '\0';
  b[0x37] = '\0';
  b[0x38] = '\0';
  b[0x39] = '\0';
  b[0x3a] = '\0';
  b[0x3b] = '\0';
  b[0x3c] = '\0';
  b[0x3d] = '\0';
  b[0x3e] = '\0';
  b[0x3f] = '\0';
  b[0x40] = '\0';
  b[0x41] = '\0';
  b[0x42] = '\0';
  b[0x43] = '\0';
  b[0x44] = '\0';
  b[0x45] = '\0';
  b[0x46] = '\0';
  b[0x47] = '\0';
  b[0x48] = '\0';
  b[0x49] = '\0';
  b[0x4a] = '\0';
  b[0x4b] = '\0';
  b[0x4c] = '\0';
  b[0x4d] = '\0';
  b[0x4e] = '\0';
  b[0x4f] = '\0';
  b[0x50] = '\0';
  b[0x51] = '\0';
  b[0x52] = '\0';
  b[0x53] = '\0';
  b[0x54] = '\0';
  b[0x55] = '\0';
  b[0x56] = '\0';
  b[0x57] = '\0';
  b[0x58] = '\0';
  b[0x59] = '\0';
  b[0x5a] = '\0';
  b[0x5b] = '\0';
  b[0x5c] = '\0';
  b[0x5d] = '\0';
  b[0x5e] = '\0';
  b[0x5f] = '\0';
  b[0x60] = '\0';
  b[0x61] = '\0';
  b[0x62] = '\0';
  b[99] = '\0';
  b[100] = '\0';
  b[0x65] = '\0';
  b[0x66] = '\0';
  b[0x67] = '\0';
  b[0x68] = '\0';
  b[0x69] = '\0';
  b[0x6a] = '\0';
  b[0x6b] = '\0';
  b[0x6c] = '\0';
  b[0x6d] = '\0';
  b[0x6e] = '\0';
  b[0x6f] = '\0';
  b[0x70] = '\0';
  b[0x71] = '\0';
  b[0x72] = '\0';
  b[0x73] = '\0';
  b[0x74] = '\0';
  b[0x75] = '\0';
  b[0x76] = '\0';
  b[0x77] = '\0';
  b[0x78] = '\0';
  b[0x79] = '\0';
  b[0x7a] = '\0';
  b[0x7b] = '\0';
  b[0x7c] = '\0';
  b[0x7d] = '\0';
  b[0x7e] = '\0';
  b[0x7f] = '\0';
  c[0] = '\0';
  c[1] = '\0';
  c[2] = '\0';
  c[3] = '\0';
  c[4] = '\0';
  c[5] = '\0';
  c[6] = '\0';
  c[7] = '\0';
  c[8] = '\0';
  c[9] = '\0';
  c[10] = '\0';
  c[0xb] = '\0';
  c[0xc] = '\0';
  c[0xd] = '\0';
  c[0xe] = '\0';
  c[0xf] = '\0';
  c[0x10] = '\0';
  c[0x11] = '\0';
  c[0x12] = '\0';
  c[0x13] = '\0';
  c[0x14] = '\0';
  c[0x15] = '\0';
  c[0x16] = '\0';
  c[0x17] = '\0';
  c[0x18] = '\0';
  c[0x19] = '\0';
  c[0x1a] = '\0';
  c[0x1b] = '\0';
  c[0x1c] = '\0';
  c[0x1d] = '\0';
  c[0x1e] = '\0';
  c[0x1f] = '\0';
  c[0x20] = '\0';
  c[0x21] = '\0';
  c[0x22] = '\0';
  c[0x23] = '\0';
  c[0x24] = '\0';
  c[0x25] = '\0';
  c[0x26] = '\0';
  c[0x27] = '\0';
  c[0x28] = '\0';
  c[0x29] = '\0';
  c[0x2a] = '\0';
  c[0x2b] = '\0';
  c[0x2c] = '\0';
  c[0x2d] = '\0';
  c[0x2e] = '\0';
  c[0x2f] = '\0';
  c[0x30] = '\0';
  c[0x31] = '\0';
  c[0x32] = '\0';
  c[0x33] = '\0';
  c[0x34] = '\0';
  c[0x35] = '\0';
  c[0x36] = '\0';
  c[0x37] = '\0';
  c[0x38] = '\0';
  c[0x39] = '\0';
  c[0x3a] = '\0';
  c[0x3b] = '\0';
  c[0x3c] = '\0';
  c[0x3d] = '\0';
  c[0x3e] = '\0';
  c[0x3f] = '\0';
  c[0x40] = '\0';
  c[0x41] = '\0';
  c[0x42] = '\0';
  c[0x43] = '\0';
  c[0x44] = '\0';
  c[0x45] = '\0';
  c[0x46] = '\0';
  c[0x47] = '\0';
  c[0x48] = '\0';
  c[0x49] = '\0';
  c[0x4a] = '\0';
  c[0x4b] = '\0';
  c[0x4c] = '\0';
  c[0x4d] = '\0';
  c[0x4e] = '\0';
  c[0x4f] = '\0';
  c[0x50] = '\0';
  c[0x51] = '\0';
  c[0x52] = '\0';
  c[0x53] = '\0';
  c[0x54] = '\0';
  c[0x55] = '\0';
  c[0x56] = '\0';
  c[0x57] = '\0';
  c[0x58] = '\0';
  c[0x59] = '\0';
  c[0x5a] = '\0';
  c[0x5b] = '\0';
  c[0x5c] = '\0';
  c[0x5d] = '\0';
  c[0x5e] = '\0';
  c[0x5f] = '\0';
  c[0x60] = '\0';
  c[0x61] = '\0';
  c[0x62] = '\0';
  c[99] = '\0';
  c[100] = '\0';
  c[0x65] = '\0';
  c[0x66] = '\0';
  c[0x67] = '\0';
  c[0x68] = '\0';
  c[0x69] = '\0';
  c[0x6a] = '\0';
  c[0x6b] = '\0';
  c[0x6c] = '\0';
  c[0x6d] = '\0';
  c[0x6e] = '\0';
  c[0x6f] = '\0';
  c[0x70] = '\0';
  c[0x71] = '\0';
  c[0x72] = '\0';
  c[0x73] = '\0';
  c[0x74] = '\0';
  c[0x75] = '\0';
  c[0x76] = '\0';
  c[0x77] = '\0';
  c[0x78] = '\0';
  c[0x79] = '\0';
  c[0x7a] = '\0';
  c[0x7b] = '\0';
  c[0x7c] = '\0';
  c[0x7d] = '\0';
  c[0x7e] = '\0';
  c[0x7f] = '\0';
  puts("Uncle: \"Lai, drink what?\"");
  puts("Lee: \"I want order a *****\"");
  read_line("[Level 1] Enter order: ",a,bufsz);
  pbVar10 = (byte *)malloc(0x100);
  if (pbVar10 == (byte *)0x0) {
LAB_0016663a:
    grumble();
  }
  else {
    bVar2 = a[0];
    *pbVar10 = 0;
    if (a[0] != '\0') {
      pp_Var11 = __ctype_tolower_loc();
      pbVar24 = (byte *)a;
      p_Var4 = *pp_Var11;
      sVar25 = 0x100;
      sVar16 = 0;
      do {
        pbVar24 = pbVar24 + 1;
        pmVar21 = MORSE;
        lVar9 = 0;
        do {
          if ((char)p_Var4[bVar2] == pmVar21->ch) {
            if (MORSE[lVar9].morse != (char *)0x0) {
              sVar12 = strlen(MORSE[lVar9].morse);
              goto LAB_0016626a;
            }
            break;
          }
          lVar9 = lVar9 + 1;
          pmVar21 = pmVar21 + 1;
        } while (lVar9 != 0x24);
        sVar12 = 0;
LAB_0016626a:
        uVar13 = ((sVar16 + 2) - (ulong)(sVar16 == 0)) + sVar12;
        if (sVar25 < uVar13) {
          sVar25 = uVar13 * 2;
          pbVar10 = (byte *)realloc(pbVar10,sVar25);
          if (pbVar10 == (byte *)0x0) goto LAB_0016663a;
        }
        pbVar18 = pbVar10;
        if (sVar16 != 0) {
          pbVar10[sVar16] = 0x20;
          sVar12 = sVar16 + 1 + sVar12;
          pbVar18 = pbVar10 + sVar16 + 1;
        }
        __memcpy_chk(pbVar18);
        bVar2 = *pbVar24;
        pbVar10[sVar12] = 0;
        sVar16 = sVar12;
      } while (bVar2 != 0);
      if (pbVar10 == (byte *)0x0) goto LAB_0016663a;
    }
    sVar25 = strlen((char *)pbVar10);
    if (sVar25 == 0) {
      pcVar8 = (char *)malloc(1);
      if (pcVar8 == (char *)0x0) goto LAB_0016698a;
      *pcVar8 = '\0';
      free(pbVar10);
    }
    else {
      pcVar8 = (char *)malloc(((sVar25 + 4) / 5) * 8 + 1);
      if (pcVar8 == (char *)0x0) {
LAB_0016698a:
        free(pbVar10);
        goto LAB_0016663a;
      }
      uVar13 = 0;
      iVar17 = 0;
      uVar23 = 0;
      pbVar24 = pbVar10;
      do {
        iVar17 = iVar17 + 8;
        uVar23 = uVar23 << 8 | (uint)*pbVar24;
        do {
          uVar14 = uVar13;
          iVar17 = iVar17 + -5;
          uVar13 = uVar14 + 1;
          pcVar8[uVar14] =
               "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"[uVar23 >> ((byte)iVar17 & 0x1f) & 0x1f];
        } while (4 < iVar17);
        pbVar24 = pbVar24 + 1;
      } while (pbVar10 + sVar25 != pbVar24);
      if (iVar17 != 0) {
        pcVar8[uVar13] =
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"[uVar23 << (5 - (byte)iVar17 & 0x1f) & 0x1f];
        uVar13 = uVar14 + 2;
      }
      for (; (uVar13 & 7) != 0; uVar13 = uVar13 + 1) {
        pcVar8[uVar13] = '=';
      }
      pcVar8[uVar13] = '\0';
      free(pbVar10);
    }
    iVar17 = strcmp(pcVar8,"FUXC2IBNFUWSALRNFUXCALROEAWS2LJNFU======");
    free(pcVar8);
    if (iVar17 != 0) goto LAB_0016663a;
    puts("\nUncle: \"Ok. $58. Enjoy ar...!\"\n");
    puts("Uncle: \"Lai, drink what?\"");
    puts("Ali: \"I want order a *******\"");
    read_line("[Level 2] Enter order: ",b,bufsz_00);
    sVar25 = strlen(b);
    pvVar15 = malloc(sVar25);
    if (pvVar15 == (void *)0x0) goto LAB_0016663a;
    if (sVar25 == 0) {
      pcVar8 = (char *)malloc(1);
      if (pcVar8 == (char *)0x0) goto LAB_0016699f;
      *pcVar8 = '\0';
    }
    else {
      uVar13 = 0;
      do {
        uVar14 = uVar13;
        *(char *)((long)pvVar15 + uVar14) = (&KEY.2)[(uint)uVar14 & 1] ^ b[uVar14];
        uVar13 = uVar14 + 1;
      } while (sVar25 != uVar13);
      uVar27 = 0;
      do {
        if (*(char *)((long)pvVar15 + uVar27) != '\0') break;
        uVar1 = uVar27 + 1;
        bVar28 = uVar14 != uVar27;
        uVar27 = uVar1;
      } while (bVar28);
      pbVar10 = (byte *)calloc(((uVar13 - uVar27) * 0x8a) / 100 + 1,1);
      if (pbVar10 == (byte *)0x0) {
LAB_0016699f:
        free(pvVar15);
        goto LAB_0016663a;
      }
      if (uVar27 < uVar13) {
        pbVar24 = (byte *)((long)pvVar15 + uVar27);
        lVar26 = 0;
        do {
          uVar23 = (uint)*pbVar24;
          if (lVar26 != 0) {
            pbVar18 = pbVar10;
            do {
              pbVar19 = pbVar18 + 1;
              iVar17 = (uint)*pbVar18 * 0x100 + uVar23;
              uVar23 = iVar17 / 0x3a;
              *pbVar18 = (char)iVar17 + (char)uVar23 * -0x3a;
              pbVar18 = pbVar19;
            } while (pbVar19 != pbVar10 + lVar26);
          }
          lVar9 = lVar26;
          if (uVar23 != 0) {
            lVar9 = lVar26 + 1;
            pbVar10[lVar26] = (char)uVar23 + (char)(uVar23 / 0x3a) * -0x3a;
            if (uVar23 / 0x3a != 0) {
              lVar9 = lVar26 + 2;
              pbVar10[lVar26 + 1] = (byte)((ulong)uVar23 / 0x3a);
            }
          }
          pbVar24 = pbVar24 + 1;
          lVar26 = lVar9;
        } while ((byte *)((long)pvVar15 + uVar13) != pbVar24);
        pcVar8 = (char *)malloc(uVar27 + 1 + lVar9);
        if (pcVar8 == (char *)0x0) {
LAB_00166997:
          free(pbVar10);
          goto LAB_0016699f;
        }
        if (uVar27 != 0) goto LAB_0016655a;
      }
      else {
        pcVar8 = (char *)malloc(uVar27 + 1);
        if (pcVar8 == (char *)0x0) goto LAB_00166997;
        lVar9 = 0;
LAB_0016655a:
        pcVar22 = pcVar8;
        for (uVar13 = uVar27 & 0xffffffff; uVar13 != 0; uVar13 = uVar13 - 1) {
          *pcVar22 = '1';
          pcVar22 = pcVar22 + (ulong)bVar29 * -2 + 1;
        }
      }
      if (lVar9 != 0) {
        pbVar24 = pbVar10 + lVar9 + -1;
        pcVar22 = pcVar8 + uVar27;
        do {
          *pcVar22 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"[*pbVar24];
          bVar28 = pbVar24 != pbVar10;
          pbVar24 = pbVar24 + -1;
          pcVar22 = pcVar22 + 1;
        } while (bVar28);
        uVar27 = uVar27 + lVar9;
      }
      pcVar8[uVar27] = '\0';
      free(pbVar10);
    }
    free(pvVar15);
    iVar17 = strcmp(pcVar8,TARGET.1);
    free(pcVar8);
    if (iVar17 != 0) goto LAB_0016663a;
    puts("\nUncle: \"Ok. $13 + $3 Enjoy ar...!\"\n");
    puts("Uncle: \"Lai, drink what?\"");
    puts("Sotong: \"I want order a **********\"");
    read_line("[Level 3] Enter order: ",c,bufsz_01);
    sVar25 = strlen(c);
    if ((sVar25 != 10) || (pvVar15 = malloc(10), pvVar15 == (void *)0x0)) goto LAB_0016663a;
    lVar9 = 0;
    do {
      cVar5 = c[lVar9];
      if ((byte)(cVar5 + 0x9fU) < 0x1a) {
        cVar5 = (char)((cVar5 + -0x54) % 0x1a) + 'a';
      }
      else if ((byte)(cVar5 + 0xbfU) < 0x1a) {
        cVar5 = (char)((cVar5 + -0x34) % 0x1a) + 'A';
      }
      *(char *)((long)pvVar15 + lVar9) = cVar5 + '\x03';
      lVar9 = lVar9 + 1;
    } while (lVar9 != 10);
    iVar17 = memcmp(pvVar15,TARGET.0,10);
    free(pvVar15);
    if (iVar17 != 0) goto LAB_0016663a;
    sVar16 = strlen(a);
    sVar12 = strlen(b);
    uVar13 = sVar16 + sVar12;
    sVar25 = uVar13 + 10;
    pvVar15 = malloc(sVar25);
    if (pvVar15 == (void *)0x0) {
      puts("Out of memory.");
    }
    else {
      __memcpy_chk(pvVar15,a,sVar16,sVar25);
      sVar20 = sVar16;
      if (sVar16 <= sVar25) {
        sVar20 = sVar25;
      }
      __memcpy_chk((long)pvVar15 + sVar16,b,sVar12,sVar20 - sVar16);
      sVar16 = sVar25;
      if (sVar25 <= uVar13) {
        sVar16 = uVar13;
      }
      __memcpy_chk((long)pvVar15 + uVar13,c,10,sVar16 - uVar13);
      SHA256_Init((SHA256_CTX *)&c_1);
      SHA256_Update((SHA256_CTX *)&c_1,pvVar15,sVar25);
      SHA256_Final(key,(SHA256_CTX *)&c_1);
      free(pvVar15);
      len = 0;
      ctx = EVP_CIPHER_CTX_new();
      if (ctx != (EVP_CIPHER_CTX *)0x0) {
        cipher = EVP_aes_256_cbc();
        iVar17 = EVP_DecryptInit_ex(ctx,cipher,(ENGINE *)0x0,key,IV);
        if (iVar17 != 0) {
          iVar6 = EVP_DecryptUpdate(ctx,out,&len,CT,0x40);
          iVar17 = len;
          if ((iVar6 != 0) && (iVar6 = EVP_DecryptFinal_ex(ctx,out + len,&len), iVar6 != 0)) {
            iVar17 = iVar17 + len;
            EVP_CIPHER_CTX_free(ctx);
            out[iVar17] = '\0';
            puts("===== Uncle ended the day happily. Who knew coffee can be so expensive. =====");
            puts((char *)out);
            local_370 = 0;
            goto LAB_00166649;
          }
        }
        EVP_CIPHER_CTX_free(ctx);
      }
      puts("Eh... You didn\'t order these leh...");
    }
  }
  local_370 = 1;
LAB_00166649:
  if (lVar3 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return local_370;
}