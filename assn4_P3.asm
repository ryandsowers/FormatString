;Code modified/updated by Ryan Sowers
;Submitted: 06/04/2018
;CS4678 Assignment 4
;Assemble: 	nasm -f bin assn4_P3.asm

bits 64

open_file:
	xor rdx, rdx
	xor rsi, rsi
	push rdx
	mov rdi, 'key' 		;load the file name 'key'
	push rdi 			;push name to stack
	mov rdi, rsp 		;create pointer to file name
	mov rax, 2			;open syscall
	syscall 			;open file 
	mov r15, rax 		;save file descriptor

loop_top:
	mov rdx, 1		;read size 1 byte
	mov rsi, rsp	;move onto stack (use stack as buffer)
	mov rdi, r15	;input from opened file
	mov eax, 0		;read system call number
	syscall			;do system call

	cmp rax, 1		;compare return value to 1
	jne all_done	;if not 1, reading is complete

	mov rdx, 1		;message length (1 byte)
	mov rsi, rsp	;pointer to message
	mov edi, 1		;output to stdout
	mov eax, 1		;write system call number
	syscall			;do system call

	jmp loop_top	;keep reading until no more bytes left (return value 0)

all_done:
	mov rdi, r15 	;retrieve fd
	mov rax, 3 		;close syscall
	syscall  		;close file

	mov edi, 0 		;exit status code 
	mov eax, 60		;exit system call number
	syscall			;do system call