import os
import uuid
from random import shuffle


class Preprocessor:
    path = "tagged"
    train_path = "train"
    test_path = "test"
    pos_texts = []
    neg_texts = []
    word_categories = ["NOM", "VER", "ADV", "ADJ"]
    ratio = 0.8     # 80%

    def __init__(self):
        self.pos_texts = self.read_files(self.path + "/pos")
        self.neg_texts = self.read_files(self.path + "/neg")

    def read_files(self, folderpath):
        result = {}

        for file in os.listdir(folderpath):
            text =[]
            with open(folderpath+'/'+file, 'r') as f:
                lines = f.readlines()

            for l in lines:
                l = l.rstrip()
                words = l.split("\t")
                try:
                    if words[1] in self.word_categories:
                        text.append(words[2])
                except:
                    print("Error in file " + folderpath + "/" + file + " at word " + str(words))
            result[file] = " ".join(text)
        return result

    def save_files(self):
        # create test and train folders
        if not os.path.exists(self.train_path+"/pos"):
            os.makedirs(self.train_path+"/pos")

        if not os.path.exists(self.train_path + "/neg"):
            os.makedirs(self.train_path+"/neg")

        if not os.path.exists(self.test_path+"/pos"):
            os.makedirs(self.test_path+"/pos")

        if not os.path.exists(self.test_path + "/neg"):
            os.makedirs(self.test_path+"/neg")

        total_text_list = {**self.pos_texts, **self.neg_texts}
        keys = list(total_text_list.keys())
        shuffle(keys)

        size = int(len(keys) * self.ratio)
        train_keys = keys[:size]
        test_keys = keys[size:]

        for key in train_keys:
            self.write_text(total_text_list[key], key, self.train_path)

        for key in test_keys:
            self.write_text(total_text_list[key], key, self.test_path)

    def write_text(self, text, name, path):
        if "pos" in name:
            path += "/pos"
        else:
            path += "/neg"

        with open(path+"/"+name, 'w') as file:
            file.write(text)


if __name__ == '__main__':
    preprocessor = Preprocessor()
    preprocessor.save_files()
    pass
