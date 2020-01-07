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
#include <vector>

#include <boost/test/unit_test.hpp>

#include <spotify/json/codec/array.hpp>
#include <spotify/json/codec/transform.hpp>
#include <spotify/json/codec/string.hpp>
#include <spotify/json/decode.hpp>
#include <spotify/json/encode.hpp>

BOOST_AUTO_TEST_SUITE(spotify)
BOOST_AUTO_TEST_SUITE(json)
BOOST_AUTO_TEST_SUITE(codec)

namespace {

template <typename Codec>
typename Codec::object_type test_decode(const Codec &codec, const std::string &json) {
  decode_context c(json.c_str(), json.c_str() + json.size());
  auto obj = codec.decode(c);
  BOOST_CHECK_EQUAL(c.position, c.end);
  return obj;
}

struct my_type {
  std::string value;
};

std::string encodeTransform(const my_type &object) {
  return object.value;
}

my_type decodeTransform(const std::string &value) {
  return my_type{ value };
}

}  // namespace

/*
 * Constructing
 */

BOOST_AUTO_TEST_CASE(json_codec_transform_should_construct) {
  transform_t<string_t, decltype(&encodeTransform), decltype(&decodeTransform)> codec(
      string(), &encodeTransform, &decodeTransform);
}

BOOST_AUTO_TEST_CASE(json_codec_transform_should_construct_with_helper_with_codec) {
  transform(string(), &encodeTransform, &decodeTransform);
}

BOOST_AUTO_TEST_CASE(json_codec_transform_should_construct_with_helper) {
  transform(&encodeTransform, &decodeTransform);
}

/*
 * Decoding
 */

BOOST_AUTO_TEST_CASE(json_codec_transform_should_decode) {
  const auto codec = transform(&encodeTransform, &decodeTransform);
  const my_type result = test_decode(codec, "\"A\"");
  BOOST_CHECK_EQUAL(result.value, "A");
}

BOOST_AUTO_TEST_CASE(json_codec_transform_should_update_offset_when_throwing_exception) {
  try {
    const auto fail = [](const std::string &) { throw decode_exception("test"); return my_type(); };
    json::decode(transform(&encodeTransform, fail), " \"A\"");
    BOOST_CHECK(false);
  } catch (const decode_exception &exception) {
    BOOST_CHECK_EQUAL(exception.what(), "test");
    BOOST_CHECK_EQUAL(exception.offset(), 1);
  }
}

/*
 * Encoding
 */

BOOST_AUTO_TEST_CASE(json_codec_transforms_should_encode) {
  const auto codec = transform(&encodeTransform, &decodeTransform);
  BOOST_CHECK_EQUAL(encode(codec, my_type{ "A" }), "\"A\"");
}

BOOST_AUTO_TEST_SUITE_END()  // codec
BOOST_AUTO_TEST_SUITE_END()  // json
BOOST_AUTO_TEST_SUITE_END()  // spotify
