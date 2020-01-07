/*
 * Copyright (c) 2015-2016 Spotify AB
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

#include <string>

#include <boost/test/unit_test.hpp>

#include <spotify/json/codec/map.hpp>
#include <spotify/json/codec/boolean.hpp>
#include <spotify/json/decode.hpp>
#include <spotify/json/decode_exception.hpp>
#include <spotify/json/encode.hpp>

BOOST_AUTO_TEST_SUITE(spotify)
BOOST_AUTO_TEST_SUITE(json)
BOOST_AUTO_TEST_SUITE(codec)

namespace {

std::string string_parse(const char *string) {
  const auto codec = default_codec<std::string>();
  auto ctx = decode_context(string, string + strlen(string));
  const auto result = codec.decode(ctx);
  BOOST_CHECK_EQUAL(ctx.position, ctx.end);
  return result;
}

void string_parse_fail(const char *string) {
  auto ctx = decode_context(string, string + strlen(string));
  BOOST_CHECK_THROW(default_codec<std::string>().decode(ctx), decode_exception);
}

std::string random_simple_character(size_t i) {
  char c;
  switch (i % 3) {
    case 0: c = '0' + (i % 10); break;
    case 1: c = 'a' + (i % ('z' - 'a')); break;
    case 2: c = 'A' + (i % ('Z' - 'A')); break;
  }
  return std::string(&c, 1);
}

std::string random_simple_character_or_escape_sequence(size_t i, bool minimal_escaping) {
  switch (i % 37) {
    case 27: return "\\u0000";
    case 28: return "\\\"";
    case 29: return minimal_escaping ? "/" : "\\/";
    case 30: return "\\b";
    case 31: return "\\f";
    case 32: return "\\n";
    case 33: return "\\r";
    case 34: return "\\t";
    case 35: return "\\\\";
    case 36: return minimal_escaping ? "\xE2\x82\xAC" : "\\u20AC";
    default: return random_simple_character(i);
  }
}

std::string random_simple_character_or_unescaped_character(size_t i) {
  // Note: since one case below returns 3 bytes and all the other return 1, the
  // total number of bytes in one rotation is 39. This number is coprime with
  // 16, which is the number of bytes in an SSE block, so this will ensure that
  // each byte will end up first in a 16-byte SSE block eventually.
  switch (i % 37) {
    case 27: return std::string(1, '\0');
    case 28: return "\"";
    case 29: return "/";
    case 30: return "\b";
    case 31: return "\f";
    case 32: return "\n";
    case 33: return "\r";
    case 34: return "\t";
    case 35: return "\\";
    case 36: return "\xE2\x82\xAC";
    default: return random_simple_character(i);
  }
}

std::string generate_simple_string(size_t size) {
  std::string string("\"");
  for (size_t i = 0; i < size; i++) {
    string.append(random_simple_character(i));
  }
  string.append("\"");
  return string;
}

std::string generate_simple_string_answer(size_t size) {
  std::string string;
  for (size_t i = 0; i < size; i++) {
    string.append(random_simple_character(i));
  }
  return string;
}

std::string generate_escaped_string(size_t approximate_size, bool minimal_escaping = false) {
  std::string string("\"");
  for (size_t i = 0; i < approximate_size; i++) {
    string.append(random_simple_character_or_escape_sequence(i, minimal_escaping));
  }
  string.append("\"");
  return string;
}

std::string generate_escaped_string_answer(size_t approximate_size) {
  std::string string;
  for (size_t i = 0; i < approximate_size; i++) {
    string.append(random_simple_character_or_unescaped_character(i));
  }
  return string;
}

std::string generate_utf8_string_answer(size_t size) {
  std::string string;
  for (size_t i = 0; i < size; i++) {
    string.append("\xE2\x98\x83");
  }
  return string;
}

std::string generate_utf8_string(size_t size) {
  std::string string("\"");
  for (size_t i = 0; i < size; i++) {
    string.append("\xE2\x98\x83");
  }
  string.append("\"");
  return string;
}

}  // namespace

/*
 * Constructing
 */

BOOST_AUTO_TEST_CASE(json_codec_string_should_construct_with_helper) {
  string();
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_construct_with_default_codec) {
  default_codec<std::string>();
}

