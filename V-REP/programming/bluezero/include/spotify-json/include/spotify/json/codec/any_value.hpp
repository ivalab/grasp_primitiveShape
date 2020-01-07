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

#pragma once

#include <cstdlib>

#include <spotify/json/decode_context.hpp>
#include <spotify/json/default_codec.hpp>
#include <spotify/json/detail/skip_value.hpp>
#include <spotify/json/encode_context.hpp>
#include <spotify/json/encoded_value.hpp>

namespace spotify {
namespace json {
namespace codec {

class any_value_t final {
 public:
  using object_type = encoded_value_ref;

  object_type decode(decode_context &context) const {
    const auto begin = context.position;
    detail::skip_value(context);
    const auto size = context.position - begin;
    return object_type(begin, size, object_type::unsafe_unchecked());
  }

  void encode(encode_context &context, const object_type &value) const {
    context.append(value.data(), value.size());
  }
};

inline any_value_t any_value() {
  return any_value_t();
}

}  // namespace codec

template<>
struct default_codec_t<encoded_value> {
  static codec::any_value_t codec() {
    return codec::any_value();
  }
};

template<>
struct default_codec_t<encoded_value_ref> {
  static codec::any_value_t codec() {
    return codec::any_value();
  }
};

}  // namespace json
}  // namespace spotify
