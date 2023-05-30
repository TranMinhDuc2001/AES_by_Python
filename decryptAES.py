import Expand_Key_AES as AES

AES_key = "2b7e151628aed2a6abf7158809cf4f3c"
AES.ImportKey(AES_key)

with open('C:/Users/ductm/Desktop/Code Python/ciphertext.txt', 'r') as file:
    input_decrypt = file.read()


AES_output = {}

for i in range(len(input_decrypt)//32):
    AES_output[i] = input_decrypt[i*32:(i+1)*32]



a = {}
def key_expand():
    a[0] = AES_key
    a[1] = AES.findRoundKey(AES_key,1)
    a[2] = AES.findRoundKey(a[1],2)
    a[3] = AES.findRoundKey(a[2],3)
    a[4] = AES.findRoundKey(a[3],4)
    a[5] = AES.findRoundKey(a[4],5)
    a[6] = AES.findRoundKey(a[5],6)
    a[7] = AES.findRoundKey(a[6],7)
    a[8] = AES.findRoundKey(a[7],8)
    a[9] = AES.findRoundKey(a[8],9)
    a[10] = AES.findRoundKey(a[9],10)






def multiply_in_galois(a, b):
    result = 0
    while a and b:
        if b & 1:
            result ^= a
        if a & 0x80:
            a = (a << 1) ^ 0x11b
        else:
            a <<= 1
        b >>= 1
    return result


def Convert_to_matrix(str_input):
    matrix = {}
    index = 0

# Lưu trữ giá trị vào từng cặp (x, y) trong dictionary
    for y in range(4):
        for x in range(4):
            matrix[(x, y)] = str_input[index:index+2]
            index += 2
    return matrix



def Add_Round_Key(Input_Matrix,Key_Matrix):
    
    for i in range(4):
        for j in range(4):
            Input_Matrix[(i,j)] = hex(int(Key_Matrix[(i,j)],16)^int(Input_Matrix[(i,j)],16)).replace("0x","").zfill(2)
    
    return Input_Matrix

# Key_Matrix = Convert_to_matrix(AES_key)

# print(AES.subbyte(int(Key_Matrix[(0,0)],16))) #da co subbyte

def Inv_ShiftRow(Input_Matrix):
    # Input_Matrix = Convert_to_matrix(Input_Matrix)
    temp1 = Input_Matrix[(1,3)]+Input_Matrix[(1,0)]+Input_Matrix[(1,1)]+Input_Matrix[(1,2)]
    for j in range(4):
        Input_Matrix[(1,j)] = temp1[j*2:j*2+2]
        
    temp2 = Input_Matrix[(2,2)]+Input_Matrix[(2,3)]+Input_Matrix[(2,0)]+Input_Matrix[(2,1)]
    for j in range(4):
        Input_Matrix[(2,j)] = temp2[j*2:j*2+2]

    temp3 = Input_Matrix[(3,1)]+Input_Matrix[(3,2)]+Input_Matrix[(3,3)]+Input_Matrix[(3,0)]
    for j in range(4):
        Input_Matrix[(3,j)] = temp3[j*2:j*2+2]

    return Input_Matrix
    
def Inv_MixColumns(Input_Matrix):
    # Input_Matrix = Convert_to_matrix(Input_Matrix)
    constant_matrix = [
        ["0e", "0b", "0d", "09"],
        ["09", "0e", "0b", "0d"],
        ["0d", "09", "0e", "0b"],
        ["0b", "0d", "09", "0e"]
    ]
    mixed_matrix = []
    for column in range(4):
        mixed_column = []
        for row in range(4):
            result = 0
            for i in range(4):
                value = int(Input_Matrix[(i,column)],16)
                constant = int(constant_matrix[row][i],16)
                result ^= multiply_in_galois(value, constant)
            mixed_column.append(result)
        mixed_matrix.append(mixed_column)
    
    mixed_matrix = [[row[i] for row in mixed_matrix] for i in range(len(mixed_matrix[0]))] #đổi cột thành hàng của mixed_Matrix cho đúng
    

    for i in range(4):
        for j in range(4):
            Input_Matrix[(i,j)] = hex(mixed_matrix[i][j])[2:].zfill(2)
    

    
    return Input_Matrix
        
def decrypt(key,input):

    input = Convert_to_matrix(input)
    key[10] = Convert_to_matrix(key[10])

    #vòng 1
    input = Add_Round_Key(input,key[10])
    
    for count in range(1,10):
        
        #Inv_ShiftRow
        input = Inv_ShiftRow(input)
        

        #inv subbyte
        for i in range(4):
            for j in range(4):
                input[(i,j)] = AES.inv_subbyte(int(input[(i,j)],16))
        
    
        #add round key
        # print(key[10-count])
        key[10-count] = Convert_to_matrix(key[10-count])
        
        input = Add_Round_Key(input,key[10-count])
        
        #inv mix_columns
        input = Inv_MixColumns(input) 
        
    # vòng 10
    #shift row
    input = Inv_ShiftRow(input)
    #subbytes
    key[0] = ''.join(key[0])
    key[0] = Convert_to_matrix(key[0])
    for i in range(4):
        for j in range(4):
            input[(i,j)] = AES.inv_subbyte(int(input[(i,j)],16))
    #add round key
    input = Add_Round_Key(input,key[0])
    
    for x in range(4):
        for y in range(4):
            print(input[(x, y)], end=' ')
        print()
    return input

for i in range(len(input_decrypt)//32):
    key_expand()
    AES_output[i] = decrypt(a,AES_output[i])
    
string_after_decrypt = ""
for x in range(len(input_decrypt)//32):
    for y in range(4):
        for z in range(4):
            string_after_decrypt+=AES_output[x][(z,y)]
string_after_decrypt = bytes.fromhex(string_after_decrypt).decode()
with open('C:/Users/ductm/Desktop/Code Python/plaintext_after.txt', 'w') as file:
    content = string_after_decrypt  # Nội dung cần ghi vào tệp tin
    file.write(content)
