#!/usr/bin/env python
# coding=utf-8

import unittest

from aeneas.idsortingalgorithm import IDSortingAlgorithm
from aeneas.language import Language
from aeneas.textfile import TextFile
from aeneas.textfile import TextFileFormat
from aeneas.textfile import TextFragment
import aeneas.globalconstants as gc
import aeneas.tests as at

class TestTextFile(unittest.TestCase):

    NOT_EXISTING_PATH = at.get_abs_path("not_existing.txt")
    NOT_WRITEABLE_PATH = at.get_abs_path("x/y/z/not_writeable.txt")
    EMPTY_FILE_PATH = "res/inputtext/empty.txt"
    BLANK_FILE_PATH = "res/inputtext/blank.txt"
    PLAIN_FILE_PATH = "res/inputtext/sonnet_plain.txt"
    UNPARSED_PARAMETERS = {
        gc.PPN_JOB_IS_TEXT_UNPARSED_ID_REGEX : "f[0-9]*",
        gc.PPN_JOB_IS_TEXT_UNPARSED_CLASS_REGEX : "ra",
        gc.PPN_JOB_IS_TEXT_UNPARSED_ID_SORT : IDSortingAlgorithm.UNSORTED,
    }
    ID_REGEX_PARAMETERS = {
        gc.PPN_TASK_OS_FILE_ID_REGEX : "word%06d"
    }
    ID_REGEX_PARAMETERS_BAD = {
        gc.PPN_TASK_OS_FILE_ID_REGEX : "word"
    }

    def load(self, input_file_path=PLAIN_FILE_PATH, fmt=TextFileFormat.PLAIN, expected_length=15, parameters=None):
        tfl = TextFile(at.get_abs_path(input_file_path), fmt, parameters)
        self.assertEqual(len(tfl), expected_length)
        return tfl

    def load_and_sort_id(self, input_file_path, id_regex, id_sort, expected):
        parameters = {}
        parameters[gc.PPN_JOB_IS_TEXT_UNPARSED_ID_REGEX] = id_regex
        parameters[gc.PPN_JOB_IS_TEXT_UNPARSED_ID_SORT] = id_sort
        tfl = self.load(input_file_path, TextFileFormat.UNPARSED, 5, parameters)
        i = 0
        for e in expected:
            self.assertEqual(tfl.fragments[i].identifier, e)
            i += 1

    def load_and_slice(self, expected, start=None, end=None):
        tfl = self.load()
        sli = tfl.get_slice(start, end)
        self.assertEqual(len(sli), expected)
        return sli

    def test_tf_identifier_str(self):
        with self.assertRaises(TypeError):
            tf = TextFragment(identifier="foo")

    def test_tf_identifier_unicode(self):
        tf = TextFragment(identifier=u"foo")
        self.assertEqual(len(tf), 0)

    def test_tf_lines_invalid(self):
        with self.assertRaises(TypeError):
            tf = TextFragment(lines="foo")

    def test_tf_lines_invalid_none(self):
        with self.assertRaises(TypeError):
            tf = TextFragment(lines=[None])

    def test_tf_lines_invalid_none_mixed(self):
        with self.assertRaises(TypeError):
            tf = TextFragment(lines=[u"foo", None, u"bar"])

    def test_tf_lines_invalid_str(self):
        with self.assertRaises(TypeError):
            tf = TextFragment(lines=["foo"])

    def test_tf_lines_invalid_str_mixed(self):
        with self.assertRaises(TypeError):
            tf = TextFragment(lines=[u"foo", "bar", u"baz"])

    def test_tf_lines_unicode(self):
        tf = TextFragment(lines=[u"foo"])
        self.assertEqual(len(tf), 1)

    def test_tf_lines_unicode_multiple(self):
        tf = TextFragment(lines=[u"foo", u"bar", u"baz"])
        self.assertEqual(len(tf), 3)

    def test_tf_lines_unicode_empty_string(self):
        tf = TextFragment(lines=[u""])
        self.assertEqual(len(tf), 1)

    def test_tf_lines_unicode_empty_string_multiple(self):
        tf = TextFragment(lines=[u"", u"", u""])
        self.assertEqual(len(tf), 3)

    def test_constructor(self):
        tfl = TextFile()
        self.assertEqual(len(tfl), 0)

    def test_file_path_not_existing(self):
        with self.assertRaises(IOError):
            tfl = TextFile(file_path=self.NOT_EXISTING_PATH)

    def test_invalid_format(self):
        with self.assertRaises(ValueError):
            tfl = TextFile(file_format="foo")

    def test_invalid_parameters(self):
        with self.assertRaises(TypeError):
            tfl = TextFile(parameters=["foo"])

    def test_invalid_fragments(self):
        tfl = TextFile()
        with self.assertRaises(TypeError):
            tfl.fragments = "foo"

    def test_empty_fragments(self):
        tfl = TextFile()
        tfl.fragments = []
        self.assertEqual(len(tfl), 0)
    
    def test_invalid_fragment(self):
        tfl = TextFile()
        with self.assertRaises(TypeError):
            tfl.fragments = ["foo"]

    def test_read_empty(self):
        for fmt in TextFileFormat.ALLOWED_VALUES:
            self.load(self.EMPTY_FILE_PATH, fmt, 0, self.UNPARSED_PARAMETERS)

    def test_read_blank(self):
        for fmt in TextFileFormat.ALLOWED_VALUES:
            expected = 0
            if fmt == TextFileFormat.PLAIN:
                expected = 5
            self.load(self.BLANK_FILE_PATH, fmt, expected, self.UNPARSED_PARAMETERS)

    def test_read_subtitles(self):
        for path in [
                "res/inputtext/sonnet_subtitles_with_end_newline.txt",
                "res/inputtext/sonnet_subtitles_no_end_newline.txt",
                "res/inputtext/sonnet_subtitles_multiple_blank.txt",
                "res/inputtext/sonnet_subtitles_multiple_rows.txt"
        ]:
            self.load(path, TextFileFormat.SUBTITLES, 15)

    def test_read_subtitles_id_regex(self):
        for path in [
                "res/inputtext/sonnet_subtitles_with_end_newline.txt",
                "res/inputtext/sonnet_subtitles_no_end_newline.txt",
                "res/inputtext/sonnet_subtitles_multiple_blank.txt",
                "res/inputtext/sonnet_subtitles_multiple_rows.txt"
        ]:
            self.load(path, TextFileFormat.SUBTITLES, 15, self.ID_REGEX_PARAMETERS)

    def test_read_subtitles_id_regex_bad(self):
        with self.assertRaises(TypeError):
            for path in [
                    "res/inputtext/sonnet_subtitles_with_end_newline.txt",
                    "res/inputtext/sonnet_subtitles_no_end_newline.txt",
                    "res/inputtext/sonnet_subtitles_multiple_blank.txt",
                    "res/inputtext/sonnet_subtitles_multiple_rows.txt"
            ]:
                self.load(path, TextFileFormat.SUBTITLES, 15, self.ID_REGEX_PARAMETERS_BAD)

    def test_read_plain(self):
        self.load("res/inputtext/sonnet_plain.txt", TextFileFormat.PLAIN, 15)

    def test_read_plain_id_regex(self):
        self.load("res/inputtext/sonnet_plain.txt", TextFileFormat.PLAIN, 15, self.ID_REGEX_PARAMETERS)

    def test_read_plain_id_regex_bad(self):
        with self.assertRaises(TypeError):
            self.load("res/inputtext/sonnet_plain.txt", TextFileFormat.PLAIN, 15, self.ID_REGEX_PARAMETERS_BAD)

    def test_read_plain_utf8(self):
        self.load("res/inputtext/sonnet_plain_utf8.txt", TextFileFormat.PLAIN, 15)

    def test_read_plain_utf8_id_regex(self):
        self.load("res/inputtext/sonnet_plain_utf8.txt", TextFileFormat.PLAIN, 15, self.ID_REGEX_PARAMETERS)

    def test_read_plain_utf8_id_regex_bad(self):
        with self.assertRaises(TypeError):
            self.load("res/inputtext/sonnet_plain_utf8.txt", TextFileFormat.PLAIN, 15, self.ID_REGEX_PARAMETERS_BAD)

    def test_read_parsed(self):
        self.load("res/inputtext/sonnet_parsed.txt", TextFileFormat.PARSED, 15)

    def test_read_parsed_bad(self):
        for path in [
                "res/inputtext/badly_parsed_1.txt",
                "res/inputtext/badly_parsed_2.txt",
                "res/inputtext/badly_parsed_3.txt"
        ]:
            self.load(path, TextFileFormat.PARSED, 0)

    def test_read_unparsed(self):
        for case in [
                {
                    "path": "res/inputtext/sonnet_unparsed_soup_1.txt",
                    "parameters": {
                        gc.PPN_JOB_IS_TEXT_UNPARSED_ID_REGEX : "f[0-9]*"
                    }
                },
                {
                    "path": "res/inputtext/sonnet_unparsed_soup_2.txt",
                    "parameters": {
                        gc.PPN_JOB_IS_TEXT_UNPARSED_ID_REGEX : "f[0-9]*",
                        gc.PPN_JOB_IS_TEXT_UNPARSED_CLASS_REGEX : "ra"
                    }
                },
                {
                    "path": "res/inputtext/sonnet_unparsed_soup_3.txt",
                    "parameters": {
                        gc.PPN_JOB_IS_TEXT_UNPARSED_CLASS_REGEX : "ra"
                    }
                },
                {
                    "path": "res/inputtext/sonnet_unparsed.xhtml",
                    "parameters": {
                        gc.PPN_JOB_IS_TEXT_UNPARSED_ID_REGEX : "f[0-9]*"
                    }
                },
        ]:
            self.load(case["path"], TextFileFormat.UNPARSED, 15, case["parameters"])

    def test_read_unparsed_unsorted(self):
        self.load_and_sort_id(
            "res/inputtext/sonnet_unparsed_order_1.txt",
            "f[0-9]*",
            IDSortingAlgorithm.UNSORTED,
            [u"f001", u"f003", u"f005", u"f004", u"f002"]
        )

    def test_read_unparsed_numeric(self):
        self.load_and_sort_id(
            "res/inputtext/sonnet_unparsed_order_2.txt",
            "f[0-9]*",
            IDSortingAlgorithm.NUMERIC,
            [u"f001", u"f2", u"f003", u"f4", u"f050"]
        )

    def test_read_unparsed_numeric_2(self):
        self.load_and_sort_id(
            "res/inputtext/sonnet_unparsed_order_3.txt",
            "f[0-9]*",
            IDSortingAlgorithm.NUMERIC,
            [u"f001", u"f2", u"f003", u"f4", u"f050"]
        )

    def test_read_unparsed_lexicographic(self):
        self.load_and_sort_id(
            "res/inputtext/sonnet_unparsed_order_4.txt",
            "[a-z][0-9]*",
            IDSortingAlgorithm.LEXICOGRAPHIC,
            [u"a005", u"b002", u"c004", u"d001", u"e003"]
        )

    def test_read_unparsed_numeric_3(self):
        self.load_and_sort_id(
            "res/inputtext/sonnet_unparsed_order_5.txt",
            "[a-z][0-9]*",
            IDSortingAlgorithm.NUMERIC,
            [u"d001", u"b002", u"e003", u"c004", u"a005"]
        )

    def test_set_language(self):
        tfl = self.load()
        tfl.set_language(Language.EN)
        for fragment in tfl.fragments:
            self.assertEqual(fragment.language, Language.EN)
        tfl.set_language(Language.IT)
        for fragment in tfl.fragments:
            self.assertEqual(fragment.language, Language.IT)

    def test_set_language_on_empty(self):
        tfl = TextFile()
        self.assertEqual(len(tfl), 0)
        tfl.set_language(Language.EN)
        self.assertEqual(len(tfl), 0)
        self.assertEqual(tfl.chars, 0)

    def test_read_from_list(self):
        tfl = TextFile()
        text_list = [
            u"fragment 1",
            u"fragment 2",
            u"fragment 3",
            u"fragment 4",
            u"fragment 5"
        ]
        tfl.read_from_list(text_list)
        self.assertEqual(len(tfl), 5)
        self.assertEqual(tfl.chars, 50)

    def test_read_from_list_with_ids(self):
        tfl = TextFile()
        text_list = [
            [u"a1", u"fragment 1"],
            [u"b2", u"fragment 2"],
            [u"c3", u"fragment 3"],
            [u"d4", u"fragment 4"],
            [u"e5", u"fragment 5"]
        ]
        tfl.read_from_list_with_ids(text_list)
        self.assertEqual(len(tfl), 5)
        self.assertEqual(tfl.chars, 50)

    def test_append_fragment(self):
        tfl = TextFile()
        self.assertEqual(len(tfl), 0)
        tfl.append_fragment(TextFragment(u"a1", Language.EN, [u"fragment 1"]))
        self.assertEqual(len(tfl), 1)
        self.assertEqual(tfl.chars, 10)

    def test_append_fragment_multiple(self):
        tfl = TextFile()
        self.assertEqual(len(tfl), 0)
        tfl.append_fragment(TextFragment(u"a1", Language.EN, [u"fragment 1"]))
        self.assertEqual(len(tfl), 1)
        tfl.append_fragment(TextFragment(u"a2", Language.EN, [u"fragment 2"]))
        self.assertEqual(len(tfl), 2)
        tfl.append_fragment(TextFragment(u"a3", Language.EN, [u"fragment 3"]))
        self.assertEqual(len(tfl), 3)
        self.assertEqual(tfl.chars, 30)

    def test_get_slice_no_args(self):
        tfl = self.load()
        sli = tfl.get_slice()
        self.assertEqual(len(sli), 15)
        self.assertEqual(sli.chars, 597)

    def test_get_slice_only_start(self):
        sli = self.load_and_slice(10, 5)
        self.assertEqual(sli.chars, 433)

    def test_get_slice_start_and_end(self):
        sli = self.load_and_slice(5, 5, 10)
        self.assertEqual(sli.chars, 226)

    def test_get_slice_start_greater_than_length(self):
        sli = self.load_and_slice(1, 100)
        self.assertEqual(sli.chars, 46)

    def test_get_slice_start_less_than_zero(self):
        sli = self.load_and_slice(15, -1)
        self.assertEqual(sli.chars, 597)

    def test_get_slice_end_greater_then_length(self):
        sli = self.load_and_slice(15, 0, 100)
        self.assertEqual(sli.chars, 597)

    def test_get_slice_end_less_than_zero(self):
        sli = self.load_and_slice(1, 0, -1)
        self.assertEqual(sli.chars, 1)

    def test_get_slice_end_less_than_start(self):
        sli = self.load_and_slice(1, 10, 5)
        self.assertEqual(sli.chars, 36)

if __name__ == '__main__':
    unittest.main()



