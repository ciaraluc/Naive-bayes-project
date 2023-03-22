import math, os, pickle, re
from turtle import pos 
from typing import Tuple, List, Dict
  
class BayesClassifier:
    """A simple BayesClassifier implementation

    Attributes:
        pos_freqs - dictionary of frequencies of positive words
        neg_freqs - dictionary of frequencies of negative words
        pos_filename - name of positive dictionary cache file
        neg_filename - name of positive dictionary cache file
        training_data_directory - relative path to training directory
        neg_file_prefix - prefix of negative reviews
        pos_file_prefix - prefix of positive reviews
    """

    def __init__(self):
        """Constructor initializes and trains the Naive Bayes Sentiment Classifier. If a
        cache of a trained classifier is stored in the current folder it is loaded,
        otherwise the system will proceed through training.  Once constructed the
        classifier is ready to classify input text."""
        # initialize attributes
        self.pos_freqs: Dict[str, int] = {}
        self.neg_freqs: Dict[str, int] = {}
        self.pos_filename: str = "posreviews.dat"
        self.neg_filename: str = "negreviews.dat"
        self.training_data_directory: str = "apple_iphone_11_reviews"

        # check if both cached classifiers exist within the current directory
        if os.path.isfile(self.pos_filename) and os.path.isfile(self.neg_filename):
            print("Data files found - loading to use cached values...")
            self.pos_freqs = self.load_dict(self.pos_filename)
            self.neg_freqs = self.load_dict(self.neg_filename)
        else:
            print("Data files not found - running training...")
            self.train()

    def train(self) -> None:
        """Trains the Naive Bayes Sentiment Classifier

        Train here means generates `pos_freq/neg_freq` dictionaries with frequencies of
        words in corresponding positive/negative reviews
        """
        # get the list of file names from the training data directory
        # os.walk returns a generator (feel free to Google "python generators" if you're
        # curious to learn more, next gets the first value from this generator or the
        # provided default `(None, None, [])` if the generator has no values)
        _, __, files = next(os.walk(self.training_data_directory), (None, None, []))
        if not files:
            raise RuntimeError(f"Couldn't find path {self.training_data_directory}")
        
        for index, filename in enumerate(files, 1): # type: ignore
            # print(f"Training on file {index} of {len(files)}")
            #     <the rest of your code for updating frequencies here>
            text = self.load_file(os.path.join(self.training_data_directory, filename))
       
            token=self.tokenize(text)
            
            if filename.startswith("posreviews"):
                self.update_dict(token, self.pos_freqs)
            elif filename.startswith("negreviews"):
                self.update_dict(token,self.neg_freqs)
        
        print(self.pos_freqs)
       
        self.save_dict(self.pos_freqs, self.pos_filename)
        self.save_dict(self.neg_freqs, self.neg_filename)

    def classify(self, text: str) -> str:
        """Classifies given text as positive, negative or neutral from calculating the
        most likely document class to which the target string belongs

        Args:
            text - text to classify

        Returns:
            classification, either positive, negative or neutral
        """
        tokens =self.tokenize(text)
        print(tokens)

        pos_prob=0
        neg_prob=0

    
        num_pos_words=sum(self.pos_freqs.values())
        num_neg_words=sum(self.neg_freqs.values())
        
        for word in tokens:

            num_pos_appearances=1
            if word in self.pos_freqs:
                num_pos_appearances+=self.pos_freqs[word]
            pos_prob += math.log(num_pos_appearances/num_pos_words)

            num_neg_appearances=1
            if word in self.neg_freqs:
                num_neg_appearances+=self.neg_freqs[word]
            neg_prob += math.log(num_neg_appearances/num_neg_words)
           

        print(f"pos_prob is:{pos_prob}")
        print(f"neg_prob is: {neg_prob}")



        # for debugging purposes, it may help to print the overall positive and negative
        # probabilities
        

        # determine whether positive or negative was more probable (i.e. which one was
        # larger)
        

        # return a string of "positive" or "negative"
        if pos_prob>neg_prob:
            return "positive"
        else:
            return "negative"

    def load_file(self, filepath: str) -> str:
        """Loads text of given file

        Args:
            filepath - relative path to file to load

        Returns:
            text of the given file
        """
        with open(filepath, "r", encoding='utf8') as f:
            return f.read()

    def save_dict(self, dict: Dict, filepath: str) -> None:
        """Pickles given dictionary to a file with the given name

        Args:
            dict - a dictionary to pickle
            filepath - relative path to file to save
        """
        print(f"Dictionary saved to file: {filepath}")
        with open(filepath, "wb") as f:
            pickle.Pickler(f).dump(dict)

    def load_dict(self, filepath: str) -> Dict:
        """Loads pickled dictionary stored in given file

        Args:
            filepath - relative path to file to load

        Returns:
            dictionary stored in given file
        """
        print(f"Loading dictionary from file: {filepath}")
        with open(filepath, "rb") as f:
            return pickle.Unpickler(f).load()

    def tokenize(self, text: str) -> List[str]:
        """Splits given text into a list of the individual tokens in order

        Args:
            text - text to tokenize

        Returns:
            tokens of given text in order
        """
        tokens = []
        token = ""
        for c in text:
            if (
                re.match("[a-zA-Z0-9]", str(c)) != None
                or c == "'"
                or c == "_"
                or c == "-"
            ):
                token += c
            else:
                if token != "":
                    tokens.append(token.lower())
                    token = ""
                if c.strip() != "":
                    tokens.append(str(c.strip()))

        if token != "":
            tokens.append(token.lower())
        return tokens

    def update_dict(self, words: List[str], freqs: Dict[str, int]) -> None:
        """Updates given (word -> frequency) dictionary with given words list

        By updating we mean increment the count of each word in words in the dictionary.
        If any word in words is not currently in the dictionary add it with a count of 1.
        (if a word is in words multiple times you'll increment it as many times
        as it appears)

        Args:
            words - list of tokens to update frequencies of
            freqs - dictionary of frequencies to update
        """
        for word in words:
            if word in freqs:
                freqs[word]+=1
            else:
                freqs[word]=1

if __name__ == "__main__":
    # uncomment the below lines once you've implemented `train` & `classify`
    b = BayesClassifier()
    pass