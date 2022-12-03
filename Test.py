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

"""

    path_str = " /home/elvino/Desktop"
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