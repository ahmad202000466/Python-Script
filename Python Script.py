alphabet = ['a','b','c','d','e','f','g', 'h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','_']
type_list = ["wire", "reg"]
reserved_words_verilog = [
    "module", "endmodule", "begin", "end", "fork", "join",
    "reg", "wire", "integer", "real", "parameter", "localparam", "input", "output",
    "always", "initial", "always_comb", "always_latch", "always_ff", "assign",
    "if", "else", "case", "endcase", "for", "while", "repeat", "forever", "break", "continue",
    "task", "endtask", "function", "endfunction", "void", "automatic", "input", "output", "inout", "ref",
    "$display", "$monitor", "$finish", "$stop", "$time", "$random", "$readmemb", "$readmemh", "$fwrite", "$fdisplay"]
input_port_list = []
input_port_list_widths = []
input_test_cases = []

output_port_list = []
output_port_list_widths = []
output_type_list = []

input_port_list_TB = []
output_port_list_TB = []
port_init_TB = []


clk_and_reset = []
clk_and_reset_TB = []

string_to_write = []
string_to_write_seq = []

n_port = []






def add_module ():
    while(1):
        module = input ("enter the name of the module: ")
        if (module[0].lower() not in alphabet) or (module in reserved_words_verilog)  :
            print("invalid syntax")
            continue

        return (module)

def add_ports():
    check0 = 0
    check1 = 0
    while(1):
        n = int(input("enter number of ports (make sure to add more ports to clk and reset): "))
        n_input = int(input("enter number of input ports : "))
        n_output = int(input("enter number of output ports : "))
        if ((n_input+n_output) != n) or (n_input == 0) or(n_output == 0) :
            print("invalid number of ports")
            continue
        # checking syntax of the input port
        n_port.append(n_input)
        n_port.append(n_output)
        for i in range (n_input):
            port = input("enter input port name : ")
            width = int(input("enter width : (for clk and reset, make sure width = 1) "))
            if (port[0].lower() not in alphabet) or (width == 0) or (port in reserved_words_verilog):
                check0 = check0+1
                input_port_list.clear()
                input_port_list_widths.clear()
                break
            else:
                input_port_list.append(port)
                input_port_list_widths.append(width-1)
        if check0 != 0:
            check0 = 0
            print("enter correct syntax for the name of ports, or enter valid width ")
            input_port_list.clear()
            input_port_list_widths.clear()
            continue
        #end of checking
        
        #checking if port is repeated
        for i in range (len(input_port_list)):
            for j in range (len(input_port_list)):
                if i==j:
                    continue
                if input_port_list[i].lower() == input_port_list[j].lower():
                    check1 = check1 + 1
                    input_port_list.clear()
                    input_port_list_widths.clear()
                    break
            if check1 !=0:
                break
        if check1 != 0:
            check1 = 0
            print("you have repeated name for ports ")
            input_port_list.clear()
            input_port_list_widths.clear()
            continue
        
        
        # checking syntax of the output port
        for i in range (n_output):
            port = input("enter output port name : ")
            width = int(input("enter width : "))
            out_type = input ("enter output type (wire, reg) : ")
            if (port[0].lower() not in alphabet)or (width == 0) or (out_type.lower() not in type_list) or(port in reserved_words_verilog):
                check0 = check0+1
                output_port_list.clear()
                output_port_list_widths.clear()
                output_type_list.clear()
                break
            else:
                output_port_list.append(port)
                output_port_list_widths.append(width-1)
                output_type_list.append(out_type)
                
        if check0 != 0:
            check0 = 0
            print("enter correct syntax for the port type ")
            output_port_list.clear()
            output_port_list_widths.clear()
            output_type_list.clear()
            continue
        #end of checking
        
        #checking for repeated ports
        for i in range (len(output_port_list)):
            for j in range (len(output_port_list)):
                if i==j:
                    continue
                if output_port_list[i].lower() == output_port_list[j].lower():
                    check1 = check1 + 1
                    output_port_list.clear()
                    output_port_list_widths.clear()
                    output_type_list.clear()
                    break
            if check1 !=0:
                break
        if check1 != 0:
            check1 = 0
            print("you have repeated name for ports ")
            output_port_list.clear()
            output_port_list_widths.clear()
            output_type_list.clear()
            continue
        print (input_port_list)
        print (output_port_list)   
        break


           
#function to put the inputs in a list for writing       
def input_ports():
    for i in range (len(input_port_list)):
        if input_port_list_widths[i] > 0:
            input_large = f"input [{input_port_list_widths[i]}:0] {input_port_list [i]}; \n"
            
        else:
            input_large = f"input {input_port_list [i]}; \n"
        string_to_write.append(input_large)
  #function to put the outputs in a list for writing          
