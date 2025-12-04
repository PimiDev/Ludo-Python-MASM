.686
.model flat, stdcall
.stack 4096

PUBLIC tirarDado
PUBLIC getTurno
PUBLIC avanzarTurno
PUBLIC puedeSacarFicha
PUBLIC moverFicha

.data

semilla        DWORD 0
inicializada   BYTE 0

turnoActual    DWORD 0     ; 0-3


.code



tirarDado PROC STDCALL
    ; Inicializar semilla 1 vez
    cmp inicializada, 0
    jne continuar

    RDTSC
    mov semilla, eax
    mov inicializada, 1

continuar:
    mov eax, semilla
    mov ecx, 1103515245
    mul ecx
    add eax, 12345
    mov semilla, eax

    ; Sacar número 1–6
    mov ebx, 6
    xor edx, edx
    div ebx
    inc edx
    mov eax, edx
    ret
tirarDado ENDP


getTurno PROC STDCALL
    mov eax, turnoActual
    ret
getTurno ENDP

avanzarTurno PROC STDCALL
    inc turnoActual
    cmp turnoActual, 4
    jl fin
    mov turnoActual, 0
fin:
    ret
avanzarTurno ENDP


; int puedeSacarFicha(int dado)
puedeSacarFicha PROC STDCALL dado:DWORD
    cmp dado, 6
    sete al
    movzx eax, al
    ret 4
puedeSacarFicha ENDP



; ============================================================
; DWORD moverFicha(DWORD posActual, DWORD pasos, DWORD jugador)
; Reglas:
;  - Casa = -1
;  - Sale con 5 o 6
;  - Tablero principal = 0 a 51 (52 casillas)
;  - Zonas seguras:
;        J0 - 52-57 (meta 57)
;        J1 - 58-63 (meta 63)
;        J2 - 64-69 (meta 69)
;        J3 - 70-75 (meta 75)
;  - Meta final = 100
; ============================================================

moverFicha PROC STDCALL posActual:DWORD, pasos:DWORD, jugador:DWORD
    mov eax, posActual     ; eax = posActual
    mov ebx, pasos         ; ebx = pasos
    mov ecx, jugador       ; ecx = jugador

    ; =============================
    ; 1) SI ESTa EN CASA (-1)
    ; =============================
    cmp eax, -1
    jne verificar_seguro

    cmp ebx, 5
    je salir_de_casa
    cmp ebx, 6
    je salir_de_casa

    ; No sale
    mov eax, -1
    jmp done

salir_de_casa:
    cmp ecx, 0
    je j0_s
    cmp ecx, 1
    je j1_s
    cmp ecx, 2
    je j2_s
    ; jugador 3
    mov eax, 39
    jmp done

j0_s:
mov eax, 0  
jmp done

j1_s:
mov eax, 13 
jmp done

j2_s: 
mov eax, 26 
jmp done

    ; =============================
    ; 2) VERIFICAR ZONA SEGURA
    ; =============================
verificar_seguro:
    cmp eax, 100
    je ya_meta

    cmp eax, 52
    jae mover_seguro

    ; =============================
    ; 3) MOVIMIENTO EN TABLERO
    ; =============================
    mov edx, eax        ; guardar posicion original
    add eax, ebx        ; mover

    ; ----- aplicar wrap 0–51 -----
    cmp eax, 52
    jl  comprobar_portal
    sub eax, 52

comprobar_portal:

    ; ========== PORTALES ==========
    ; JUGADOR 0 portal = 51 - zona 52
    cmp ecx, 0
    jne portal_j1

    cmp edx, 51
    jae normal_j0
    cmp eax, 51
    jb  normal_j0

    ; PASÓ POR PORTAL
    mov eax, 52
    jmp done

normal_j0:
    jmp wrap_done

; --------------------------------------------------

portal_j1:
    ; J1 portal = 12 - zona 58
    cmp ecx, 1
    jne portal_j2

    cmp edx, 12
    jae normal_j1
    cmp eax, 12
    jb  normal_j1

    mov eax, 58
    jmp done

normal_j1:
    jmp wrap_done

; --------------------------------------------------

portal_j2:
    ; J2 portal = 25 - zona 64
    cmp ecx, 2
    jne portal_j3

    cmp edx, 25
    jae normal_j2
    cmp eax, 25
    jb  normal_j2

    mov eax, 64
    jmp done

normal_j2:
    jmp wrap_done

; --------------------------------------------------

portal_j3:
    ; J3 portal = 38 - zona 70

    cmp edx, 38
    jae normal_j3
    cmp eax, 38
    jb  normal_j3

    mov eax, 70
    jmp done

normal_j3:

wrap_done:
    jmp done

; ============================================================
; 4) MOVIMIENTO EN ZONA SEGURA
; ============================================================
mover_seguro:
    add eax, ebx

    ; Jugador 0: meta en 57
    cmp ecx, 0
    jne meta_j1
    cmp eax, 57
    jle done
    mov eax, 100
    jmp done

meta_j1:
    ; Jugador 1: meta 63
    cmp ecx, 1
    jne meta_j2
    cmp eax, 63
    jle done
    mov eax, 100
    jmp done

meta_j2:
    ; Jugador 2: meta 69
    cmp ecx, 2
    jne meta_j3
    cmp eax, 69
    jle done
    mov eax, 100
    jmp done

meta_j3:
    ; Jugador 3: meta 75
    cmp eax, 75
    jle done
    mov eax, 100
    jmp done

; ============================================================
ya_meta:
    mov eax, 100

; ============================================================
done:
    ret 12
moverFicha ENDP

END
