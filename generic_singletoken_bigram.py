import json
import random
from nltk import MLEProbDist, FreqDist


excludes = ["<s>", "</s>", "。", "，", "、", "：", "“", "”", "？"]

class GenericSingleTokenBigramModel():
    def __init__(self) -> None:
        self.estimator = estimator = lambda fdist, bins: MLEProbDist(fdist)
        self.raw_data = self.load_data("宋词三百首.json", "paragraphs")
        self.cleaned_tokens = self.clean_token(self.raw_data)
        self.unigrams = self.build_unigrams(self.cleaned_tokens)
        self.bigrams = self.build_bigrams(self.cleaned_tokens)

    def load_data(self, data_file: str, data_content_tag: str) -> list:
        with open(data_file, 'r', encoding="utf8") as raw:
            data = json.load(raw)
            contents = [content[data_content_tag] for content in data]
        return contents

    def clean_token(self, contents: list) -> list:
        tokens = [item for sublist in contents for item in sublist]
        cleaned_tokens = []
        for token in tokens:
            cleaned_token = []
            for c in token:
                if c not in excludes:
                    cleaned_token.append(c)
            cleaned_token = "".join(cleaned_token)
            cleaned_tokens.append(cleaned_token)
        return cleaned_tokens
    
# Note: added normalization for FreqDist values! 

    def build_bigrams(self, tokens: list) -> FreqDist:
        bigrams = []
        for token in tokens:
            token_bigrams = []
            for i in range(len(token)):
                if i == 0:
                    bigram_list = ["<s>", token[i]]
                    token_bigrams.append("".join(bigram_list))
                else:
                    bigram_list = [token[i - 1], token[i]]
                    token_bigrams.append("".join(bigram_list))
            final_list = [token[i], "</s>"]
            token_bigrams.append("".join(final_list))
            bigrams += token_bigrams
        # normalize step
        freq_dist = FreqDist(bigrams)
        total = freq_dist.N()
        for word in freq_dist:
            freq_dist[word] /= float(total)
        return freq_dist

    def build_unigrams(self, tokens: list) -> FreqDist:
        unigrams = []
        for token in tokens:
            token_unigrams = []
            for char in token:
                token_unigrams.append(char)
            unigrams += token_unigrams
        # normalize step
        freq_dist = FreqDist(unigrams)
        total = freq_dist.N()
        for word in freq_dist:
            freq_dist[word] /= float(total)
        return freq_dist
    
    def generate(self) -> str:
        """
        Idea: choose a unigram from seen unigrams, go to bigrams which start with this unigram, and sample a "second char" from the bigrams? 
        """
        # determine first char
        chosen_unigram = None
        p = random.random()
        # print("random p is: " + str(p))
        p_cur = p
        for unigram in self.unigrams:
            uni_p = self.unigrams.freq(unigram)
            # print(uni_p)
            p_cur -= uni_p
            # print(p_cur)
            if p_cur <= 0:
                # return unigram  # shows that this part works
                chosen_unigram = unigram
                break
        #     break
        # return chosen_unigram
        if chosen_unigram is None:
            print("Unigram probability fails to determine a proper first character, randomly sampling...")
            chosen_unigram = random.choice(self.unigrams)
        # determine second char
        p = random.random()
        p_cur = p
        related_bigrams, sum_of_related_bigram_probs = self.bigrams_starting_with(chosen_unigram)
        # TODO: need to normalize for these bigrams as well! 
        for bigram in related_bigrams:
            bi_p = self.bigrams.freq(bigram) / sum_of_related_bigram_probs
            p_cur -= bi_p
            if p_cur <= 0:
                return bigram
        print("Bigram probability fails to determine a proper bigram for the leading unigram " + chosen_unigram + ", randomly selecting from related bigrams...")
        return random.choice(related_bigrams)
    
    def bigrams_starting_with(self, leading_char: str):
        wanted_bigrams = []
        sum_of_prob = 0
        for bigram in self.bigrams:  # .keys()? 
            if bigram[0] == leading_char:
                wanted_bigrams.append(bigram)
                sum_of_prob += self.bigrams.freq(bigram)
        return wanted_bigrams, sum_of_prob
    
    def generate_multiple(self, number: int) -> list:
        generated = []
        for i in range(number):
            generated.append(
                self.generate()
            )
        return generated
        
    def check_normalization(self):
        bigram_sum = sum(self.bigrams.values())
        unigram_sum = sum(self.unigrams.values())
        print("Bigram sum: " + str(bigram_sum))
        print("Unigram sum: " + str(unigram_sum))
        


if __name__ == "__main__":
    bm = GenericSingleTokenBigramModel()
    # in memorial to "舷独", the fixed result of early implementation which made me realize that the problem is normalization of probabilities. 
    generated = bm.generate_multiple(10)
    print(generated)
    



