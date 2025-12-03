; bridge.asm
.686
.model flat, stdcall
.stack 4096

PUBLIC sumarDosNumeros
PUBLIC restarDosNumeros
PUBLIC tirarDado
PUBLIC getTurno
PUBLIC avanzarTurno
PUBLIC puedeSacarFicha
PUBLIC esComida
PUBLIC esVictoria
PUBLIC esBloqueo

.data
semilla DWORD 0
inicializada BYTE 0

turnoActual DWORD 0       


.code

; int sumarDosNumeros(int a, int b)

sumarDosNumeros PROC STDCALL
    mov eax, [esp+4]
    add eax, [esp+8]
    ret 8
sumarDosNumeros ENDP

; int restarDosNumeros(int a, int b)

restarDosNumeros PROC STDCALL
    mov eax, [esp+4]
    sub eax, [esp+8]
    ret 8
restarDosNumeros ENDP


tirarDado PROC STDCALL
    cmp inicializada, 0
    jne Continuar

    RDTSC
    mov semilla, eax
    mov inicializada, 1

Continuar:
    mov eax, semilla
    mov ecx, 1103515245
    mul ecx
    add eax, 12345
    mov semilla, eax

    mov ebx, 6
    mov edx, 0
    div ebx
    inc edx
    mov eax, edx
    ret 0
tirarDado ENDP


getTurno PROC STDCALL
    mov eax, turnoActual
    ret 0
getTurno ENDP


avanzarTurno PROC STDCALL
    mov eax, turnoActual
    inc eax
    cmp eax, 4
    jl Guardar
    mov eax, 0

Guardar:
    mov turnoActual, eax
    ret 0
avanzarTurno ENDP



; int puedeSacarFicha(int dado)
; retorna 1 si dado == 6

puedeSacarFicha PROC STDCALL
    mov eax, [esp+4]     ; dado
    cmp eax, 6
    jne noPasa
    mov eax, 1
    ret 4
noPasa:
    mov eax, 0
    ret 4
puedeSacarFicha ENDP


; int esComida(int posA, int jugA, int posB, int jugB)
; retorna 1 si posA == posB y jugA != jugB

esComida PROC STDCALL
    mov eax, [esp+4]     ; posA
    mov ebx, [esp+8]     ; jugA
    mov ecx, [esp+12]    ; posB
    mov edx, [esp+16]    ; jugB

    cmp eax, ecx         ; misma posición?
    jne noComida
    cmp ebx, edx         ; mismo jugador?
    je noComida

    mov eax, 1
    ret 16

noComida:
    mov eax, 0
    ret 16
esComida ENDP


; int esVictoria(int f1, int f2, int f3, int f4)
; si las 4 fichas == 57 se toma como victoria

esVictoria PROC STDCALL
    mov eax, [esp+4]
    cmp eax, 57
    jne noGana
    mov eax, [esp+8]
    cmp eax, 57
    jne noGana
    mov eax, [esp+12]
    cmp eax, 57
    jne noGana
    mov eax, [esp+16]
    cmp eax, 57
    jne noGana

    mov eax, 1
    ret 16

noGana:
    mov eax, 0
    ret 16
esVictoria ENDP


; int esBloqueo(int f1, int f2, int f3, int f4)
; Detecta si 2 o más fichas propias están en la misma casilla

esBloqueo PROC STDCALL
    mov eax, [esp+4]     ; f1
    mov ebx, [esp+8]     ; f2
    mov ecx, [esp+12]    ; f3
    mov edx, [esp+16]    ; f4

    ; Comparaciones entre fichas
    cmp eax, ebx
    je bloqueo
    cmp eax, ecx
    je bloqueo
    cmp eax, edx
    je bloqueo

    cmp ebx, ecx
    je bloqueo
    cmp ebx, edx
    je bloqueo

    cmp ecx, edx
    je bloqueo

    mov eax, 0
    ret 16

bloqueo:
    mov eax, 1
    ret 16
esBloqueo ENDP


END
