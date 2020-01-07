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

#include <spotify/json/detail/skip_chars.hpp>

#include <spotify/json/detail/macros.hpp>

#include "skip_chars_common.hpp"

namespace spotify {
namespace json {
namespace detail {

void skip_any_simple_characters_scalar(decode_context &context) {
  const auto end = context.end;
  auto pos = context.position;
  JSON_STRING_SKIP_N_SIMPLE(1,  2, uint8_t,  if, done_x)
  JSON_STRING_SKIP_N_SIMPLE(2,  4, uint16_t, if, done_2)
  JSON_STRING_SKIP_N_SIMPLE(4,  8, uint32_t, if, done_4)
          JSON_STRING_SKIP_N_SIMPLE(8, x, uint64_t, while, done_8)
  done_8: JSON_STRING_SKIP_N_SIMPLE(4, x, uint32_t, while, done_4)
  done_4: JSON_STRING_SKIP_N_SIMPLE(2, x, uint16_t, while, done_2)
  done_2: JSON_STRING_SKIP_N_SIMPLE(1, x, uint8_t,  while, done_x)
  done_x: context.position = pos;
}

void skip_any_whitespace_scalar(decode_context &context) {
  const auto end = context.end;
  auto pos = context.position;
  while (pos < end && is_space(*pos)) {
    ++pos;
  }
  context.position = pos;
}

}  // namespace detail
}  // namespace json
}  // namespace spotify
