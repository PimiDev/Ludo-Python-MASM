
.686
.model flat, stdcall
.stack 4096

PUBLIC sumarDosNumeros
PUBLIC restarDosNumeros
PUBLIC tirarDado
PUBLIC getTurno
PUBLIC avanzarTurno
PUBLIC puedeSacarFicha


.data

semilla        DWORD 0
inicializada   BYTE 0

turnoActual    DWORD 0      ; 0–3


.code


; int sumarDosNumeros(int a, int b)
sumarDosNumeros PROC STDCALL a:DWORD, b:DWORD
    mov eax, a
    add eax, b
    ret 8
sumarDosNumeros ENDP

; int restarDosNumeros(int a, int b)
restarDosNumeros PROC STDCALL a:DWORD, b:DWORD
    mov eax, a
    sub eax, b
    ret 8
restarDosNumeros ENDP


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


END
