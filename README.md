# FormatString

Part 1:
Develop an exploit that injects reverse/callback shellcode as part of the user supplied input and transfers control to that shell code. You must utilize shellcode that results in an interactive shell. Your shellcode must not depend on the presence of any executable other than /bin/sh

Part 2: 
Create an exploit which in a single connection to a target, determines a good address for your shellcode, then without disconnecting, or establishing a second connection, generates and sends the additional data to exploit and obtain a shell on the target which you use without any additional network connections taking place

Part 3:
payload should make use of system calls to open a file named “key”, read the content of that file and send that content back to your attacking computer over a network socket.
