# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

print('tf.constant(u"Thanks 😊") =', tf.constant(u"Thanks 😊"))

print('tf.contant([u"You\'re", u"welcome!"]).shape =', tf.constant([u"You're", u"welcome!"]).shape)
text_utf8 = tf.constant(u"语言处理")
print('text_utf8 =', text_utf8)

text_utf16be = tf.constant(u"语言处理".encode("UTF-16-BE"))
print('text_utf16be =', text_utf16be)

text_chars = tf.constant([ord(char) for char in u"语言处理"])
print('text_chars =', text_chars)

print(
    'decode text_utf8 =',
    tf.strings.unicode_decode(text_utf8, input_encoding='UTF-8')
)
print(
    'encode text_chars =',
    tf.strings.unicode_encode(text_chars, output_encoding='UTF-8')
)
print(
    'transcode text_utf8 =',
    tf.strings.unicode_transcode(text_utf8, input_encoding='UTF8', output_encoding='UTF-16-BE')
)

batch_utf8 = [
    s.encode('UTF-8') for s in [u'hÃllo',  u'What is the weather tomorrow',  u'Göödnight', u'😊']
]

batch_chars_ragged = tf.strings.unicode_decode(batch_utf8, input_encoding='UTF-8')
for sentence_chars in batch_chars_ragged.to_list():
    print('sentence_chars =', sentence_chars)

batch_chars_padded = batch_chars_ragged.to_tensor(default_value=-1)
print(
    'batch_chars_padded.numpy() =',
    batch_chars_padded.numpy()
)
batch_chars_sparse = batch_chars_ragged.to_sparse()
print(
    'batch_chars_sparse =',
    batch_chars_sparse
)
print(
    "tf.strings.unicode_encode([[99, 97, 116], [100, 111, 103], [ 99, 111, 119]], output_encoding='UTF-8') =",
    tf.strings.unicode_encode([[99, 97, 116], [100, 111, 103], [ 99, 111, 119]], output_encoding='UTF-8')
)
print(
    "tf.strings.unicode_encode(batch_chars_ragged, output_encoding='UTF-8') =",
    tf.strings.unicode_encode(batch_chars_ragged, output_encoding='UTF-8')
)

print(
    tf.strings.unicode_encode(
        tf.RaggedTensor.from_sparse(batch_chars_sparse),
        output_encoding='UTF-8'
    )
)

print(
    tf.strings.unicode_encode(
        tf.RaggedTensor.from_tensor(batch_chars_padded, padding=-1),
        output_encoding='UTF-8'
    )
)

print('-'*80)
thanks = u'Thanks 😊'.encode('UTF-8')
num_bytes = tf.strings.length(thanks).numpy()
num_chars = tf.strings.length(thanks, unit='UTF8_CHAR').numpy()
print('{} bytes; {} UTF-8 characters'.format(num_bytes, num_chars))
print(
    'tf.strings.substr(thanks, pos=7, len=1).numpy() =',
    tf.strings.substr(thanks, pos=7, len=1).numpy()
)

print(
    "tf.strings.substr(thanks, pos=7, len=1, unit='UTF8_CHAR').numpy() =",
    tf.strings.substr(thanks, pos=7, len=1, unit='UTF8_CHAR').numpy()
)

print(
    "tf.strings.unicode_split(thanks, 'UTF-8').numpy() =",
    tf.strings.unicode_split(thanks, 'UTF-8').numpy()
)

print('-'*80)
# note: the special chars in the following line may not be displayed in some IDE(s)
special_chars = u"🎈🎉🎊"
codepoints, offsets = tf.strings.unicode_decode_with_offsets(special_chars, 'UTF-8')

for (codepoint, offset) in zip(codepoints.numpy(), offsets.numpy()):
    print("At byte offset {}: codepoint {}".format(offset, codepoint))

print('-'*80)
uscript = tf.strings.unicode_script([33464, 1041])  # ['芸', 'Б']
print(uscript.numpy())  # [17, 8] == [USCRIPT_HAN, USCRIPT_CYRILLIC]

print('batch_chars_ragged =', batch_chars_ragged)
print(
    'tf.strings.unicode_script(batch_chars_ragged) =',
    tf.strings.unicode_script(batch_chars_ragged)
)

print('-'*80)
sentence_texts = [u'Hello, world.', u'世界こんにちは']
print('sentence_texts =', sentence_texts)
sentence_char_codepoint = tf.strings.unicode_decode(sentence_texts, 'UTF-8')
print('sentence_char_codepoint =', sentence_char_codepoint)
sentence_char_script = tf.strings.unicode_script(sentence_char_codepoint)
print('sentence_char_script =', sentence_char_script)

print('[sentence_char_script.nrows(), 1] =', [sentence_char_script.nrows().numpy(), 1])
print('tf.fill([sentence_char_script.nrows(), 1], True) =', tf.fill([sentence_char_script.nrows(), 1], True))
print(
    'tf.not_equal(sentence_char_script[:, 1:], sentence_char_script[:, :-1]) =',
    tf.not_equal(sentence_char_script[:, 1:], sentence_char_script[:, :-1])
)
sentence_char_starts_word = tf.concat(
    [
        tf.fill([sentence_char_script.nrows(), 1], True), # beginning of each sentence
        tf.not_equal(sentence_char_script[:, 1:], sentence_char_script[:, :-1]) # script differs from the previous char
    ],
    axis=1
)
print('sentence_char_starts_word =', sentence_char_starts_word)
print('sentence_char_starts_word.values =', sentence_char_starts_word.values)
print('tf.where(sentence_char_starts_word.values =', tf.where(sentence_char_starts_word.values))

word_starts = tf.squeeze(tf.where(sentence_char_starts_word.values), axis=1)
print('word_starts =', word_starts)
word_char_codepoint = tf.RaggedTensor.from_row_starts(
    values=sentence_char_codepoint.values,
    row_starts=word_starts
)
print('word_char_codepoint =', word_char_codepoint)

# count how many starts are there, this value is the number of words (in the sense of change of unicode script)
sentence_num_words = tf.reduce_sum(
    tf.cast(sentence_char_starts_word, tf.int64),
    axis=1
)
print('sentence_num_words =', sentence_num_words)
# asseble the words back into sentences
# pass in the number of words in each sentence as row_lengths
sentence_word_char_codepoint = tf.RaggedTensor.from_row_lengths(
    values=word_char_codepoint,
    row_lengths=sentence_num_words)
print('sentence_word_char_codepoint =', sentence_word_char_codepoint)
print(
    tf.strings.unicode_encode(sentence_word_char_codepoint, 'UTF-8').to_list()
)

