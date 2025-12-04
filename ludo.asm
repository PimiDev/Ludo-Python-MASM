.686
.model flat, stdcall
.stack 4096

PUBLIC tirarDado
PUBLIC getTurno
PUBLIC avanzarTurno
PUBLIC puedeSacarFicha
PUBLIC moverFicha
PUBLIC traducirPosicion

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


; DWORD moverFicha(DWORD posActual, DWORD pasos, DWORD jugador)
moverFicha PROC STDCALL posActual:DWORD, pasos:DWORD, jugador:DWORD
    mov eax, posActual
    mov ebx, pasos
    mov ecx, jugador

    ; Si está en casa (-1)
    cmp eax, -1
    jne verificar_seguro

    ; Solo puede salir con 6
    cmp ebx, 6
    jne stay_home
    
    ; Salir a la primera casilla según jugador
    cmp ecx, 0
    je jugador0_salida
    cmp ecx, 1
    je jugador1_salida
    cmp ecx, 2
    je jugador2_salida
    ; jugador 3
    mov eax, 39
    jmp done

jugador0_salida:
    mov eax, 0
    jmp done
jugador1_salida:
    mov eax, 13
    jmp done
jugador2_salida:
    mov eax, 26
    jmp done

stay_home:
    mov eax, -1
    jmp done

verificar_seguro:
    ; Si está en zona segura (pos >= 52)
    cmp eax, 52
    jae mover_en_seguro

    ; Movimiento normal en tablero principal
    add eax, ebx
    
    ; Verificar si pasa por entrada a zona segura
    cmp ecx, 0
    jne check_jugador1
    ; Jugador 0 - entrada en casilla 51
    cmp eax, 52
    jl check_wrap
    mov eax, 52  ; entrar a zona segura
    jmp done

check_jugador1:
    cmp ecx, 1
    jne check_jugador2
    ; Jugador 1 - entrada después de casilla 12
    cmp eax, 13
    jl check_wrap
    ; Si pasa de 13, ir a zona segura
    sub eax, 13
    add eax, 52
    jmp done

check_jugador2:
    cmp ecx, 2
    jne check_jugador3
    ; Jugador 2 - entrada después de casilla 25
    cmp eax, 26
    jl check_wrap
    ; Si pasa de 26, ir a zona segura
    sub eax, 26
    add eax, 58  ; 52 + 6
    jmp done

check_jugador3:
    ; Jugador 3 - entrada después de casilla 38
    cmp eax, 39
    jl check_wrap
    ; Si pasa de 39, ir a zona segura
    sub eax, 39
    add eax, 64  ; 52 + 12
    jmp done

check_wrap:
    ; Wrap alrededor del tablero (0-51)
    cmp eax, 51
    jle done
    sub eax, 52
    jmp done

mover_en_seguro:
    ; Ya está en zona segura (52-57 para jugador 0)
    add eax, ebx
    cmp eax, 58
    jl done
    mov eax, 58  ; Llegó a la meta
    jmp done

done:
    ret 12
moverFicha ENDP



; DWORD traducirPosicion(DWORD jugador, DWORD pos)
traducirPosicion PROC jugador:DWORD, pos:DWORD

    mov eax, pos

    ; ZONA SEGURA (52+)
    cmp eax, 52
    jae seguro

    ; CAMINO GLOBAL 0–51
    mov ecx, jugador
    mov edx, 13
    imul ecx, edx
    add eax, ecx
    mov edx, 52
    div edx
    mov eax, edx
    ret

seguro:
    sub eax, 52
    mov ecx, jugador
    mov edx, 6
    imul ecx, edx
    add eax, ecx
    add eax, 52
    ret

traducirPosicion ENDP


END