/*
 * Decoding Simple Strings
 */

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_empty) {
  BOOST_CHECK_EQUAL(string_parse("\"\""), "");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_single_letter) {
  BOOST_CHECK_EQUAL(string_parse("\"a\""), "a");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_letters) {
  BOOST_CHECK_EQUAL(string_parse("\"abc\""), "abc");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_long_string) {
  const auto string = generate_simple_string(10027);
  const auto answer = string.substr(1, string.size() - 2);
  BOOST_CHECK_EQUAL(string_parse(string.c_str()), answer);
}

/*
 * Decoding Invalid Strings
 */

BOOST_AUTO_TEST_CASE(json_codec_string_should_not_decode_invalid) {
  string_parse_fail("");
  string_parse_fail("\"");
}

/*
 * Decoding Escaped Strings
 */

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_escaped_characters) {
  BOOST_CHECK_EQUAL(string_parse("\"\\\"\""), "\"");
  BOOST_CHECK_EQUAL(string_parse("\"\\/\""), "/");
  BOOST_CHECK_EQUAL(string_parse("\"\\b\""), "\b");
  BOOST_CHECK_EQUAL(string_parse("\"\\f\""), "\f");
  BOOST_CHECK_EQUAL(string_parse("\"\\n\""), "\n");
  BOOST_CHECK_EQUAL(string_parse("\"\\r\""), "\r");
  BOOST_CHECK_EQUAL(string_parse("\"\\t\""), "\t");
  BOOST_CHECK_EQUAL(string_parse("\"\\\\\""), "\\");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_escaped_string_with_unescaped_parts) {
  BOOST_CHECK_EQUAL(string_parse("\"prefix\\nmiddle\\nsuffix\""), "prefix\nmiddle\nsuffix");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_escaped_unicode) {
  // Examples from http://en.wikipedia.org/wiki/UTF-8#Examples
  BOOST_CHECK_EQUAL(string_parse("\"\\u0024\""), "\x24");
  BOOST_CHECK_EQUAL(string_parse("\"\\u00A2\""), "\xC2\xA2");
  BOOST_CHECK_EQUAL(string_parse("\"\\u20AC\""), "\xE2\x82\xAC");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_surrogate_pairs) {
  // [TWO HEARTS] Emoji (code point 0x1F495)
  const std::string two_hearts = "\xf0\x9f\x92\x95";
  BOOST_CHECK_EQUAL(string_parse("\"I \\ud83d\\udc95 Unicode\""),
                    "I " + two_hearts + " Unicode");
  BOOST_CHECK_EQUAL(string_parse("\"I\\n\\ud83d\\udc95\\nUnicode\""),
                    "I\n" + two_hearts + "\nUnicode");
  // Extreme values of each surrogate
  BOOST_CHECK_EQUAL(string_parse("\"\\ud800\\udc00\""), "\xf0\x90\x80\x80");
  BOOST_CHECK_EQUAL(string_parse("\"\\ud800\\udfff\""), "\xf0\x90\x8f\xbf");
  BOOST_CHECK_EQUAL(string_parse("\"\\udbff\\udc00\""), "\xf4\x8f\xb0\x80");
  BOOST_CHECK_EQUAL(string_parse("\"\\udbff\\udfff\""), "\xf4\x8f\xbf\xbf");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_output_code_points_from_broken_surrogate_pairs) {
  // [TWO HEARTS] Emoji (code point 0x1F495)
  const std::string two_hearts = "\xf0\x9f\x92\x95";
  // UTF-8 representations of code points 0xd83d and 0xdc95, which form the
  // surrogate pairs for the emoji above.
  const std::string high = "\xed\xa0\xbd";
  const std::string low = "\xed\xb2\x95";

  // Lone high surrogate
  BOOST_CHECK_EQUAL(string_parse("\"\\ud83d\""), high);
  BOOST_CHECK_EQUAL(string_parse("\"\\n\\ud83d\\n\""), "\n" + high + "\n");
  BOOST_CHECK_EQUAL(string_parse("\"\\\\\\ud83d\\\\\""), "\\" + high + "\\");
  BOOST_CHECK_EQUAL(string_parse("\"Foo\\ud83dFoo\""), "Foo" + high + "Foo");
  BOOST_CHECK_EQUAL(string_parse("\"\\ud83d\\ud83d\\udc95\""), high + two_hearts);

  // Lone low surrogate
  BOOST_CHECK_EQUAL(string_parse("\"\\udc95\""), low);
  BOOST_CHECK_EQUAL(string_parse("\"\\n\\udc95\\n\""), "\n" + low + "\n");
  BOOST_CHECK_EQUAL(string_parse("\"\\\\\\udc95\\\\\""), "\\" + low + "\\");
  BOOST_CHECK_EQUAL(string_parse("\"Foo\\udc95Foo\""), "Foo" + low + "Foo");
  BOOST_CHECK_EQUAL(string_parse("\"\\udc95\\ud83d\\udc95\""), low + two_hearts);

  // Flipped order surrogates
  BOOST_CHECK_EQUAL(string_parse("\"\\udc95\\ud83d\""), low + high);

  // Double high surrogate
  BOOST_CHECK_EQUAL(string_parse("\"\\ud83d\\ud83d\""), high + high);

  // Double low surrogate
  BOOST_CHECK_EQUAL(string_parse("\"\\udc95\\udc95\""), low + low);

  // Intermingled valid and invalid sequences
  BOOST_CHECK_EQUAL(string_parse("\"\\ud83d\\udc95\\udc95\""), two_hearts + low);
  BOOST_CHECK_EQUAL(string_parse("\"\\ud83d\\udc95\\ud83d\""), two_hearts + high);
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_not_decode_incomplete_low_surrogate) {
  string_parse_fail("\"\\ud83d\\\"");
  string_parse_fail("\"\\ud83d\\u\"");
  string_parse_fail("\"\\ud83d\\udc9\"");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_not_decode_invalid_escaped_characters) {
  string_parse_fail("\"\\q\"");  // \q is not a valid escape sequence
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_not_decode_invalid_unicode_escape_sequences) {
  string_parse_fail("\"\\u0\"");
  string_parse_fail("\"\\u01\"");
  string_parse_fail("\"\\u012\"");
  string_parse_fail("\"\\u_FFF\"");
  string_parse_fail("\"\\uF_FF\"");
  string_parse_fail("\"\\uFF_F\"");
  string_parse_fail("\"\\uFFF_\"");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_decode_long_escaped_string) {
  const auto string = generate_escaped_string(10027);
  const auto answer = generate_escaped_string_answer(10027);
  BOOST_CHECK_EQUAL(string_parse(string.c_str()), answer);
}

