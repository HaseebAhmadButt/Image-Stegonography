import random, numpy as np, colorama as co, math as m, cv2
class Encrypt:
    # Combinations to detect the end of stored data
    __combinations = ['^|!', '^!|', '!^|', '!|^', '|!^', '|^!']

    def __init__(self):
        pass

    # This is private method, which receives, the character
    # Which is to be encoded in 12-bits
    def __hash_function(self, word):
        hashed_value = list()
        bits = self.__int2bits(ord(word))

        # Adding 2 bits after every 4 bits to increase the length of total bits
        for i in range(0, 8, 4):
            hashed_value.extend([bits[i], bits[i + 1], bits[i + 2], bits[i + 3]] + self.__getValue(bits[i], bits[i + 1]))
        # Then applying different swapping to increase the security
        return self.__even_to_odd(self.__swape_value_inversely(hashed_value))

    # This function receives two bits and
    # return 2 bits according to the received bits
    def __getValue(self, bit1, bit2):
        # list of expected 2 bits combination
        input = [['0', '0'], ['0', '1'], ['1', '0'], ['1', '1']]
        # list of corresponding 2 bits combination, according to the input combination
        output = [['1', '1'], ['1', '0'], ['0', '1'], ['0', '0']]
        for item in range(4):
            if (input[item][0] == bit1) and (input[item][1] == bit2):
                return output[item]
            else:
                continue

    # This method breaks the total list of bits which is of
    # 12 bits in three segments, then swap the first and last segment with
    # each other
    def __swape_value_inversely(self, bits_string):
        # Length Of Total Bits is 12, already defined
        for i in range(4):
            temp = bits_string[i]
            bits_string[i] = bits_string[i + 8]
            bits_string[i + 8] = temp

        return bits_string

    # This method swaps each even index bit with its next odd
    # index bit, then checks if both are same then invert
    # those two bits, else remain same
    def __even_to_odd(self, bits_string):
        for i in range(0, 12, 2):
            # Swapping two bits
            temp = bits_string[i]
            bits_string[i] = bits_string[i + 1]
            bits_string[i + 1] = temp
            # If they are same, invert both the bits
            if bits_string[i] == bits_string[i + 1]:
                if bits_string[i] == '1':
                    bits_string[i], bits_string[i + 1] = '0', '0'
                else:
                    bits_string[i], bits_string[i + 1] = '1', '1'
        return bits_string

    # This method will generate a random number, between 0-5
    # this number is used to select any combination from combinations list
    def __final_combination(self):
        return self.__combinations[random.randint(0, 5)]

    # Return list of bits according to the passed
    # Character
    def __int2bits(self, value):
        bits = format(value, '08b')
        List = list()
        for i in bits:
            List.append(i)
        return List

    # Return integer value of passed bits
    def __bits2int(self, bits_list):
        return int(''.join(str(e) for e in bits_list), 2)

    # This method takes character, and 3 pixels on which the character is to stored
    # And returns the new value after embedding the character to those three pixels
    def __encryption(self, data, pixel1, pixel2, pixel3):
        # different methods are called bits for each of
        # passed value
        word_to_bits = self.__hash_function(data)
        first_cell = self.__int2bits(pixel1)
        second_cell = self.__int2bits(pixel2)
        third_cell = self.__int2bits(pixel3)
        index = 4
        # Embedding character to pixel values
        for k in range(4):
            first_cell[index] = word_to_bits[k]
            second_cell[index] = word_to_bits[k + 4]
            third_cell[index] = word_to_bits[k + 8]
            index += 1
        return self.__bits2int(first_cell), self.__bits2int(second_cell), self.__bits2int(third_cell)

    # This is used in decryption, which will give the
    # exact 8-bits of character from 12-bits
    def __getMain_bits(self, bits_list):
        List = list()
        List.extend(bits_list[0:4])
        List.extend(bits_list[6:10])
        return List

    # This method is used to retrieve character from
    # passed pixel values
    def __correct_value(self, pixel1, pixel2, pixel3):
        Output = list()
        # converting each pixel value to its corresponding bits
        returned_list = [self.__int2bits(pixel1), self.__int2bits(pixel2), self.__int2bits(pixel3)]
        # Selecting 4 Right most bits from bits of each pixel
        for i in range(3):
            Output.extend(returned_list[i][4:])
        # Now applying each method of encryption on retrieved bits to
        # reverse the value encrypted in these bits
        value_stored = chr(self.__bits2int(self.__getMain_bits(self.__swape_value_inversely(self.__even_to_odd(Output)))))
        return value_stored

    # This method tells if the detected combination is from the stored
    # combinations or it is part of message stored in image
    def __getCombination(self, combination):
        if combination in self.__combinations:
            return True
        else:
            return False

    # Used to convert list to string
    def __list_str(self, list):
        output = ""
        for j in list:
            output += j
        return output

    # Method is called to store data in grayscale image
    def data_to_gray_image(self, img, data):
        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.array(img)
        if isinstance(data, list):
            data = self.__list_str(data)
        if isinstance(data, str):
            pass
        else:
            data = str(data)
        index_counter_data = 0
        combination_index = 0
        flag = None
        pattern = self.__final_combination()
        if img.ndim == 2:
            height, width = img.shape
            if width % 3 == 0:
                pass
            else:
                width = m.floor(width / 3) * 3
            for i in range(height - 1):
                for j in range(0, width, 3):
                    # keeping check on passed data to
                    # tell the user if all data is stored or not
                    if index_counter_data < len(data):
                        img[i, j], img[i, j + 1], img[i, j + 2] = self.__encryption(data[index_counter_data], img[i, j],
                                                                                    img[i, j + 1], img[i, j + 2])
                        index_counter_data += 1
                        flag = False
                    else:
                        flag = True
                        # Since We are calculating columns by converting total columns to the multiple of 3
                        # Each Character will again consume 3 pixels to hold value
                        # Then the remaining columns of row should also be the multiple of 3
                        if combination_index < len(pattern):
                            img[i, j], img[i, j + 1], img[i, j + 2] = self.__encryption(pattern[combination_index],
                                                                                        img[i, j], img[i, j + 1],
                                                                                        img[i, j + 2])
                            combination_index += 1
                        if combination_index >= len(pattern):
                            break

                    if combination_index >= len(pattern):
                        break

            # Means Complete Data was not stored in the file
            # Data is much larger than storing capacity of image
            if not flag:
                for j in range(0, 9, 3):
                    img[height - 1, j], img[height - 1, j + 1], img[height - 1, j + 2] = self.__encryption(
                        pattern[combination_index], img[i, j], img[height - 1, j + 1], img[height - 1, j + 2])
                    combination_index += 1
                return [img, False]
            # Data is stored in the image completely
            # But combination is not stored completely, so embedding combination in the next row
            elif flag and combination_index < len(pattern):
                row_index = 9 - (combination_index * 3)
                for j in range(0, row_index, 3):
                    img[height - 1, j], img[height - 1, j + 1], img[height - 1, j + 2] = self.__encryption(
                        pattern[combination_index], img[height - 1, j], img[height - 1, j + 1], img[height - 1, j + 2])
                    combination_index += 1
                return [img, True]

            # Data and Combination Index both are stored Completely
            else:
                return [img, True]
        else:
            raise ValueError("Only Grayscale Images Are Acceptable")

    # Method is called to retrieve data in grayscale image
    def img_gray_to_data(self, img):
        List = img.split('.')
        if List[len(List) - 1] == "bmp" or List[len(List) - 1] == "png" or List[len(List) - 1] == "tiff" :
            pass
        else:
            raise ValueError("File Format Not Supported")
        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.array(img)
        output_string = ""
        combination = ""
        flag = None
        if img.ndim == 2:
            height, width = img.shape
            if width % 3 == 0:
                pass
            else:
                width = m.floor(width / 3) * 3
            for i in range(height):
                for j in range(0, width, 3):
                    # retrieve each character and store in the private string variable
                    character = self.__correct_value(img[i, j], img[i, j + 1], img[i, j + 2])
                    if character != "^" and character != "!" and character != "|":
                        if(combination!=""):
                            output_string+=combination
                            combination=""
                            output_string = output_string + character
                        else:
                            output_string = output_string + character

                    else:
                        # if part final combination is detected, then check the pattern
                        # if it belongs to document or it is the ending of document
                        combination = combination + character
                        if len(combination) >= 3:
                            flag = self.__getCombination(combination)
                            if flag:
                                break
                if flag:
                    break
            return output_string
        else:
            raise ValueError("Only Grayscale Images Are Acceptable")

    # Method is called to store data in RGB image
    def data_to_img_rgb(self, img, data):
        img = cv2.imread(img)
        if isinstance(data, list):
            data = self.__list_str(data)
        if isinstance(data, str):
            pass
        else:
           data = str(data)
        index_counter_data = 0
        combination_index = 0
        flag = None
        pattern = self.__final_combination()
        if img.ndim == 3:
            height, width, channel = img.shape
            if width % 2 == 0:
                pass
            else:
                width = m.floor(width / 2) * 2
            for i in range(height - 1):
                for j in range(0, width, 2):
                    # keeping check on passed data to
                    # tell the user if all data is stored or not
                    if index_counter_data < len(data):
                        img[i, j, 0], img[i, j, 1], img[i, j + 1, 2] = \
                            self.__encryption(data[index_counter_data], img[i, j, 0], img[i, j, 1], img[i, j + 1, 2])
                        index_counter_data += 1
                        flag = False
                    else:
                        flag = True
                        # Since We are calculating columns by converting total columns to the multiple of 2
                        # Each Word will again consume 2 pixels to hold value
                        # Then the remaining columns of row should also be the multiple of 2
                        if combination_index < len(pattern):
                            img[i, j, 0], img[i, j, 1], img[i, j + 1, 2] = \
                                self.__encryption(pattern[combination_index], img[i, j, 0], img[i, j, 1], img[i, j + 1, 2])
                            combination_index += 1
                        else:
                            break
                if combination_index >= len(pattern):
                    break
            # Means Complete Data was not stored in the file
            # Data is much larger than storing capacity of image
            if not flag:
                for j in range(0, 6, 2):
                    img[height - 1, j, 0], img[height - 1, j, 1], img[height - 1, j + 1, 2] = \
                        self.__encryption(pattern[combination_index], img[height - 1, j, 0], img[height - 1, j, 1],
                                          img[height - 1, j + 1, 2])
                    combination_index += 1
                return [img, False]
            # # Data is stored in the image completely
            # # But combination is not stored completely, so embedding combination in the next row
            elif flag and combination_index < len(pattern):
                row_index = 6 - (combination_index * 2)
                for j in range(0, row_index, 2):
                    img[height - 1, j, 0], img[height - 1, j, 1], img[height - 1, j + 1, 2] = \
                        self.__encryption(pattern[combination_index], img[height - 1, j, 0], img[height - 1, j, 1],
                                          img[height - 1, j + 1, 2])
                    combination_index += 1
                return [img, True]

            # Data and Combination Index both are stored Completely
            else:
                return [img, True]
        else:
            raise ValueError("Only RGB Images Are Acceptable")

    # Method is called to retrieve data in RGB image
    def img_rgb_to_data(self, img):
        List = img.split('.')
        if List[len(List) - 1] == "bmp" or List[len(List) - 1] == "png" or List[len(List) - 1] == "tiff" :
            pass
        else:
            raise ValueError("File Format Not Supported")
        img = cv2.imread(img)
        output_string = ""
        combination = ''
        flag = False
        if img.ndim == 3:
            height, width, channels = img.shape
            if width % 2 == 0:
                pass
            else:
                width = m.floor(width / 2) * 2
            k = 0
            for i in range(height):
                for j in range(0, width, 2):
                    # retrieve each character and store in the private string variable
                    character = self.__correct_value(img[i, j, 0], img[i, j, 1], img[i, j + 1, 2])
                    if character != "^" and character != "!" and character != "|":
                        if(combination!=""):
                            output_string+=combination
                            combination=""
                            output_string = output_string + character
                        else:
                            output_string = output_string + character
                    else:
                        # if part of final combination is detected, then check the pattern
                        # if it belongs to document or it is the ending of document
                        combination += character
                        if len(combination) >= 3:
                            flag = self.__getCombination(combination)
                            if flag:
                                break
                if flag:
                    break
            return output_string
        else:
            raise ValueError("Only RGB Images Are Acceptable")
