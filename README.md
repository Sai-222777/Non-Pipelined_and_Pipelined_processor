# Non-Pipelined_and_Pipelined_processor
 Simulation of a simple processor in both Non-Pipelined and Pipelined senarios using python with binary format instructions following MIPS architecture. The input to both the senarios are taken from a machine code file. One is 'dump2.txt' which is the machine code corresponding to a simple string encrypter and decrypter (check https://github.com/Sai-222777/Basic_mips_encrypter_decrypyter for more details). Another one is 'comgaming.txt' which is the machine code for a program that computes the factorial of the input if valid. The number of clock cycles can be compared in non_pipeline and in pipeline. 


 If using 'comgaming.txt' the number to compute can be given on line 41 in pipeline.py and on line 36 in non_pipeline.py.

 If using 'dump2.txt' in pipeline.py :-
                                        on line 19 -> choice to either encode or decode in binary
                                        on line 20 -> string to be encoded or decoded can be modified
                                        on line 21 -> enter in binary the number of characters in the string
                                                      rounded up to the closest multiple of 4

 If using 'dump2.txt' in non_pipeline.py :-
                                        on line 14 -> choice to either encode or decode in binary
                                        on line 15 -> string to be encoded or decoded can be modified
                                        on line 16 -> enter in binary the number of characters in the string
                                                      rounded up to the closest multiple of 4

Suppose string is "Hello World". Has 11 characters. So round up to 12.



