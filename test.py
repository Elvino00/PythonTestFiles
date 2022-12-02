import os



def main():
    """stringa = "{" \
              "1) Desktop : /home/elvino/Desktop,\n" \
              "2) Downloads: /home/elvino/Downloads,\n" \
              "3) Templates: /home/elvino/Templates,\n" \
              "4) Public: /home/elvino/Public,\n" \
              "5) Documents: /home/elvino/Documents,\n" \
              "6) Music: /home/elvino/Music,\n" \
              "7) Pictures: /home/elvino/Pictures\n" \
              "8) Videos : /home/elvino/Videos\n" \
              "}"


    row_number = stringa.count('\n') - 1
    print(f"row_number in stringa = {row_number}")
    stringa = stringa.replace('{','')
    stringa = stringa.replace('}','')


    path_dict = {}

    print(f"path_dict length is {len(path_dict)}")

    for i in stringa.splitlines():
        mod_string = i[3:-1]
        mod_string = mod_string.split(":")
        path_dict[str(mod_string[0])] = str(mod_string[1])


    print(path_dict)"""

    path_str = "      /home/elvino/Desktop"
    count = 1
    file_number = []
    path_str = path_str.replace(" ","")
    for root, dir, files in os.walk(path_str):
        for file in files:
            print(f"{count})  {file}")  # for file with full path   os.path.join(root,file)
            file_number.append(os.path.join(root, file))
            # print(os.path.join(root,file))
            count += 1







if __name__ == "__main__":
    main()