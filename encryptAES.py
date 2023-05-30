import Expand_Key_AES as AES

AES_key = "2b7e151628aed2a6abf7158809cf4f3c"

AES.ImportKey(AES_key)

def add_zero(NumOfZero):
    zero = ""
    for i in range(NumOfZero):
        zero = zero + "0"
    return zero

# with open('C:/Users/ductm/Desktop/Code Python/plaintext_before.txt', 'r') as file:
#     input_encrypt = file.read()    

with open('C:/Users/ductm/Desktop/Code Python/plaintext_before.txt', 'r') as file:
    input_encrypt = file.read()

input_encrypt = ''.join(format(ord(c), '02x') for c in input_encrypt)

print(input_encrypt)

if len(input_encrypt)<=32:
    input_encrypt+=add_zero(32 - len(input_encrypt))
    
elif len(input_encrypt) % 32 != 0 :
    additional_bit = len(input_encrypt)%32
    input_encrypt+=add_zero(32 - additional_bit)



AES_input = {}

for i in range(len(input_encrypt)//32):
    AES_input[i] = input_encrypt[i*32:(i+1)*32]


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

def ShiftRow(Input_Matrix):
    temp1 = Input_Matrix[(1,1)]+Input_Matrix[(1,2)]+Input_Matrix[(1,3)]+Input_Matrix[(1,0)]
    for j in range(4):
        Input_Matrix[(1,j)] = temp1[j*2:j*2+2]
        
    temp2 = Input_Matrix[(2,2)]+Input_Matrix[(2,3)]+Input_Matrix[(2,0)]+Input_Matrix[(2,1)]
    for j in range(4):
        Input_Matrix[(2,j)] = temp2[j*2:j*2+2]

    temp3 = Input_Matrix[(3,3)]+Input_Matrix[(3,0)]+Input_Matrix[(3,1)]+Input_Matrix[(3,2)]
    for j in range(4):
        Input_Matrix[(3,j)] = temp3[j*2:j*2+2]

    return Input_Matrix
    
def MixColumns(Input_Matrix):
    constant_matrix = [
        ["02", "03", "01", "01"],
        ["01", "02", "03", "01"],
        ["01", "01", "02", "03"],
        ["03", "01", "01", "02"]
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
        

def encrypt(key,input):
    input = Convert_to_matrix(input)
    key = Convert_to_matrix(key)
    #vòng 1
    input = Add_Round_Key(input,key)
    
    
    for count in range(1,10):
        #subbyte
        for i in range(4):
            for j in range(4):
                input[(i,j)] = AES.subbyte(int(input[(i,j)],16))
        
        #shiftrow
        input = ShiftRow(input)
    
        #mix_columns
        input = MixColumns(input) 
        key = ''.join(key.values())
        key = AES.findRoundKey(key,count)

        key = Convert_to_matrix(key)
        
        #add round key
        input = Add_Round_Key(input,key)
    

    # vòng 10
    key = ''.join(key.values())
    key = AES.findRoundKey(key,10)
    key = Convert_to_matrix(key)
    for i in range(4):
        for j in range(4):
            input[(i,j)] = AES.subbyte(int(input[(i,j)],16))
    input = ShiftRow(input)
    input = Add_Round_Key(input,key)
    
    for x in range(4):
        for y in range(4):
            print(input[(x, y)], end=' ')
        print()
    return input


for i in range(len(input_encrypt)//32):
    AES_input[i] = encrypt(AES_key,AES_input[i])

# string_after_encrypt = ''.join(list(AES_input.values()))
# print(AES_input)
string_after_encrypt = ""
for x in range(len(input_encrypt)//32):
    for y in range(4):
        for z in range(4):
            string_after_encrypt+=AES_input[x][(z,y)]
with open('C:/Users/ductm/Desktop/Code Python/ciphertext.txt', 'w') as file:
    content = string_after_encrypt  # Nội dung cần ghi vào tệp tin
    file.write(content)