from dataclasses import dataclass
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

import numpy as np


@dataclass(frozen=True)
class SentencePair:
    """
    Contains lists of tokens (strings) for source and target sentence
    """
    source: List[str]
    target: List[str]


@dataclass(frozen=True)
class TokenizedSentencePair:
    """
    Contains arrays of token vocabulary indices (preferably np.int32) for source and target sentence
    """
    source_tokens: np.ndarray
    target_tokens: np.ndarray


@dataclass(frozen=True)
class LabeledAlignment:
    """
    Contains arrays of alignments (lists of tuples (source_pos, target_pos)) for a given sentence.
    Positions are numbered from 1.
    """
    sure: List[Tuple[int, int]]
    possible: List[Tuple[int, int]]


def extract_sentences(filename: str) -> Tuple[
    List[SentencePair], List[LabeledAlignment]]:
    """
    Given a file with tokenized parallel sentences and alignments in XML format, return a list of sentence pairs
    and alignments for each sentence.

    Args:
        filename: Name of the file containing XML markup for labeled alignments

    Returns:
        sentence_pairs: list of `SentencePair`s for each sentence in the file
        alignments: list of `LabeledAlignment`s corresponding to these sentences
    """
    with open(filename, 'r', encoding='utf-8') as f:
        xml_str = f.read()
    xml_str = xml_str.replace('&', '&amp;')
    root = ET.fromstring(xml_str)
    sentences = []
    alignments = []
    for el in root.findall('s'):
        eng_el = el.find('english')
        cz_el = el.find('czech')
        if eng_el is None or cz_el is None:
            continue
        eng_t = eng_el.text.strip().split()
        cz_t = cz_el.text.strip().split()
        sure_el = el.find('sure')
        sure_list = []
        if sure_el is not None and sure_el.text is not None:
            sure_text = sure_el.text.strip()
            if sure_text:
                for pair in sure_text.split():
                    src_i, trg_i = pair.split('-')
                    sure_list.append((int(src_i), int(trg_i)))
        pos_el = el.find('possible')
        pos_list = []
        if pos_el is not None and pos_el.text is not None:
            pos_text = pos_el.text.strip()
            if pos_text:
                for pair in pos_text.split():
                    src_i, trg_i = pair.split('-')
                    pos_list.append((int(src_i), int(trg_i)))
        sentences.append(SentencePair(source=eng_t, target=cz_t))
        alignments.append(LabeledAlignment(sure=sure_list, possible=pos_list))
    return sentences, alignments


def get_token_to_index(sentence_pairs: List[SentencePair], freq_cutoff=None) -> \
Tuple[Dict[str, int], Dict[str, int]]:
    """
    Given a parallel corpus, create two dictionaries token->index for source and target language.

    Args:
        sentence_pairs: list of `SentencePair`s for token frequency estimation
        freq_cutoff: if not None, keep only freq_cutoff -- natural number -- most frequent tokens in each language

    Returns:
        source_dict: mapping of token to a unique number (from 0 to vocabulary size) for source language
        target_dict: mapping of token to a unique number (from 0 to vocabulary size) target language

    Tip:
        Use cutting by freq_cutoff independently in src and target. Moreover in both cases of freq_cutoff (None or not None) - you may get a different size of the dictionary

    """
    source_freq = {}
    target_freq = {}
    for pair in sentence_pairs:
        for tok in pair.source:
            if tok not in source_freq:
                source_freq[tok] = 0
            source_freq[tok] += 1
        for tok in pair.target:
            if tok not in target_freq:
                target_freq[tok] = 0
            target_freq[tok] += 1
    source_list = sorted(source_freq.items(), key=lambda x: x[1], reverse=True)
    target_list = sorted(target_freq.items(), key=lambda x: x[1], reverse=True)
    if freq_cutoff is not None:
        source_list = source_list[:freq_cutoff]
        target_list = target_list[:freq_cutoff]
    source_dict = {}
    for i, (tok, fr) in enumerate(source_list):
        source_dict[tok] = i
    target_dict = {}
    for i, (tok, fr) in enumerate(target_list):
        target_dict[tok] = i
    return source_dict, target_dict


def tokenize_sents(sentence_pairs: List[SentencePair], source_dict,
                   target_dict) -> List[TokenizedSentencePair]:
    """
    Given a parallel corpus and token_to_index for each language, transform each pair of sentences from lists
    of strings to arrays of integers. If either source or target sentence has no tokens that occur in corresponding
    token_to_index, do not include this pair in the result.

    Args:
        sentence_pairs: list of `SentencePair`s for transformation
        source_dict: mapping of token to a unique number for source language
        target_dict: mapping of token to a unique number for target language

    Returns:
        tokenized_sentence_pairs: sentences from sentence_pairs, tokenized using source_dict and target_dict
    """
    tokenized_sentence_pairs = []
    for pair in sentence_pairs:
        src_indices = []
        for tok in pair.source:
            if tok in source_dict:
                src_indices.append(source_dict[tok])
        tgt_indices = []
        for tok in pair.target:
            if tok in target_dict:
                tgt_indices.append(target_dict[tok])
        if len(src_indices) == 0 or len(tgt_indices) == 0:
            continue
        src_arr = np.array(src_indices)
        tgt_arr = np.array(tgt_indices)
        tokenized_sentence_pairs.append(
            TokenizedSentencePair(source_tokens=src_arr,
                                  target_tokens=tgt_arr))
    return tokenized_sentence_pairs
