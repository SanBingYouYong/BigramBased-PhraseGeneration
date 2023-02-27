# BigramBased-PhraseGeneration
A bigram based approach to generate short phrases. Intention is to be used as a Chinese name generator. 

宋词三百首.json and other data from https://github.com/chinese-poetry/chinese-poetry

Guide: run generic_singletoken_bigram.py, check commandline output for now. 

## Intuition

1. From raw data, obtain unigrams and bigrams. 
2. Generating: 
   - using unigram frequencies, sample a unigram as the "leading unigram"
   - using the leading unigram, collect a pool of bigrams that start with it. 
   - from the selected bigrams, with normalized probabilities, sample a final bigram. 

## Example Outputs
(s denotes start of sentence, /s the end of sentence; can be interpreted as "" in the final results; haven't added filtering)

from 宋词三百首

['舟横', '暝尘', '溪深', '影横', '中年', '珠坠', '照</s>', '处问', '歌长', '草</s>']

['际烟', '山千', '暮雨', '片片', '数</s>', '带脂', '练秋', '凄情', '事古', '是豪']


from 楚辞: 

['之卑', '嗟尔', '来者', '君之', '迁</s>', '怐愗', '以须', '殪兮', '余之', '佩之']

['哀众', '奉帝', '怀逝', '杂菜', '兮谗', '陆</s>', '兮为', '酒不', '後下', '远之']


from 李世民诗选:

['靜戈', '聞弦', '驚禽', '鏡上', '無定', '佩蘭', '淨峰', '景洛', '疏派', '雲飄']

['撫躬', '結伴', '嗣雲', '瑣除', '樹</s>', '姓玉', '銜宵', '條風', '豈必', '笥</s>']


from 曹操诗选:

['沉吟', '贯日', '金阶', '彼洛', '人俱', '饮酒', '弗忧', '何困', '之</s>', '高冈']

['东到', '不可', '千秋', '颈长', '尊</s>', '卒来', '离</s>', '以咏', '乔乃', '不相']