/*
 * Encoding Simple Strings
 */

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_empty) {
  BOOST_CHECK_EQUAL(encode(std::string()), "\"\"");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_single_character) {
  BOOST_CHECK_EQUAL(encode(std::string("a")), "\"a\"");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_long_string) {
  const auto string = generate_simple_string_answer(10027);
  const auto answer = generate_simple_string(10027);
  BOOST_CHECK_EQUAL(encode(string), answer);
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_long_utf8_string) {
  const auto string = generate_utf8_string_answer(10027);
  const auto answer = generate_utf8_string(10027);
  BOOST_CHECK_EQUAL(encode(string), answer);
}

/*
 * Encoding Escaped Strings
 */

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_escaped_character) {
  BOOST_CHECK_EQUAL(encode(std::string("\"")), "\"\\\"\"");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_popular_escaped_characters) {
  const auto string = "\b\t\n\f\r";
  const auto answer = "\"\\b\\t\\n\\f\\r\"";
  BOOST_CHECK_EQUAL(encode(std::string(string)), answer);
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_escaped_control_characters) {
  BOOST_CHECK_EQUAL(encode(std::string("\x01\x02")), "\"\\u0001\\u0002\"");
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_null_char) {
  // Enough zero bytes to get a full 16-byte SSE block, regardless of what
  // memory aligment the string data happens to get.
  const std::string input_data(31, '\0');

  std::string expected_result = "\"";
  for (std::size_t i = 0; i < input_data.size(); i++) {
    expected_result += "\\u0000";
  }
  expected_result += "\"";

  BOOST_CHECK_EQUAL(encode(input_data), expected_result);
}

BOOST_AUTO_TEST_CASE(json_codec_string_should_encode_long_string_with_special_chars) {
  const auto input_str = generate_escaped_string_answer(10000);
  const auto expected_result = generate_escaped_string(10000, true);
  BOOST_CHECK(encode(input_str) == expected_result);
}

BOOST_AUTO_TEST_SUITE_END()  // codec
BOOST_AUTO_TEST_SUITE_END()  // json
BOOST_AUTO_TEST_SUITE_END()  // spotify