def output_ports():
    for i in range (len(output_port_list)):
        if output_port_list_widths[i] > 0:
            output_large = f"output {output_type_list[i]} [{output_port_list_widths[i]}:0]  {output_port_list [i]}; \n"
        else:
            output_large = f"output {output_type_list[i]} {output_port_list [i]} ; \n"      
        string_to_write.append(output_large)

def circuit_type():
    #check if circuit sequential of combinational
    while (1):
        x = int(input ("is circuit combinational or sequential? (0 for combinational and 1 for sequential) : "))
        if x == 0:
            return(0)
        elif x == 1:
            return(1)
        else:
            print("enter valid choice")
            continue

def circuit_create(choice):
    while (1):
        # sequential
        if choice == 1:
        #check if there are at least 2 available 1-bit ports
            test = 0
            for i in input_port_list_widths:
                if i == 0:
                    test = test +1
            if (test < 2):
                print("you should have input ports more than 1 with 1 bit each")
                break
            choice1 = int(input ("synchronus or asynchronus? (0 for synchronus and 1 for asynchronus) : "))
        #synchronus
            if choice1 == 0:

        #clock
                clk = input("enter clock signal: ")
                if clk not in input_port_list:   #check if the input port is available and with width = 1
                    print ("enter the correct name for the input port")
                    continue
        #reset
                reset = input("enter reset signal: ")
                if reset not in input_port_list:   #check if the input port is available and with width = 1
                    print ("enter the correct name for the input port")
                    continue
                if (input_port_list_widths[input_port_list.index(clk)] > 0) or (input_port_list_widths[input_port_list.index(reset)] > 0):
                    print("assign 1 bit ports only to clk and reset")
                    continue
         #check if clk and reset are equal to each other
                if (clk == reset):
                     print("clk and reset have the same port. invalid!")
                     continue               
        #appending on clk and reset list for testbench
                clk_and_reset.append(clk)
                clk_and_reset.append(reset)
        #clock edge conditon
                edge = int(input ("posedge or negedge? (0 for pos and 1 for neg): "))
                if edge == 0 :
                    string_to_write_seq.append(f"always@ (posedge {clk}) \n ")
                elif edge == 1:
                    string_to_write_seq.append(f"always@ (negedge {clk}) \n ")
                    
                else:
                    print("enter valid choice")
                    string_to_write_seq.clear()
                    continue
                string_to_write_seq.append("begin \n")
                
        #reset condition
                rst = int(input ("pos or neg reset? (0 for pos and 1 for neg): "))
                if rst > 1:
                    print("enter valid choice")
                    continue
                if rst == 0:
                    string_to_write_seq.append(f"if ({reset}) \n ")
    
                elif rst == 1:
                    string_to_write_seq.append(f"if (!{reset}) \n ")

                string_to_write_seq.append("begin \n")
                string_to_write_seq.append("// reset conditon \n")
                string_to_write_seq.append("end \n")
                string_to_write_seq.append("else \n")
                string_to_write_seq.append("begin \n")
                string_to_write_seq.append("//non reset conditon \n")
                string_to_write_seq.append("end \n")
                string_to_write_seq.append("end \n")
                string_to_write_seq.append("endmodule; \n")                  

                break
            
        #asynchronus   
            elif choice1 == 1:
        #clk and reset
                clk = input("enter clock signal: ")
                if clk not in input_port_list:   #check if the input port is available and with width = 1
                    print ("enter the correct name for the input port")
                    continue

                    
                reset = input("enter reset signal: ")
                if reset not in input_port_list:   #check if the input port is available and with width = 1
                    print ("enter the correct name for the input port")
                    continue
             
                
        #check if clk and reset are equal to each other
                if (clk == reset):
                    print("clk and reset have the same port. invalid!")
                    continue
                if (input_port_list_widths[input_port_list.index(clk)] > 0) or (input_port_list_widths[input_port_list.index(reset)] > 0):
                    print("assign 1 bit ports only to clk and reset")
                    continue 
        #appending on clk and reset list for testbench
                clk_and_reset.append(clk)
                clk_and_reset.append(reset)                 
        #edge part
                edge = int(input ("posedge or negedge clk? (0 for pos and 1 for neg): "))
                rst = int(input ("posedge or negedge reset? (0 for posedge and 1 for negedge): "))
        #edge conditon check
        
                if edge == 0 and rst == 0:
                    string_always = f"always@ (posedge {clk} or posedge {reset}) \n "
                   
                elif edge == 0 and rst == 1:
                    string_always =f"always@ (posedge {clk} or negedge {reset}) \n "
                elif edge == 1 and rst == 0:
                    string_always =f"always@ (negedge {clk} or posedge {reset}) \n "                    
                elif edge == 1 and rst == 1:
                    string_always =f"always@ (negedge {clk} or negedge {reset}) \n "
                                     
                else:
                    print("enter valid choice")
                    string_to_write_seq.clear()
                    continue
                string_to_write_seq.append(string_always)
        #reset condition
                string_to_write_seq.append("begin \n")
                rst = int(input ("pos or neg reset? (0 for pos and 1 for neg) : "))
                if rst == 0:
                    string_to_write_seq.append(f"if ({reset}) \n ")     
                elif rst == 1:
                    string_to_write_seq.append(f"if (!{reset}) \n ")
                  
                else:
                    print("enter valid choice")
                    continue
                string_to_write_seq.append("begin \n")
                string_to_write_seq.append("// reset conditon \n")
                string_to_write_seq.append("end \n")
                string_to_write_seq.append("else \n")
                string_to_write_seq.append("begin \n")
                string_to_write_seq.append("//non reset conditon \n")
                string_to_write_seq.append("end \n")
                string_to_write_seq.append("end \n")
                string_to_write_seq.append("endmodule; \n")  
                break
            
            else:
               print("enter valid choice")
               continue 
        else:
            string_to_write_seq.append(" // write your logic here \n") 
            string_to_write_seq.append("endmodule; \n") 
            break
            
