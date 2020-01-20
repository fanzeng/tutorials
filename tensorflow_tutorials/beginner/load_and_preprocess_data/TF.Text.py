# -*- coding: utf-8 -*-
from __future__ import print_function
import tensorflow as tf
print('tf.__version__ =', tf.__version__)
import tensorflow_text as text

docs = tf.constant([u'Everything not saved will be lost.'.encode('UTF-16-BE'), u'Sad☹'.encode('UTF-16-BE')])
print('docs =', docs)
utf8_docs = tf.strings.unicode_transcode(docs, input_encoding='UTF-16-BE', output_encoding='UTF-8')
print('utf8_docs =', utf8_docs)

t = ['Everything not saved will be lost.', u'Sad☹'.encode('UTF-8')]
tokenizer = text.WhitespaceTokenizer()
tokens = tokenizer.tokenize(t)

print('tokens.to_list() =', tokens.to_list())

tokenizer = text.UnicodeScriptTokenizer()
tokens = tokenizer.tokenize(t)
print('tokens.to_list() =', tokens.to_list())


tokens = tf.strings.unicode_split([u"仅今年前".encode('UTF-8')], 'UTF-8')
print('tokens.to_list() =', tokens.to_list())

tokenizer = text.UnicodeScriptTokenizer()
tokens, offset_starts, offset_limits = tokenizer.tokenize_with_offsets(t)
print('tokens.to_list() =', tokens.to_list())
print('offset_starts.to_list() =', offset_starts.to_list())
print('offset_limits.to_list() =', offset_limits.to_list())

docs = tf.data.Dataset.from_tensor_slices([['Never tell me the odds.'], ["It's a trap!"]])
tokenizer = text.WhitespaceTokenizer()
tokenized_docs = docs.map(lambda x: tokenizer.tokenize(x))
iterator = iter(tokenized_docs)
print('next(iterator).to_list() = ', next(iterator).to_list())
print('next(iterator).to_list() = ', next(iterator).to_list())

tokenizer = text.WhitespaceTokenizer()
tokens = tokenizer.tokenize(t)
f1 = text.wordshape(tokens, text.WordShape.HAS_TITLE_CASE)
f2 = text.wordshape(tokens, text.WordShape.IS_UPPERCASE)
f3 = text.wordshape(tokens, text.WordShape.HAS_SOME_PUNCT_OR_SYMBOL)
f4 = text.wordshape(tokens, text.WordShape.IS_NUMERIC_VALUE)
print('tokens.to_list() =', tokens.to_list())
print('f1.to_list() =', f1.to_list())
print('f2.to_list() =', f2.to_list())
print('f3.to_list() =', f3.to_list())
print('f4.to_list() =', f4.to_list())

tokenizer = text.WhitespaceTokenizer()
tokens = tokenizer.tokenize(t)
bigrams = text.ngrams(tokens, 2, reduction_type=text.Reduction.STRING_JOIN)
print('bigrams.to_list() =', bigrams.to_list())