def add_to_file():
    while(1):
        module = add_module()
        F=open(f"{module}.txt", 'w')
        #declaring ports
        add_ports()
        ports = ','.join(input_port_list+output_port_list)
        F.write("module ")
        F.write(module)
        F.write(f" ({ports} ); \n")
        
        #input and output
        input_ports()
        output_ports()
        
        #combinational or sequential
        circuit_create(circuit_type())
        
        #writing input and output ports in file
        for i in string_to_write:
            F.write(i)
        #writing the circuit in file
        for i in string_to_write_seq:
            F.write(i)
        #close file
        F.close()
        print("done")
        y = int(input ("create another module? (1 for yes, any number for no) : "))
        if y == 1:
            continue
        else:
            break
    return (module)
    

#testbench
def testbench_creator(module):
    #module name 
    file = module + "_TB"
    F=open(f"{file}.txt", 'w')
    F.write(f"module {file} (); \n")
    #creating ports for testbench based on the design
    
    #for inputs
    for i in range (len(input_port_list)):
        input_port_list_TB.append(input_port_list[i] +"_TB")
        if input_port_list_widths[i] > 0:
           F.write (f"reg [{input_port_list_widths[i]}:0] {input_port_list_TB[i]} ; \n ")
        else:
             F.write (f"reg {input_port_list_TB[i]} ; \n ") 
        port = f".{input_port_list[i]} ({input_port_list_TB[i]})"
        port_init_TB.append(port)
     #for outputs        
    for i in range (len(output_port_list)):
        output_port_list_TB.append(output_port_list[i] +"_TB")
        if output_port_list_widths[i] > 0:
           F.write (f"wire [{output_port_list_widths[i]}:0] {output_port_list_TB[i]} ; \n ") 
        else:
             F.write (f"wire {output_port_list_TB[i]} ; \n ")  
        port = f".{output_port_list[i]} ({output_port_list_TB[i]})"
        port_init_TB.append(port)      
    
    #case if the circuit is sequential
    if clk_and_reset:
        clk_tb = clk_and_reset[0] +"_TB"
        clk_and_reset_TB.append(clk_tb)
        F.write (" always begin \n ")
        F.write (f" {clk_and_reset_TB[0]} = ~{clk_and_reset_TB[0]} ; #5 ; \n ")     #clk generation
        F.write (" end \n ")


        del input_port_list_widths[(input_port_list.index(clk_and_reset[0]))]     #remove the clk and reset input ports if exists
        input_port_list.remove(clk_and_reset[0])
        input_port_list_TB.remove(clk_and_reset_TB[0])



    #writing test cases
    
    F.write (" initial begin \n ") 
    for k in range (3): #number of test cases = 3
        for i in range (len(input_port_list)):
            for j in range (input_port_list_widths[i]+1):
                x = input(f"enter input values for {input_port_list[i]}")
                input_test_cases.append(x)
            tests = ''.join(input_test_cases)
            F.write(f"{input_port_list_TB[i]} = {tests} ; #20  ; ")
            input_test_cases.clear()
        F.write("\n")
    F.write (" end \n ") 
    #writing initialization
    init = ','.join(port_init_TB)
    F.write (f" {module} mod1 ({init}) ; \n ")    
    F.write (" endmodule \n ")   
    F.close()
    print("done test"  )     

 
testbench_creator(add_to_file())  